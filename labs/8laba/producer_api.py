from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer
import json
import os

app = FastAPI(title="Kafka Producer API")

class Message(BaseModel):
    text: str

# Подключение к Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',
    retries=5
)

TOPIC = "input-topic"

@app.post("/send")
async def send_message(msg: Message):
    try:
        future = producer.send(TOPIC, {"text": msg.text, "source": "http-api"})
        future.get(timeout=10)  # Ждём подтверждения
        return {"status": "sent", "message": msg.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "Kafka Producer API работает. Используй POST /send"}