from fastapi import FastAPI
import redis


app = FastAPI()
# REDIS_CLIENT = redis.Redis(host="0.0.0.0",port=6379,db=0)


@app.get("/")
def home():
    # data = REDIS_CLIENT.rpop('QUEUE')
    # print("REDIS_CLIENT--->",data)
    return{"message": "Hello message from Project1."}
