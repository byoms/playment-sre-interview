# mctl #

**mctl** is a command line utility that can be used to consume messages from a queue and store them in a database. Additionally it can be used to also fetch the stored messages and delete them if needed. Currently the tool supports AWS SQS and DynamoDB.

Messages are stored in a table named "Messages". If a table with that name does not exist already it will be created.
Some other static configurations such as queue name, aws endpoint and region are currently hard-coded just to keep usage in the context of the assignment simple. In it's current form it can be easily extended to be separated out to work with a config file or source if needed.


## Requirements ##

### GNU/Linux ###

  - **Python 3** is required (v3.7 minimum). This was developed and tested on **v3.9** so it is highly recommended to use the same if possible
  - **pip** - python's standard package manager

#### Docker ####

## Configuration ##

The code uses environment variables to access AWS credentials. Hence for the script to work ensure that the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are configured accordingly. For localstack the following can be used

```sh
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
```


## Usage ##

```
mctl [OPTIONS] COMMAND [ARGS]
```


### Global options ###

```
  -h, --help            show help message and exit
  -d, --debug           enable additional debug info in console output
```


### Commands and options ###


| Command      | Options | Description |
| ----------- | ----------- |----------|
| consume      | `-c`<br/>`--count` | Consume messages from queue and store in DB. Use `-c/--count` to specify message count (**required**) |
| show   | -       | Show all messages currently stored in DB |
| clear | - | Clear all messages from DB |


### Examples ###

To consume 5 messages from the queue and store in DB

```sh
mctl consume --count 5
```

To show all messages stored in DB

```sh
mctl show
```

To clear all messages in DB

```sh
mctl clear
```
