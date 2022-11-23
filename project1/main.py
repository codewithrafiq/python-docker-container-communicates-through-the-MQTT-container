from fastapi import FastAPI
import redis
import json

app = FastAPI()

POOL = redis.ConnectionPool(host='0.0.0.0', port=6379, db=0)
REDIS_CLIENT = redis.Redis(connection_pool=POOL)


@app.get("/")
def home():
    REDIS_CLIENT.rpush('QUEUE', "Hello World")
    return{"message": "Hello message from Project1."}
