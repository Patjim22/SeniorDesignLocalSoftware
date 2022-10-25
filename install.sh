#!/bin/sh

if ! which java; then
	sudo apt install openjdk-11-jdk
fi

if ! which anvil-app-server; then
	sudo apt install libpq-dev
	pip install anvil-app-server
	PATH+=":$HOME/.local/bin"
	anvil-app-server
fi

sudo mv $(dirname $0)/makerspace.service /lib/systemd/system/makerspace.service
sudo systemctl enable makerspace.service
sudo systemctl start makerspace.service
