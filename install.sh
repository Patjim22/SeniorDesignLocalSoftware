#!/bin/sh

sudo mv $(dirname $0)/makerspace.service /lib/systemd/system/makerspace.service
sudo systemctl enable makerspace.service
sudo systemctl start makerspace.service
