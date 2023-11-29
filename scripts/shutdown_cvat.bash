export CVAT_HOST=127.0.0.1
cd ../cvat
# Shutdown docker containers
docker compose -f docker-compose.local.yml -f components/serverless/docker-compose.serverless.yml down