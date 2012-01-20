#!/bin/bash
# ./run.sh &
# Run all services as daemons.
# You can monitor a service from a different xterm, e.g.: 
# ps -ef | grep api.py

nohup python api.py &
nohup python webserver.py &
nohup nice python overmind.py &

