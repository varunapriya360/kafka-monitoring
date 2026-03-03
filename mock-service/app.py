from fastapi import FastAPI
from kafka import KafkaProducer
import json
import random
import time
import threading

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def generate_data():
    while True:
        data = {
            "cpu": round(random.uniform(10, 90), 2),
            "memory": round(random.uniform(20, 80), 2)
        }
        producer.send("mock_data_homework", data)
        print("Produced:", data)
        time.sleep(5)

@app.on_event("startup")
def start_producer():
    thread = threading.Thread(target=generate_data)
    thread.daemon = True
    thread.start()

@app.get("/")
def read_root():
    return {"status": "Mock Service Running"}

