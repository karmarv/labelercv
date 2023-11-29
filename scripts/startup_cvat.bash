export CVAT_HOST=127.0.0.1
cd ../cvat
# Startup docker containers
docker compose -f docker-compose.local.yml -f components/serverless/docker-compose.serverless.yml up -d