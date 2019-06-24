#################
# run spark in backend
#################


### run spark_streaming on spark-cluster-1
/usr/local/spark/bin/spark-submit --master spark://10.0.0.8:7077 --jars spark-streaming-kafka-0-8-assembly_2.11-2.3.1.jar 'spark_streaming.py' &
