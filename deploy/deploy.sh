#!/bin/bash
# Run on the Droplet to deploy a new version.
set -e

cd /opt/shipandearn

# Pull as the user who ran `sudo`, not root — the GitHub deploy key
# lives in that user's ~/.ssh, and root has no access to GitHub.
sudo -u "${SUDO_USER:-$(whoami)}" git pull --ff-only origin main
docker build -t shipandearn:latest .
docker compose -f docker-compose.prod.yml up -d --remove-orphans

echo "Deploy complete."
