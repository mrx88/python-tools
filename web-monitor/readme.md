# Web Monitor

## Introduction

A web monitor application that feeds information about website availability over a Kafka instance to be inserted into a PostgreSQL instance.

This application is structured in two parts:

* A producer which periodically checks target websites for their status and sends the results to a Kafka topic.
* A consumer that reads the Kafka topic and stores the results to a PostgreSQL database.

The website checker collects the following information:

* Total response time
* HTTP status code, if the request completes successfully
* Whether the response body matches an optional regex check that can be passed as config to the program

## Prerequisites

* [Kafka instance](https://aiven.io/kafka)
 (I used Aiven's Apache Kafka 3.2.0)
 with predefined *Kafka topic* (define in settings.yaml).

 Kafka Topic can be created via Aiven UI or using kafka-python library.
* [PostgreSQL instance](https://aiven.io/postgresql)
 (I used Aiven's PostgreSQL 14.4)
* Python version 3.10.0
* Python kafka-python library (version 2.0.2)
* Python psycopg2 library (version 2.9.3)
* Python requests library (version 2.28.1)
* Python click library (version 8.1.3)
* Python dynaconf library (version 3.1.9)

## Development quick set up

Install all dependencies automatically from Pipfile

```
pipenv install
```

## Development step-by-step

* Pipenv virtual environment

    (and use python 3.10.0 version in pyenv)
```
 pyenv install 3.10.0
 echo "3.10.0" > .python-version

 Enable PIPENV_NO_INHERIT to avoid inheriting the environment from the parent process.
 export PIPENV_NO_INHERIT=true

 pipenv --python 3.10.0
 pipenv shell

 Install Python configuration management
 pipenv install dynaconf 

 Install linters
 pipenv install flake8 --dev 
 pipenv install pycodestyle --dev

 Install libs for interacting with Kafka and PostgreSQL
 pipenv install kafka-python
 pipenv install psycopg2

 Install requests library for Website Checker
 pipenv install requests 

 Install Click library for command line interface
 pipenv install click
 ```

 * Python configuration management dynaconf set up
 ```
   ~/devel/SRE-20221907-mrx88  webmon-dev !1 ?3  dynaconf init -f yaml
⚙️  Configuring your Dynaconf environment
------------------------------------------
🐍 The file `config.py` was generated.
  on your code now use `from config import settings`.
  (you must have `config` importable in your PYTHONPATH).

🎛️  settings.yaml created to hold your settings.

🔑 .secrets.yaml created to hold your secrets.

🙈 the .secrets.yaml is also included in `.gitignore` 
  beware to not push your secrets to a public repo 
  or use dynaconf builtin support for Vault Servers.

🎉 Dynaconf is configured! read more on https://dynaconf.com
   Use `dynaconf -i config.settings list` to see your settings
```

## Configuration

Program settings are defined in settings.yaml

```
<environment>:
  web_regex: '<regex>'
  enabled_web_urls: ['<url1>', '<url2>']
```

If web_regex is not defined, the program will not check the response body regex match and sets the variable value as None.

If site that is defined in enabled_web_wars does not exist (DNS resolution fails), the program will set the variable value as None.

Kafka settings:
```
<environment>:
  kafka_bootstrap_servers: '<bootstrap servers>'
  kafka_security_protocol: 'SSL'
  kafka_ssl_certfile: '<kafka.client.cert>'
  kafka_ssl_keyfile: '<kafka.client.key>'
  kafka_ssl_cafile: '<kafka.ca.cert>'
  kafka_topic: '<kafka topic>'
```

PostgreSQL settings:
```
<environment>:
  postgres_host: '<postgres host>'
  postgres_port: '<postgres port>'
  postgres_user: '<postgres user>'
  postgres_dbname: '<postgres db>'
  postgres_sslmode: 'verify-ca'
  postgres_ssl_cafile: '<postgres.ca.cert>'
```	

Store database password in .secrets.yaml.

*NOTE:* For production use any other sensitive values can be defined in .secrets.yaml
(postgres_host, postgres_user etc)
```
<environment>:
  postgres_password: '<postgres password>'
```
< environment > by default is `development` in dynaconf.

Verify that the settings are correct by running:

```
dynaconf -i config.settings list
```

## Usage

```
Usage: main.py [OPTIONS]

Options:
  --producer  Kafka mode: Producer
  --consumer  Kafka mode: Consumer
  --debug     Debug mode
  --help      Show this message and exit.
```

## Examples

### Producer

Example of monitoring websites and producing the results to a Kafka topic:

```
Configuration in use:
 ~/devel/SRE-20221907-mrx88  webmon-dev !6  dynaconf -i config.settings list 
Working in development environment 
WEB_REGEX<str> 'CSS1Compat'
ENABLED_WEB_URLS<list> ['https://www.google.ee/',
 'https://www.google.com/',
 'https://www.google.au/',
 'https://www.google.fi/',
 'https://aiven.io/']
KAFKA_BOOTSTRAP_SERVERS<str> 'kafka-6d026c2-matahh-d50f.aivencloud.com:14772'
KAFKA_SECURITY_PROTOCOL<str> 'SSL'
KAFKA_SSL_CERTFILE<str> '/home/matah/devel/SRE-20221907-mrx88/kafka.client.cert'
KAFKA_SSL_KEYFILE<str> '/home/matah/devel/SRE-20221907-mrx88/kafka.client.key'
KAFKA_SSL_CAFILE<str> '/home/matah/devel/SRE-20221907-mrx88/kafka.ca.cert'
KAFKA_TOPIC<str> 'WebMonitor'
POSTGRES_HOST<str> 'pg-35ba704d-matahh-d50f.aivencloud.com'
POSTGRES_PORT<int> 14770
POSTGRES_USER<str> 'avnadmin'
POSTGRES_DBNAME<str> 'defaultdb'
POSTGRES_SSLMODE<str> 'verify-ca'
POSTGRES_SSL_CAFILE<str> '/home/matah/devel/SRE-20221907-mrx88/postgres.ca.cert'
POSTGRES_PASSWORD<str> '<*>'

  
  ~/devel/SRE-20221907-mrx88  webmon-dev !4 ?2  python main.py --producer
2022-07-20 01:45:48,004 - INFO - Regex matched: CSS1Compat
2022-07-20 01:45:48,004 - INFO - Website https://www.google.ee code: 200
2022-07-20 01:45:48,004 - INFO - Website https://www.google.ee response time: 0.225304
2022-07-20 01:45:48,004 - INFO - Website https://www.google.ee response body match: True 
....
2022-07-20 01:45:48,085 - INFO - <BrokerConnection node_id=bootstrap-0 host=kafka-6d026c2-matahh-d50f.aivencloud.com:14772 <connecting> ...
2022-07-20 01:45:48,950 - INFO - <BrokerConnection node_id=1 host=20.107.220.153:14772 <handshake> [IPv4 ('20.107.220.153', 14772)]>: Connection complete.
2022-07-20 01:45:48,950 - INFO - <BrokerConnection node_id=bootstrap-0 host=kafka-6d026c2-matahh-d50f.aivencloud.com:14772 <connected> [IPv4 ('20.238.105.189', 14772)]>: Closing connection. 
2022-07-20 01:45:49,026 - INFO - <BrokerConnection node_id=1 host=20.107.220.153:14772 <connected> [IPv4 ('20.107.220.153', 14772)]>: Closing connection. 
...

```

### Consumer
Example of the consumer of the Kafka topic and event sending to PostgreSQL database

```
 python main.py --consumer
 ...
2022-07-20 12:06:16,365 - INFO - Message: {'url': 'https://www.google.ee/', 'status_code': 200, 'response_time': 0.354868, 'response_body_regex': True}
2022-07-20 12:06:17,235 - INFO - Event sent to Postgres: https://www.google.ee/ 200 0.354868 True
2022-07-20 12:06:17,647 - INFO - Message: {'url': 'https://www.google.com/', 'status_code': 200, 'response_time': 0.29367, 'response_body_regex': True}
2022-07-20 12:06:18,482 - INFO - Event sent to Postgres: https://www.google.com/ 200 0.29367 True
2022-07-20 12:06:21,831 - INFO - Message: {'url': 'https://www.google.au/', 'status_code': None, 'response_time': None, 'response_body_regex': None}
2022-07-20 12:06:22,766 - INFO - Event sent to Postgres: https://www.google.au/ None None None
2022-07-20 12:06:23,159 - INFO - Message: {'url': 'https://www.google.fi/', 'status_code': 200, 'response_time': 0.245511, 'response_body_regex': True}
2022-07-20 12:06:24,043 - INFO - Event sent to Postgres: https://www.google.fi/ 200 0.245511 True
2022-07-20 12:06:24,517 - INFO - Message: {'url': 'https://aiven.io/', 'status_code': 200, 'response_time': 0.282418, 'response_body_regex': False}
2022-07-20 12:06:25,345 - INFO - Event sent to Postgres: https://aiven.io/ 200 0.282418 False


Verify events in the PostgreSQL database:
pgcli -h pg-35ba704d-matahh-d50f.aivencloud.com -p 14770 -U avnadmin -d defaultdb

defaultdb> select * FROM events
+----+-------------------------+-------------+---------------+---------------------+
| id | url                     | status_code | response_time | response_body_regex |
|----+-------------------------+-------------+---------------+---------------------|
| 1  | https://www.google.ee/  | 200         | 0.354868      | True                |
| 2  | https://www.google.com/ | 200         | 0.29367       | True                |
| 3  | https://www.google.au/  | <null>      | <null>        | <null>              |
| 4  | https://www.google.fi/  | 200         | 0.245511      | True                |
| 5  | https://aiven.io/       | 200         | 0.282418      | False               |
+----+-------------------------+-------------+---------------+---------------------+
```

## Tests and Validation

Dynaconf allows the validation of settings parameters, we want to validate the settings before starting the program, therefore required validation checks
are defined in config.py.

*Tests* for program configuration are defined in dynaconf_validators.toml and can be tested using "dynaconf validate" command:

```
 ~/devel/SRE-20221907-mrx88  webmon-dev !3 ?1  dynaconf validate  

Validating 'enabled_web_urls' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validating 'kafka_bootstrap_servers' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validating 'kafka_security_protocol' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validating 'kafka_ssl_certfile' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validating 'kafka_ssl_keyfile' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validating 'kafka_ssl_cafile' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validating 'kafka_topic' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validating 'postgres_host' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validating 'postgres_port' with '{'must_exist': True, 'gte': 1, 'env': 'development'}'
Validating 'postgres_user' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validating 'postgres_password' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validating 'postgres_dbname' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validating 'postgres_sslmode' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validating 'postgres_ssl_cafile' with '{'must_exist': True, 'len_min': 1, 'env': 'development'}'
Validation success!
```
## Contributions

If you're interested in contributing to this project, you are free to do this! Read the
development section how to set up the development environment.

Feel free to reach out to me if you need help.

## Compatibility

Web Monitor is tested on Linux platform with python version 3.10.0. It is not tested on Windows, but the libraries used in this app are Windows-compatible.
If you're unable to run it on Windows, please file a bug.