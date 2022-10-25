#!/bin/sh

PATH="$PATH:$HOME/.local/bin"
cd $(dirname $0)
nohup anvil-app-server --app . &
sleep 50s
nohup chromium-browser --kiosk http://localhost:3030 &
