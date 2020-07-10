# pylint: disable=broad-except
"""listen for messages on message queue"""
import os
import json
from azure.servicebus import ServiceBusClient
from src.apps.slack.event_handler import resolve_event
from src.init_logger import InitLogger
from src.apps.const import APP_VERSION, SLACK_WORKSPACE

logger = InitLogger.instance(SLACK_WORKSPACE, os.environ["APP_ENV"])
logger.warn(f'app version: {APP_VERSION}')

connstr = os.environ['SERVICE_BUS_CONN_STR']
queue_name = os.environ['SERVICE_BUS_QUEUE_NAME']

with ServiceBusClient.from_connection_string(connstr) as client:
    with client.get_queue_receiver(queue_name, idle_timeout=None) as receiver:
        logger.info('listening for events')
        for msg in receiver:
            try:
                data = json.loads(str(msg))
                resolve_event(data)
                msg.complete()
            except Exception as error:
                msg.dead_letter()
                logger.error(error)
