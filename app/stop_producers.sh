#!/bin/bash

##############
#### stop the kafka producers
##############


pkill -f kafka_producer_sessions.py
ssh ubuntu@ip-10-0-0-12 'pkill -f kafka_producer_sessions.py'
ssh ubuntu@ip-10-0-0-9 'pkill -f kafka_producer_sessions.py'
ssh ubuntu@ip-10-0-0-5 'pkill -f kafka_producer_sessions.py'

pkill -f kafka_producer_requests.py
ssh ubuntu@ip-10-0-0-12 'pkill -f kafka_producer_requests.py'
ssh ubuntu@ip-10-0-0-9 'pkill -f kafka_producer_requests.py'
ssh ubuntu@ip-10-0-0-5 'pkill -f kafka_producer_requests.py'
