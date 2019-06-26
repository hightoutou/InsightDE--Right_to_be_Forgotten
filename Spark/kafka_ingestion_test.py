#!/usr/bin/env python3

################################
## This is a script to test the throughput of Kafka.
################################

from pyspark import SparkContext
from pyspark.streaming import StreamingContext, StreamingListener
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
import yaml
import redis
import psycopg2, datetime

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

# Create Spark Streaming Context
sc = SparkContext(appName="kafka_ingestion_test")
sc.setLogLevel("Error")
ssc = StreamingContext(sc, 1)

########### Count number of messages  ##############

# Connect to Kafka
topic = "sessions"
requestStream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list":config['broker_list'], 'auto.offset.reset':'smallest'})
requestStream.count().pprint()

ssc.start()
ssc.awaitTermination()
