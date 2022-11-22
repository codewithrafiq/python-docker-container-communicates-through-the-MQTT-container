import base64
from ctypes import cast
from traceback import print_tb
from paho.mqtt import client as mqtt_client
import json
import cv2
import logging
import logging
import logging.handlers
from decouple import config
from datetime import datetime


LOG_FILENAME = 'mlEngineEntry4.log'

logging.basicConfig(filename=LOG_FILENAME, filemode='a',
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# Creating an object
my_logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
my_logger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=20000000, backupCount=5)


my_logger.addHandler(handler)


class MQTTClient:
    def __init__(self):
        self.broker = config("BROKER_IP")
        self.port = config("BROKER_PORT", cast=int)
        self.topic = config("BROKER_TOPIC")
        self.client_id = config("BROKER_CLIENT_ID")

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        # Set Connecting Client ID
        client = mqtt_client.Client(client_id=self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port, keepalive=0)
        return client


    def send_message(self,message):
        client = self.connect_mqtt()
        try:
            client.publish(self.topic, json.dumps(message))
        except Exception as e:
            my_logger.debug(f"{e}")
        finally:
            client.disconnect()
    


# MQTTClient().send_message("Hi I am From ML Engine")