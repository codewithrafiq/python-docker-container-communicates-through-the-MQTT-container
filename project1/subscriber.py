from datetime import datetime
from decouple import config
import paho.mqtt.client as mqtt
import cv2
import json
import base64

from pymongo import MongoClient

from project import settings

client = MongoClient(settings.mongodb_uri, settings.port)
db = client['altersense']


class MQTTClient:
    def __init__(self):
        self.broker = config('MQTT_BROKER')
        self.port = config('MQTT_PORT', cast=int)
        self.worker_count_ml_topic = config('MQTT_TOPIC')
        self.client_id = config('MQTT_CLIENT_ID')

    def run(self):
        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))

            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            # client.subscribe(self.topic)
            client.subscribe([
                (self.worker_count_ml_topic, 0),
            ])

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            if msg.topic == self.worker_count_ml_topic:
                data = json.loads(msg.payload.decode('utf-8'))
                print(data)
                if data["enter"] != 0 or data["exit"] != 0:
                    d = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")

                    data["datetime"] = {
                        "year": d.date().year,
                        "month": d.date().month,
                        "day": d.date().day,
                        "hour": d.time().hour,
                        "minute": d.time().minute,
                        "second": d.time().second
                    }
                    data["cam_id"] = data["cam_id"]
                    try:
                        floor = db.floor_camera_info.find_one(
                            {"cam_id": data["cam_id"]})
                        print("floor--->", floor)
                        data["floor"] = floor["floor"]
                    except Exception as e:
                        print(str(e))
                    db.worker_count.insert_one(data)
                with open('worker_count_backend.json', 'a') as f:
                    f.write(msg.payload.decode('utf-8')+"\n")

        client = mqtt.Client(client_id=self.client_id)
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(self.broker, self.port, 60)

        client.loop_start()
