#!/bin/bash

DEST_USER="pi"
DEST_HOST="192.168.8.235"
SSH_PASSWORD="raspberry"

REMOTE_COMMAND="pkill -f 'python3 weatherbot/main.py'"

echo "Logging into $DEST_USER@$DEST_HOST and executing: $REMOTE_COMMAND"

sshpass -p "$SSH_PASSWORD" ssh -o StrictHostKeyChecking=no "$DEST_USER@$DEST_HOST" "$REMOTE_COMMAND"

if [ $? -eq 0 ]; then
    echo "Remote command executed successfully."
else
    echo "Error: Remote command execution failed."
fi
