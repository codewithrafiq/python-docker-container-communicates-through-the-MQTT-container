from audioop import add
from fastapi import FastAPI
from pymongo import MongoClient
from project.subscriber import MQTTClient
from project import settings
app = FastAPI()



client = MongoClient(settings.mongodb_uri, settings.port)
db = client['altersense']
token = ''


from project import routes
app.include_router(routes.router)


mqtt_client = MQTTClient()
mqtt_client.run()