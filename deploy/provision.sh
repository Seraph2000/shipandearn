#!/bin/bash
# Run once on a fresh Ubuntu 22.04 Droplet as root.
set -e

apt-get update && apt-get upgrade -y

# Docker
curl -fsSL https://get.docker.com | sh
apt-get install -y docker-compose-plugin

# App directory
mkdir -p /opt/earnstack
cd /opt/earnstack

echo ""
echo "Provision complete. Next steps:"
echo "  1. git clone <repo> /opt/earnstack"
echo "  2. cp .env.example /opt/earnstack/.env  (fill in all values)"
echo "  3. Run: flask db init && flask db migrate -m 'initial'  (first deploy only)"
echo "  4. Run: ./deploy/deploy.sh"
