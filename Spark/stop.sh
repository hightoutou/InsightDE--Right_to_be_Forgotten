##############
#### stop the entire streaming process
##############

### clear Topics on kafka-cluster-1
#ssh ubuntu@ip-10-0-0-6 /usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic requests
#ssh ubuntu@ip-10-0-0-6 /usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic sessions

### clear Redis DB
#ssh ubuntu@ip-10-0-0-9 redis-cli FLUSHDB

### stop kafka_producer on s3_reader
ssh ubuntu@ip-10-0-0-12 'pkill -f kafka_producer.py'

### stop spark_streaming on spark-cluster-1
ssh ubuntu@ip-10-0-0-8 'pkill -f spark_streaming.py'


