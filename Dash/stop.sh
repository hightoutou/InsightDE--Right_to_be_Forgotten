##############
#### stop the entire streaming process
##############

### stop kafka_producer on s3_reader
ssh ubuntu@ip-10-0-0-12 'pkill -f kafka_producer.py'

### stop spark_streaming
#ssh ubuntu@ip-10-0-0-8 'pkill -f spark_streaming.py'

### clear Topics on kafka-cluster-1
#ssh ubuntu@ip-10-0-0-6 /usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic requests
#ssh ubuntu@ip-10-0-0-6 /usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic sessions

### run spark_streaming on spark-cluster-1
#ssh ubuntu@ip-10-0-0-8 /usr/local/spark/bin/spark-submit --master spark://10.0.0.8:7077 --jars spark-streaming-kafka-0-8-assembly_2.11-2.3.1.jar 'spark_streaming.py' &
