from kafka import KafkaProducer, KafkaConsumer
import json

INPUT_TOPIC = "input-topic"
OUTPUT_TOPIC = "processed-topic"

consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Stream Processor запущен...")

for message in consumer:
    data = message.value
    text = data.get("text", "")
    
    # Преобразование
    transformed = {
        "original_text": text,
        "length": len(text),
        "reversed": text[::-1],
        "is_long": len(text) > 20
    }
    
    producer.send(OUTPUT_TOPIC, transformed)
    print(f"Отправлено в {OUTPUT_TOPIC}: {transformed}")