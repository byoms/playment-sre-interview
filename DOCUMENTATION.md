# mctl #

**mctl** is a command line utility that can be used to consume messages from a queue and store them in a database. Additionally it can be used to also fetch the stored messages and delete them if needed. Currently the tool supports AWS SQS and DynamoDB.

Messages are stored in a table named "Messages". If a table with that name does not exist already it will be created.
Some other static configurations such as queue name, aws endpoint and region are currently hard-coded just to keep usage in the context of the assignment simple. In it's current form it can be easily extended to be separated out to work with a config file or any desired external source if needed.


## Requirements ##

### GNU/Linux ###

  - **Python 3** is required (v3.7 minimum). This was developed and tested on **v3.9** so it is highly recommended to use the same if possible
    + **python3-pip** - python's standard package manager
    + **python3-venv** - a standard python virtual-environment creation tool
    + **python3-distutils** - distutils package for Python 3.x

To install on Debian/Ubuntu run:

```
apt update && apt install -y python3-pip python3-venv python3-distutils
```

## Installation ##

### Building from source and installing locally ###

**Important pre-requisite:**

Please ensure the local bin path (for eg. `~/.local/bin` in Debian/Ubuntu) is included in `PATH`. This is sometimes optionally enabled as a part of `~/.profile`. It can be verified by checking `PATH` using `echo $PATH`. If absent run:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

and add the same to you shell initialisation config file for permanent configuration.

### A note on the installation hygiene ###

The above is **important** and is **required** for the installation to work. This is by design because especially in case of python installing packages at the system level can break system utilities that use python. Additionally, this also avoids requiring superuser privileges. The tool and related dependencies will be installed at the user account level. Furthermore as `pipx` is used internally for installation, it is sandboxed into a separate environment and avoid conflicts even locally!

### Installation steps ###

```
# download
git clone https://github.com/byoms/playment-sre-interview/tree/subm/byomakesh-m
# install locally
cd ./playment-sre-interview/
make install
```


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

### Commands ###

| Command      |  Description |
| ----------- | --------------------|
| consume      | Consume messages from queue and store in DB <br/>`-c, --count`<br/><ensp> Specify message count (**required**) |
| show   | Show all messages currently stored in DB |
| clear  | Clear all stored messages from DB |

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


## Un-install ##

```
make uninstall
make clean
```

---

## Notes ##

  - Learning localstack
  - Fix docker-compose
  - Learning SQS and DynamoDB
  - CLI tool
  - Documentation
  - Makefile