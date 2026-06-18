#!/bin/bash
# Run on the Droplet to deploy a new version.
set -e

cd /opt/shipandearn

git pull origin main
docker build -t shipandearn:latest .
docker compose -f docker-compose.prod.yml up -d --remove-orphans

echo "Deploy complete."
