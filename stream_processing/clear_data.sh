#!/bin/bash

##############
#### Clear Kafka topics, Redis database, and PostgreSQL database 
##############

### clear Topics on kafka-cluster-1
ssh ubuntu@ip-10-0-0-6 /usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic requests
ssh ubuntu@ip-10-0-0-6 /usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic sessions
ssh ubuntu@ip-10-0-0-6 /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 4 --topic requests
ssh ubuntu@ip-10-0-0-6 /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 12 --topic sessions

### clear Redis DB
ssh ubuntu@ip-10-0-0-9 redis-cli FLUSHDB

### clear PostgreSQL DB
ssh ubuntu@ip-10-0-0-5 'sudo PGPASSWORD="spark" psql -U spark -d my_db -w -h localhost -p 5431 -c "DELETE FROM device_avg_time_filter;"'



