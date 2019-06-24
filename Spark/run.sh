##############
#### run the entire streaming process
##############

### clear Topics on kafka-cluster-1
ssh ubuntu@ip-10-0-0-6 /usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic requests
ssh ubuntu@ip-10-0-0-6 /usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic sessions

### clear Redis DB
ssh ubuntu@ip-10-0-0-9 redis-cli FLUSHDB

### clear PostgreSQL DB
ssh ubuntu@ip-10-0-0-5 'sudo PGPASSWORD="spark" psql -U spark -d my_db -w -h localhost -p 5431 -c "DELETE FROM device_counts_filter;"'
ssh ubuntu@ip-10-0-0-5 'sudo PGPASSWORD="spark" psql -U spark -d my_db -w -h localhost -p 5431 -c "DELETE FROM device_counts;"'

### run spark_streaming on spark-cluster-1
#/usr/local/spark/bin/spark-submit --master spark://10.0.0.8:7077 --jars spark-streaming-kafka-0-8-assembly_2.11-2.3.1.jar 'spark_streaming.py' &

### run kafka_producer on s3_reader
#ssh ubuntu@ip-10-0-0-12 'python3 kafka_producer.py'


