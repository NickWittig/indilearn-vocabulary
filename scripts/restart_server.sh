#!/bin/bash
# Load the .env file
set -a
. ./.env
set +a

# Stop old containers

if [ "$1" == "delete-volumes" ]; then
  docker-compose down -v # also delete volumes => RESET DB => CAREFUL!!!
else
  docker-compose down
fi

# Login to Docker
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin

# Pull new Image
docker pull ghcr.io/$GITHUB_PACKAGE:latest
docker pull ghcr.io/$GITHUB_PACKAGE2:latest

# Start new containers
docker-compose up -d --build --force-recreate