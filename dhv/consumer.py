from kafka import KafkaConsumer, KafkaProducer
from prometheus_client import Counter, Gauge, start_http_server
import json
import logging
import time
import signal
import sys

# ---------------- LOGGING SETUP ---------------- #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger("dhv-consumer")

# ---------------- PROMETHEUS METRICS ---------------- #

messages_processed_total = Counter(
    "messages_processed_total",
    "Total number of messages processed"
)

processing_errors_total = Counter(
    "processing_errors_total",
    "Total number of processing errors"
)

high_cpu_alerts_total = Counter(
    "high_cpu_alerts_total",
    "Total high CPU alerts triggered"
)

kafka_consumer_lag = Gauge(
    "kafka_consumer_lag",
    "Current Kafka consumer lag"
)

# ---------------- KAFKA SETUP ---------------- #

consumer = KafkaConsumer(
    "mock_data_homework",
    bootstrap_servers="kafka:9092",
    auto_offset_reset="earliest",
    group_id="dhv_group",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

dlq_producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

MAX_RETRIES = 3

# ---------------- METRICS SERVER ---------------- #

start_http_server(8000)
logger.info("Prometheus metrics server started on port 8000")

# ---------------- GRACEFUL SHUTDOWN ---------------- #

def shutdown_handler(sig, frame):
    logger.info("Graceful shutdown initiated")
    consumer.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

logger.info("DHV Consumer Started")

# ---------------- PROCESSING LOOP ---------------- #

for message in consumer:

    retries = 0

    while retries < MAX_RETRIES:
        try:
            data = message.value

            # Increment processed counter
            messages_processed_total.inc()

            # Example business rule
            cpu = data.get("cpu", 0)

            if cpu > 80:
                high_cpu_alerts_total.inc()
                logger.warning(json.dumps({
                    "event": "high_cpu_detected",
                    "data": data
                }))

            logger.info(json.dumps({
                "event": "message_processed",
                "data": data
            }))

            break  # success → exit retry loop

        except Exception as e:
            retries += 1
            processing_errors_total.inc()
            logger.error(f"Processing failed. Retry {retries}. Error: {str(e)}")
            time.sleep(2)

    if retries == MAX_RETRIES:
        logger.error("Max retries reached. Sending to DLQ.")
        dlq_producer.send("mock_data_homework_dlq", message.value)