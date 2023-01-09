# Localstack SQS Exercise

In this exercise, you are expected to develop a commandline tool. The tool should consume messages in an AWS SQS queue, store the
results in a database, then show the results when asked.

After the implementation, please proceed to Questions section, and include them in your `ANSWERS.md` file.

Expectations from you are:

* Research and understand how AWS SQS works on a basic level
* Submit a working solution
* Solve problems that might occur during the setup (yes, we know about localhost:4567)
* Provide documentation (explained in `Documentation` section)
* Provide answers to 5 questions (explained in `Questions` section)

## Localstack
https://github.com/localstack/localstack

Instead of using an actual AWS account, you will use a localstack implementation to imitate AWS services. Localstack
uses the same API with AWS services, you can use the same API by targeting the local endpoint: `localhost:4576`

## Requirements
- [docker](https://www.docker.com/get-started)
- [docker-compose](https://docs.docker.com/compose/install/)

## Input
In this exercise you have three files:
- `docker-compose.yml` 
- `mesage_generator`
- `README.md`

To setup the localstack environment, run:
```bash
$ docker-compose up
```

To setup the test case, you can run `message-generator`s appropriate for your environment. Right now darwin, linux, and
windows OSs are supported:
```bash
$ ls message-generators
darwin       linux        windows.exe
$ ./message-generators/linux    # for linux
$ ./message-generators/darwin   # for macos
$ ./message-generators/generator.py  # python script which will work for all systems
```

**P.S.**: You can run `message-generator` to generate more messages.

Follow the outputs to configure your tool.

## Output
The commandline tool should be able to run with given arguments & exit afterwards.

### Options & Parameters
The commandline tool should support following options:

- `consume --count n`: Consume `n` messages
    Prints `n` consumed messages with message content and `MessageId`s from SQS context
- `show`: Show all consumed messages
    Prints all consumed messages with message content and `MessageId`s from SQS context
- `clear`: Clear all consumed messages from database

In the end, the command will be: `<command> consume [--count n] | show | clear`

### Persisting
You need to persist the consumed messages. The tool should be able to run multiple times, just like any other
commandline tool.

**You need to persist each message only once, there shouldn't be any duplicates.**

Please setup a local database, that can be reproducible in our systems as well (both Linux and Darwin). We prefer to have a `docker run`
command to run the database of your choice.

### Language
Please prepare your solution in one of the following languages:
- Java
- Kotlin
- Go
- Python 3
- Any Linux scripting language

Please motivate your choice of programming language in the documentation.

### Documentation
You are expected to provide the source code and a documentation of the tool. Please add a `DOCUMENTATION.md` file in
you submission which includes:

- Tool introduction/explanation
- How to build the tool and build requirements
- How to configure the environment (if necessary)
- How to run the tool
- How to use the tool (options, parameters, etc.)
- Challenges while solving the problem

### Questions
Please answer these questions in `ANSWERS.md` file.

- Q1: Please explain what is the advantage of using SQS in this solution.
- Q2: Compare SQS to a message broker you have used before. What are the differences? Strong/weak points? (If you
    did not use such a solution, please skip this question)
- Q3: If we run multiple instances of this tool, what prevents a message from processed twice?
- Q4: In very rough terms, can you suggest an alternative solution aside from using SQS from your previous experience
    using different technologies?


### Submission format
Please open a Pull/Merge request to this repository.

```
$ tree .
├── DOCUMENTATION.md
├── ANSWERS.md
└── src
    └── ...
```
Please include DOCUMENTATION.md, source code, and build scripts if necessary to your submission.

Your submission should be able to run with a single command. You can add a `run.sh` script that runs required commands if needed. See Bonus Points #3.

--

Your program will be judged on the quality of the code as well as the correctness of the output.

## Bonus points
1. Include your database setup to `docker-compose` setup as container.
2. Make your tool runnable by docker. Provide running instructions.
3. Prepare a Makefile that builds your submission and runs it.
4. Use DynamoDB as your database of choice.

--

Prepared by Playment SRE Team