#!/bin/bash

##############
#### run Kafka producers
##############


python3 kafka_producer_sessions.py 1 &
python3 kafka_producer_sessions.py 2 &
python3 kafka_producer_sessions.py 3 &
ssh ubuntu@ip-10-0-0-12 python3 kafka_producer_sessions.py 4 &
ssh ubuntu@ip-10-0-0-12 python3 kafka_producer_sessions.py 5 &
ssh ubuntu@ip-10-0-0-12 python3 kafka_producer_sessions.py 6 &
ssh ubuntu@ip-10-0-0-9 python3 kafka_producer_sessions.py 7 &
ssh ubuntu@ip-10-0-0-9 python3 kafka_producer_sessions.py 8 &
ssh ubuntu@ip-10-0-0-9 python3 kafka_producer_sessions.py 9 &
ssh ubuntu@ip-10-0-0-5 python3 kafka_producer_sessions.py 10 &
ssh ubuntu@ip-10-0-0-5 python3 kafka_producer_sessions.py 11 &
ssh ubuntu@ip-10-0-0-5 python3 kafka_producer_sessions.py 12 &

