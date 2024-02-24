export CVAT_VERSION="v2.11.0"
export CVAT_HOST="$(hostname)"
cd ../cvat
# Startup docker containers
docker compose -f docker-compose.local.yml -f components/serverless/docker-compose.serverless.yml up -d

