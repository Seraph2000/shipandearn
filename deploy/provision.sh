#!/bin/bash
# Run once on a fresh Ubuntu 22.04 Droplet as root.
set -e

apt-get update && apt-get upgrade -y

# Docker
curl -fsSL https://get.docker.com | sh
apt-get install -y docker-compose-plugin

# App directory
mkdir -p /opt/shipandearn
cd /opt/shipandearn

echo ""
echo "Provision complete. Next steps:"
echo "  1. git clone <repo> /opt/shipandearn"
echo "  2. cp .env.example /opt/shipandearn/.env  (fill in all values)"
echo "  3. Run: sudo bash deploy/deploy.sh"
