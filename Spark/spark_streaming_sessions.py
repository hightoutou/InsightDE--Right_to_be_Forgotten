#!/usr/bin/env python3

#####################################################
###### This is a script to use Spark Streaming to consume the sessions data stream from Kafka.
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
sc = SparkContext(appName="consuming_sessions")
sc.setLogLevel("Error")
ssc = StreamingContext(sc, 2)

# Connect to Kafka and split each message to list of strings
topic = "sessions"
# sessionStream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list":config['broker_list'], 'auto.offset.reset':'smallest'})
sessionStream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list":config['broker_list']})

lines = sessionStream.map(lambda x: x[1])
lines_list = lines.map(lambda line: line[:-1].split("\t"))

########### Filtering sessions stream and calculate the metrics ###############
 
def deletion_filter_local(lines):
    """
    Fetch data from redis and Delete the messages from users with deletion requests
    """
    rdb = redis.StrictRedis(config['redis_server'], port=6379, db=0, decode_responses=True)    
    users_deletion = set()
    cursor = '0'
    while cursor != 0:
        cursor, keys = rdb.scan(cursor=cursor)
        #values = rdb.mget(*keys)
        users_deletion.update([user for user in keys if user is not None])
    print("Number of Deletion Requests: "+str(len(users_deletion)))     
    return [line for line in lines if line[0] not in users_deletion]

def deletion_filter_remote(lines):
    """
    Check the existence of user ids on Redis server and delete the messages from users with deletion requests
    """
    rdb = redis.StrictRedis(config['redis_server'], port=6379, db=0, decode_responses=True)
    return [line for line in lines if rdb.get(line[0]) is None]


# Calculate theaverage elapsed time for each (action_type, device_type)
lines_list_filter = lines_list.mapPartitions(deletion_filter_remote)
device_avg_time_filter = lines_list_filter.filter(lambda l: l[5].replace('.','',1).isdigit()) \
                                          .map(lambda l: ((l[2], l[4]), float(l[5]))) \
                                          .mapValues(lambda v: (v, 1)) \
                                          .reduceByKey(lambda a,b: (a[0]+b[0], a[1]+b[1])) \
                                          .mapValues(lambda v: v[0]/v[1])
lines_list.count().pprint()
#lines_list_filter.count().pprint()


########### Send Metrics to PostgreSQL  ###############

def sendToSQL_filter(rdd):
    """
    Write results to PostgreSQL
    """
    connection = psycopg2.connect(host = 'ip-10-0-0-5', port = '5431', database = 'my_db', user = config['postgres_user'], password = config['postgres_password'])
    cursor = connection.cursor()
    timestamp = datetime.datetime.now()
    for line in rdd:
        query = 'INSERT INTO device_avg_time_filter VALUES (%s, %s, %s, %s)'
        data = (timestamp, line[0][0], line[0][1], line[1])
        cursor.execute(query, data)
    connection.commit()
    connection.close()


device_avg_time_filter.foreachRDD(lambda rdd: rdd.foreachPartition(sendToSQL_filter))

ssc.start()
ssc.awaitTermination()
