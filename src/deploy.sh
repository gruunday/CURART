#!/bin/bash

set -e
cd /home/greenday/prod/
chmod +x configen.sh
./configen.sh
docker-compose up -d --build