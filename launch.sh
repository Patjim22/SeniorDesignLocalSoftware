#!/bin/sh

anvil-app-server --app $(dirname $0) &
sleep 10s
chromium --kiosk http://localhost:3030
