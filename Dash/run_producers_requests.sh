#!/bin/bash

##############
#### run Kafka producers for the request stream
##############

python3 kafka_producer_requests.py 1 $1 &
ssh ubuntu@ip-10-0-0-12 python3 kafka_producer_requests.py 2 $1 &
ssh ubuntu@ip-10-0-0-9 python3 kafka_producer_requests.py 3 $1 &
ssh ubuntu@ip-10-0-0-5 python3 kafka_producer_requests.py 4 $1 &
