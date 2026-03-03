from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "mock_data_homework",
    bootstrap_servers="kafka:9092",
    auto_offset_reset="earliest",
    #group_id="dhv_group",
    group_id=None,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("DHV Consumer Started...")

for message in consumer:
    print("Consumed:", message.value)