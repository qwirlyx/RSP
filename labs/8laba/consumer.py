from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError
import json

INPUT_TOPIC = "input-topic"
DLQ_TOPIC = "dlq-topic"  # Dead Letter Queue

consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='my-consumer-group',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

consumer.subscribe([INPUT_TOPIC])

print("Консюмер запущен. Ожидание сообщений...")

for message in consumer:
    try:
        data = message.value
        text = data.get("text", "")
        
        # Пример обработки: считаем длину строки
        processed = {
            "original": text,
            "length": len(text),
            "upper": text.upper()
        }
        
        print(f"Обработано: {processed}")
        
        # Здесь можно отправить в другую тему или БД
        
    except Exception as e:
        print(f"Ошибка обработки сообщения: {e}")
        # Отправляем в DLQ
        producer.send(DLQ_TOPIC, {
            "error": str(e),
            "original_message": data,
            "offset": message.offset
        })
        print(f"Сообщение отправлено в DLQ: {DLQ_TOPIC}")