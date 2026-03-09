Event-Driven System Monitoring Pipeline
A cloud-native event-driven system that simulates infrastructure metrics, streams them through Kafka, processes them via a consumer service, and exposes observability using Prometheus and Grafana on Kubernetes.
This project demonstrates a real microservices architecture with message streaming, containerization, Kubernetes orchestration, and monitoring.

Architecture Overview
The system consists of the following components:
Mock Producer Service
Generates simulated CPU and memory metrics.
Publishes messages to a Kafka topic every few seconds.
Apache Kafka
Acts as the event streaming platform.
Handles message ingestion from producers and delivery to consumers.
Consumer Service
Reads messages from the Kafka topic.
Processes and logs incoming metric events.
Prometheus
Scrapes application metrics from services.
Grafana
Visualizes metrics through dashboards.
Kubernetes
Manages container deployment, scaling, and networking.

System Flow
Mock service generates CPU and memory usage data.
Data is published to a Kafka topic.
Consumer service reads events from Kafka.
Prometheus scrapes service metrics.
Grafana visualizes system metrics through dashboards.

Tech Stack
Python (FastAPI) – API service
Apache Kafka – Event streaming platform
Docker – Containerization
Kubernetes – Container orchestration
Prometheus – Metrics collection
Grafana – Monitoring dashboards

Project Structure


Mock Service
The mock service simulates system metrics and sends them to Kafka.
Metrics generated:
CPU Usage
Memory Usage
Sample message:
{
  "cpu": 54.21,
  "memory": 63.47
}

Messages are sent to the Kafka topic:
mock_data_homework


FastAPI Service
The service exposes two endpoints.
Root Endpoint
GET /

Response
{
 "status": "Mock Service Running"
}

Metrics Endpoint
GET /metrics

This endpoint exposes Prometheus metrics.

Kubernetes Deployment
The service runs inside a Kubernetes cluster.
Deployment Features
Containerized FastAPI application
Resource limits and requests
Liveness probe
Readiness probe
Environment variables via ConfigMap

Kafka Integration
Kafka is used as the event streaming platform.
Producer configuration:
bootstrap_servers="kafka:9092"

Topic used:
mock_data_homework

Data is generated every 5 seconds and published to the topic.

Monitoring Setup
Prometheus
Prometheus scrapes metrics exposed by the FastAPI service.
Metrics endpoint:
/metrics

Example metric:
http_requests_total

Prometheus collects metrics from the Kubernetes service endpoints.

Grafana
Grafana is used to visualize metrics.
Example dashboards include:
Request rate
Service health
CPU usage simulation
Memory usage simulation
Grafana connects to Prometheus as a data source.

Running the Project
1 Clone the Repository
git clone <repo-url>
cd mock-service


2 Build Docker Image
docker build -t varunapriya/mock-service:latest .


3 Push Image
docker push varunapriya/mock-service:latest


4 Deploy to Kubernetes
kubectl apply -f deployment.yaml


5 Verify Pods
kubectl get pods


6 Check Logs
kubectl logs <pod-name>


Troubleshooting
Issue 1 – Old Docker Image Being Used
Problem
Kubernetes continued using an older image even after code changes.
Cause
Docker image was rebuilt locally but not pushed to DockerHub.
Solution
Rebuild and push the image.
docker build --no-cache -t varunapriya/mock-service:latest .
docker push varunapriya/mock-service:latest
kubectl rollout restart deployment mock-service


Issue 2 – CrashLoopBackOff
Problem
The application failed during startup.
Error:
RuntimeError: Cannot add middleware after an application has started

Cause
Prometheus instrumentation middleware was added inside the startup event.
Solution
Move instrumentation outside the startup function.
Correct implementation:
Instrumentator().instrument(app).expose(app)


Issue 3 – Deployment Pulling Wrong Image
Problem
Deployment referenced an incorrect or outdated image.
Solution
Verify the image in the deployment configuration.
kubectl get deployment mock-service -o yaml | grep image


Observability
The project demonstrates how to monitor containerized applications using:
Prometheus metrics scraping
Grafana dashboards
Kubernetes health probes




