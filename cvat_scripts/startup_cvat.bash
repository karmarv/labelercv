export CVAT_VERSION="v2.9.1"
export CVAT_HOST="$(hostname).local"
cd ../cvat
# Startup docker containers
docker compose -f docker-compose.local.yml -f components/serverless/docker-compose.serverless.yml up -d

