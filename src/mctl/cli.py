#!/usr/bin/env python3

# standard libs
import argparse
import os
import sys
import logging

# additional packages
import boto3
import botocore

# static configs
QUEUE_NAME = 'test-queue'
AWS_REGION = 'ap-southeast-1'
AWS_ENDPOINT = "http://localhost:4566"
DB_NAME = "Messages"

# global logging configuration
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S %Z',
    level=logging.WARNING
)

def check_creds():

    if "AWS_ACCESS_KEY_ID" not in os.environ:
        logging.error("Error: Missing credentials - AWS_ACCESS_KEY_ID not set in the environment. Exiting..")
        sys.exit(1)
    if "AWS_SECRET_ACCESS_KEY" not in os.environ:
        logging.error("Error: Missing credentials - AWS_SECRET_ACCESS_KEY not set in the environment. Exiting..")
        sys.exit(1)
    
    return

def positive_int(input_str):

    try:
        value = int(input_str)
    except ValueError:
        error_message1 = f"Provided input: {input_str} is invalid - not an integer"
        raise argparse.ArgumentTypeError(error_message1)
    if value <= 0:
        error_message2 = f"Provided input: {input_str} is invalid - not a positive integer"
        raise argparse.ArgumentTypeError(error_message2)

    return value

def get_args():

    parser = argparse.ArgumentParser(description="A command line SQS message processing utility")
    parser.add_argument('-d', '--debug', action='store_true',
        help="enable additional debug info in console output"
    )
    subparser = parser.add_subparsers(
        title = "sub-commands",
        description = "valid sub-commands",
        help = "additional sub-command help",
        dest = 'cmd'
    )

    consume_subcmd_parser = subparser.add_parser('consume')
    subparser.add_parser('show')
    subparser.add_parser('clear')

    consume_required_args = consume_subcmd_parser.add_argument_group("Required arguments")
    consume_required_args.add_argument(
        '-c', '--count', type=positive_int, required=True, 
        help="Count of the total number of messages to be consumed/processed"
    )

    args = parser.parse_args()

    return args

class MessageQueue:

    def __init__(self, queue_name, dynamodb_table):
        try:
            session = boto3.session.Session(region_name=AWS_REGION)
            sqs_client = session.client('sqs', endpoint_url=AWS_ENDPOINT)
            queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
            sqs = session.resource('sqs', endpoint_url=AWS_ENDPOINT)

            self.queue = sqs.Queue(queue_url)
            self.db_table = dynamodb_table
        
        except botocore.exceptions.EndpointConnectionError as ClientErr:
            logging.error("Failed to connect to the SQS endpoint. Exiting..")
            sys.exit(1)
        
        except botocore.exceptions.ClientError as ClientErr:
            if ClientErr.response['Error']['Code'] != 'AWS.SimpleQueueService.NonExistentQueue':
                logging.error("Unexpected error when connecting with SQS. Exiting..")
                sys.exit(1)
            else:
                logging.error("The specified Queue does not exist. Exiting..")
                sys.exit(1)
        
    
    def process_messages(self, message_count):
        for iteration in range(message_count):
            message = self.queue.receive_messages(WaitTimeSeconds=1, MaxNumberOfMessages=1)[0]
            try:
                self.db_table.put_item(
                    Item = {
                        "msg_id": message.message_id,
                        "msg_body": message.body
                    },
                    ConditionExpression = "attribute_not_exists(msg_id)" # de-dup
                )
                logging.info(f"Stored message with message ID: {message.message_id} in DB.")
            except botocore.exceptions.ClientError as ClientErr:
                if ClientErr.response['Error']['Code'] != 'ConditionalCheckFailedException':
                    logging.error("Unexpected error when storing message in DB. Exiting..")
                    sys.exit(1)
                else:
                    logging.info(f"Message with {message.message_id} already exists. Skipping..")
            
            message.delete()
        
        return

class MessageDB:

    def __init__(self, table_name):
        # check if table exists and create if not
        try:
            session = boto3.session.Session(region_name=AWS_REGION)
            dynamodb_client = session.client('dynamodb', endpoint_url=AWS_ENDPOINT)
            dynamodb = session.resource('dynamodb', endpoint_url=AWS_ENDPOINT)

            tables = dynamodb_client.list_tables()['TableNames']
            
            if table_name not in tables:
                logging.info("Table not present, creating..")
                dynamodb.create_table(
                    TableName = table_name,
                    KeySchema = [
                        {'AttributeName': 'msg_id', 'KeyType': 'HASH'}
                    ],
                    AttributeDefinitions = [
                        {'AttributeName': 'msg_id', 'AttributeType': 'S'}
                    ],
                    ProvisionedThroughput = {'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
                )
                logging.info(f"Table created. Table name: {table_name}")

            self.main_table = dynamodb.Table(table_name)
        
        except botocore.exceptions.EndpointConnectionError as ClientErr:
            logging.error("Failed to connect to the DB (DynamoDB) endpoint. Exiting..")
            sys.exit(1)

    def get_all_messages(self):
        
        table_scan = self.main_table.scan()
        stored_messages = table_scan['Items']
        # paginate if required:
        while 'LastEvaluatedKey' in table_scan:
            logging.info("Scanning not complete, scanning next page..")
            table_scan = self.main_table.scan(ExclusiveStartKey=table_scan['LastEvaluatedKey'])
            stored_messages.extend(table_scan['Items'])

        return stored_messages

    
    def show_messages(self):
        for stored_msg in self.get_all_messages():
            print(f"{stored_msg['msg_id']} {stored_msg['msg_body']}")
        
        return
    
    def clear_messages(self):
        with self.main_table.batch_writer() as batch_op:
            for stored_msg in self.get_all_messages():
                batch_op.delete_item(
                    Key = {
                        'msg_id': stored_msg['msg_id']
                    }
                )
                logging.info(f"Deleted message with message ID: {stored_msg['msg_id']}")
        
        return

def main():

    # parse command
    args = get_args()

    # verify if environment is configured with the required credentials
    check_creds()

    # initialise our resources
    message_db = MessageDB(DB_NAME)
    message_queue = MessageQueue(QUEUE_NAME, message_db.main_table)

    # enable additional info logging for troubleshooting if option specified via CLI
    if args.debug == True:
        logging.getLogger().setLevel(logging.INFO)

    # select action as per command
    if args.cmd == 'consume':
        message_queue.process_messages(args.count)
    elif args.cmd == 'show':
        message_db.show_messages()
    elif args.cmd == 'clear':
        message_db.clear_messages()
    else:
        logging.error('Unknown error parsing command. Exiting..')
        sys.exit(1)

    
    return

if __name__ == '__main__':
    main()
