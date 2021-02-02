#!/bin/bash

sudo systemctl stop monitoring.service
sudo systemctl start monitoring.service
sleep 1
sudo systemctl status monitoring.service

