#!/bin/bash

#################
# run spark in backend
#################


### run spark_streaming on spark-cluster-1
/usr/local/spark/bin/spark-submit --master spark://10.0.0.8:7077 --conf spark.cores.max=3 --jars spark-streaming-kafka-0-8-assembly_2.11-2.3.1.jar 'spark_streaming_requests.py' &
/usr/local/spark/bin/spark-submit --master spark://10.0.0.8:7077 --conf spark.cores.max=15 --jars spark-streaming-kafka-0-8-assembly_2.11-2.3.1.jar 'spark_streaming_sessions.py' &

