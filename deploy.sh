#!/bin/bash
set -e

# Add Helm repos
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Deploy Zookeeper
helm upgrade --install zookeeper bitnami/zookeeper --set replicaCount=1

# Deploy Kafka (local only, no external access)
helm upgrade --install kafka bitnami/kafka \
  --set replicaCount=1 \
  --set zookeeper.enabled=false \
  --set externalAccess.enabled=false

# Deploy Prometheus (Grafana disabled here, install separately)
helm upgrade --install prometheus bitnami/kube-prometheus --set grafana.enabled=false

# Deploy Grafana
helm upgrade --install grafana bitnami/grafana \
  --set adminUser=admin \
  --set adminPassword=admin123 \
  --set service.type=NodePort

# Start mock-service
cd mock-service
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m uvicorn app:app --host 0.0.0.0 --port 5000 &

# Start DHV consumer
cd ../dhv
python3 -m pip install -r requirements.txt
python3 consumer.py &

echo "✅ Deployment complete! Grafana NodePort URL: http://localhost:<nodeport>"