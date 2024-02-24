#!/bin/bash

export CVAT_VERSION="v2.11.0"
export CVAT_HOST="$(hostname)"
cd ../cvat
# Shutdown docker containers
docker compose -f docker-compose.local.yml -f components/serverless/docker-compose.serverless.yml down

# Check the arguments for cleanup
if [[ "$#" -eq  "0" ]] ; then
    echo "No arguments supplied"
else
    if [[ "$1" == delete ]] ; then
        echo "Delete the container and volumens" 
        docker compose -f docker-compose.local.yml -f components/serverless/docker-compose.serverless.yml  down --rmi all --volumes --remove-orphans
        rm -rf ~/dev/cvat_data/*
    fi
fi