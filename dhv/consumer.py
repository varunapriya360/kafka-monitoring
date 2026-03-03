from kafka import KafkaConsumer, KafkaProducer
import json
import logging
import time
import signal
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger("dhv-consumer")

consumer = KafkaConsumer(
    "mock_data_homework",
    bootstrap_servers="kafka:9092",
    auto_offset_reset="earliest",
    group_id="dhv_group",
    #group_id=None,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

dlq_producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

MAX_RETRIES = 3

def shutdown_handler(sig, frame):
    logger.info("Graceful shutdown initiated")
    consumer.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

logger.info("DHV Consumer Started")

for message in consumer:
    retries = 0
    while retries < MAX_RETRIES:
        try:
            data = message.value

            if data["cpu"] > 80:
                logger.warning(json.dumps({
                    "event": "high_cpu_detected",
                    "data": data
                }))

            logger.info(json.dumps({
                "event": "message_processed",
                "data": data
            }))

            break

        except Exception as e:
            retries += 1
            logger.error(f"Processing failed. Retry {retries}. Error: {str(e)}")
            time.sleep(2)

    if retries == MAX_RETRIES:
        logger.error("Max retries reached. Sending to DLQ.")
        dlq_producer.send("mock_data_homework_dlq", message.value)


