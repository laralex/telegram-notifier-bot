#!/bin/bash
set -e

IN_FILE="systemctl_template.service"
OUT_FILE="systemctl.service"

# Get the absolute path of the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Replace the placeholder in the service file
sed "s|REPLACE_THIS_PATH|$SCRIPT_DIR|g" "$SCRIPT_DIR/$IN_FILE" > "$SCRIPT_DIR/$OUT_FILE"

sudo cp systemctl.service /etc/systemd/system/laralex_notifier_bot.service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl stop laralex_notifier_bot
sudo systemctl enable laralex_notifier_bot
sudo systemctl start laralex_notifier_bot