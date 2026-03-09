Event-Driven Monitoring Pipeline on Kubernetes
A lightweight event-driven monitoring pipeline built using FastAPI, Apache Kafka, Prometheus, and Grafana, deployed on Kubernetes.
This project simulates infrastructure metrics (CPU & memory usage), streams them through Kafka, processes them with a consumer service, and exposes metrics for Prometheus scraping and Grafana visualization.
The goal of this project is to demonstrate how event-driven microservices and observability tools integrate in a Kubernetes environment.

Architecture Overview
           +------------------+
            |  Mock Producer   |
            |  (FastAPI App)   |
            +--------+---------+
                     |
                     | Kafka Events
                     v
               +------------+
               |   Kafka    |
               |  Topic     |
               +-----+------+
                     |
                     v
             +---------------+
             | Consumer App  |
             | (DHV Service) |
             +-------+-------+
                     |
                     | Metrics
                     v
             +---------------+
             |  Prometheus   |
             |  Scrapes Data |
             +-------+-------+
                     |
                     v
                +---------+
                | Grafana |
                |Dashboard|
                +---------+


Tech Stack
FastAPI – mock producer service
Apache Kafka – event streaming
Python Kafka Client – producer & consumer
Prometheus – metrics scraping
Grafana – monitoring dashboards
Docker – containerization
Kubernetes – orchestration

Project Components
1️⃣ Mock Producer Service
A FastAPI application that generates synthetic system metrics.
Every few seconds it publishes:
{
  "cpu": 64.3,
  "memory": 45.7
}

to a Kafka topic.
It also exposes a /metrics endpoint for Prometheus.

2️⃣ Apache Kafka
Kafka acts as the event streaming platform.
The producer sends data to the topic:
mock_data_homework

Kafka ensures:
decoupled services
reliable message delivery
scalable streaming pipeline

3️⃣ Consumer Service
The consumer reads messages from Kafka and processes them.
This simulates a downstream processing system that could:
analyze metrics
trigger alerts
store metrics

4️⃣ Prometheus
Prometheus periodically scrapes the producer’s:
/metrics

endpoint.
These metrics include:
HTTP request metrics
application performance metrics
custom service metrics

5️⃣ Grafana
Grafana connects to Prometheus and visualizes the metrics through dashboards.
Example dashboards include:
CPU usage
memory usage
request latency
service health

Kubernetes Deployment
All services are deployed inside a Kubernetes cluster.

Kubernetes manages:
container orchestration
pod lifecycle
health checks
resource allocation

Example configuration includes:
readiness probes
liveness probes
resource limits
service networking

Observability Flow
FastAPI Service
      │
      │ exposes
      ▼
   /metrics
      │
      ▼
Prometheus Scrapes Metrics
      │
      ▼
Grafana Visualizes Data


Running the Project
1️⃣ Build the Docker Image
docker build -t mock-service .


2️⃣ Push Image to DockerHub
docker tag mock-service varunapriya/mock-service:latest
docker push varunapriya/mock-service:latest


3️⃣ Deploy to Kubernetes
kubectl apply -f deployment.yaml


4️⃣ Verify Pods
kubectl get pods


Kafka UI
Kafka UI is used to inspect topics and message streams.
Example:
topic: mock_data_homework
message stream of CPU and memory data
(Add screenshot here)

Prometheus Targets
Prometheus automatically scrapes the mock service metrics.
Example target:
mock-service:5000/metrics

(Added screenshot in /images folder)

Grafana Dashboard
Grafana visualizes metrics collected by Prometheus.
Example panels:
CPU usage
memory usage
request latency
(Added screenshot in /images folder)

Troubleshooting
Prometheus Not Scraping Metrics
Issue:
HTTP 404 on /metrics

Cause:
The FastAPI service did not expose the metrics endpoint.
Solution:
Added:
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)


Kubernetes Using Old Docker Image

Issue:
Pod continued using outdated image.

Cause:
Kubernetes cached the previous image.

Solution:
Rebuilt and pushed a new image, then restarted the deployment.
docker build -t varunapriya/mock-service:latest .
docker push varunapriya/mock-service:latest
kubectl rollout restart deployment mock-service


CrashLoopBackOff After Metrics Integration

Issue:
Application failed during startup.

Error:
RuntimeError: Cannot add middleware after an application has started

Cause:
Prometheus instrumentation was added during the FastAPI startup event.

Solution:
Move instrumentation outside the startup function so it runs before the application starts.

Future Improvements
Potential enhancements:
Kafka consumer autoscaling
Prometheus alerting rules
Kubernetes Horizontal Pod Autoscaler
Persistent storage for metrics
distributed tracing with Jaeger


