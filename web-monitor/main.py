#!/usr/bin/env python
import psycopg2
import kafka
import requests
import logging
import re
import click
from config import settings
import json


def webchecker(url):
    """Check website status for collecting website
    status code, response time and response body

    Args:
        url (string): Website URL

    Returns:
        status_code (string): HTTP request status code
        response_time (string): Response time in seconds
        response_body_regex (boolean): Response body regex match status
    """
    try:
        req = requests.get(url)
        status_code = req.status_code
        response_time = req.elapsed.total_seconds()
        response_body = req.content.decode('latin-1')

        logging.info(f"Website {url} code: {status_code}")
        logging.info(f"Website {url} response time: {response_time}")

        # Check if response_body matches the expected regex
        # defined in settings.yml
        try:
            response_body_regex = re.search(settings.web_regex, response_body)
            logging.debug(f"Website {url} regex status: {response_body_regex}")
            return status_code, response_time, response_body_regex is not None

        except AttributeError:
            return status_code, response_time, None

    except requests.exceptions.RequestException as e:
        logging.error(e)
        return None, None, None


def kafka_producer(topic, enabled_web_urls):
    """Send messages to Kafka topic

    Args:
        topic (string): Kafka topic name
        enabled_web_urls (list): list of enabled website URLs
    """
    try:

        producer = kafka.KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            security_protocol=settings.kafka_security_protocol,
            ssl_certfile=settings.kafka_ssl_certfile,
            ssl_keyfile=settings.kafka_ssl_keyfile,
            ssl_cafile=settings.kafka_ssl_cafile,
            value_serializer=lambda m: json.dumps(m).encode('ascii')
        )
        # Monitor website X status
        for url in enabled_web_urls:
            status_code, response_time, response_body_regex = webchecker(
                url)
            message = {
                'url': url,
                'status_code': status_code,
                'response_time': response_time,
                'response_body_regex': response_body_regex
            }
            producer.send(topic, message)
            producer.flush()
    except kafka.errors.NoBrokersAvailable:
        logging.error("Kafka NoBrokersAvailable")
    except kafka.errors.KafkaError as e:
        logging.error(f"KafkaError: {e}")
    except Exception as e:
        logging.error(f"Kafka producer function error: {e}")


def consume_events(topic):
    """Consume messages from Kafka topic
    and send events to Postgres database

    Args:
        topic (string): Kafka topic name
    """
    try:
        pgconn = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database=settings.postgres_dbname,
            sslmode=settings.postgres_sslmode,
            sslrootcert=settings.postgres_ssl_cafile
        )

        events_table_sql = """
                CREATE TABLE IF NOT EXISTS events (
                    id SERIAL PRIMARY KEY,
                    url TEXT,
                    status_code INTEGER,
                    response_time REAL,
                    response_body_regex BOOLEAN
                )
            """
        # Create Postgres events table if not exists
        with pgconn.cursor() as cur_table:
            cur_table.execute(events_table_sql)
            pgconn.commit()
            cur_table.close()

        consumer = kafka.KafkaConsumer(
            topic,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            security_protocol=settings.kafka_security_protocol,
            ssl_certfile=settings.kafka_ssl_certfile,
            ssl_keyfile=settings.kafka_ssl_keyfile,
            ssl_cafile=settings.kafka_ssl_cafile,
            value_deserializer=lambda m: json.loads(m.decode('ascii'))
        )

        for message in consumer:
            logging.debug(f"Message: {message.value}")

            url = message.value['url']
            status_code = message.value['status_code']
            response_time = message.value['response_time']
            response_body_regex = message.value['response_body_regex']

            cur = pgconn.cursor()
            cur.execute(
                "INSERT INTO events (url, status_code, response_time, response_body_regex) VALUES (%s, %s, %s, %s)",
                (url, status_code, response_time, response_body_regex)
            )
            logging.info(
                f"Event sent to Postgres: {url} {status_code} {response_time} {response_body_regex}")
            pgconn.commit()
            cur.close()
        pgconn.close()
        consumer.close()

    except kafka.errors.NoBrokersAvailable:
        logging.error("Kafka NoBrokersAvailable")
    except kafka.errors.KafkaError as e:
        logging.error(f"KafkaError: {e}")
    except (Exception, psycopg2.Error) as error:
        logging.error(error)


@click.command()
@click.option('--producer', is_flag=True, help='Kafka mode: Producer')
@click.option('--consumer', is_flag=True, help='Kafka mode: Consumer')
@click.option('--debug', default=False, is_flag=True, help='Debug mode')
def main(producer, consumer, debug):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        topic = settings.kafka_topic
        enabled_web_urls = settings.enabled_web_urls
        if producer:
            producer = kafka_producer(topic, enabled_web_urls)

        elif consumer:
            # Kafka Consumer: Read website X status from Kafka topic
            # display it on the screen and send events to the Postgres database
            consume_events(topic)

    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
