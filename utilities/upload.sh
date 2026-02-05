#!/bin/bash
set -euo pipefail

SOURCE_FOLDER="/Users/isaac/Developer/weatherbot"
DEST_USER="pi"
DEST_HOST="192.168.8.235"
DEST_DIR="/home/pi/weatherbot"
SSH_PASSWORD="raspberry"

echo "Syncing to $DEST_USER@$DEST_HOST:$DEST_DIR ..."

sshpass -p "$SSH_PASSWORD" rsync -az --delete \
    -e "ssh -o StrictHostKeyChecking=no" \
    "$SOURCE_FOLDER/" "$DEST_USER@$DEST_HOST:$DEST_DIR/"

echo "Done."
