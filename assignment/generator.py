import boto3
import random
sqs = boto3.client('sqs',endpoint_url="http://localhost:4576")
sqs.create_queue(QueueName='test-queue')
count = random.randint(10, 100)
while count > 0 :
    message_body="Test message {}".format(count)
    sqs.send_message(QueueUrl='http://localhost:4576/000000000000/test-queue',MessageBody=message_body)
    count-=1
   

