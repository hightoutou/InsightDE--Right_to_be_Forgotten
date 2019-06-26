#!/usr/bin/env python3

#####################################################
###### This is a script to use Spark Streaming to consume the requests data stream from Kafka.
#####################################################

from pyspark import SparkContext
from pyspark.streaming import StreamingContext, StreamingListener
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
import yaml
import redis
import psycopg2, datetime

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

# Create Spark Streaming Context
sc = SparkContext(appName="consuming_requests")
sc.setLogLevel("Error")
ssc = StreamingContext(sc, 1)

# Connect to Kafka
topic = "requests"
requestStream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list":config['broker_list'], 'auto.offset.reset':'smallest'})
lines = requestStream.map(lambda x: x[1])

########### Recording Deletion Requests ##############

def db_update(users):
    """
    Write users with deletion requests to Redis
    """
    rdb = redis.StrictRedis(config['redis_server'], port=6379, db=0, decode_responses=True)
    for user in users:
        rdb.append(user, 1)
    return users

lines.count().pprint()
lines_update = lines.mapPartitions(db_update)
lines_update.pprint()

ssc.start()
ssc.awaitTermination()
