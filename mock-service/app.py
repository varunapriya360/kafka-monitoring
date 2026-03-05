from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from kafka import KafkaProducer
import json
import random
import time
import threading

app = FastAPI()

# Prometheus instrumentation at module level (before app startup)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def generate_data():
    """Background thread to generate mock CPU/memory data and send to Kafka"""
    while True:
        try:
            data = {
                "cpu": round(random.uniform(10, 90), 2),
                "memory": round(random.uniform(20, 80), 2)
            }
            producer.send("mock_data_homework", data)
            print("Produced:", data)
        except Exception as e:
            print("Kafka send failed:", e)
        time.sleep(5)

@app.on_event("startup")
def startup_event():
    """Start the Kafka producer thread on app startup"""
    thread = threading.Thread(target=generate_data)
    thread.daemon = True  # ensures thread exits when app shuts down
    thread.start()

@app.get("/")
def read_root():
    return {"status": "Mock Service Running", "metrics": "/metrics"}