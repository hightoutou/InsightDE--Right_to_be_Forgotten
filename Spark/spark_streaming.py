"""
This is a script to use Spark Streaming to consume the sessions data stream and requests data stream from Kafka.
"""


from pyspark import SparkContext
from pyspark.streaming import StreamingContext, StreamingListener
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
import yaml
import redis
import psycopg2, datetime

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)
redis_server = 'ec2-52-34-94-103.us-west-2.compute.amazonaws.com'

# Create Spark Context
sc = SparkContext(appName="streaming_process")
sc.setLogLevel("Error")
# Create Spark Streaming Context
ssc = StreamingContext(sc, 5)
ssc.checkpoint('/home/ubuntu/checkpoint')

########### Recording Deletion Requests ##############

# Set the offset for Kafka stream
topic = "requests"
partition = 0
start = 0
topicpartion = TopicAndPartition(topic, partition)
fromoffset = {topicpartion: int(start)}

# Connect to Kafka
requestStream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list":config['broker_list']}, fromOffsets = fromoffset)
lines = requestStream.map(lambda x: x[1])

# Write users to Redis
def db_update(users):
    rdb = redis.StrictRedis(redis_server, port=6379, db=0, decode_responses=True)
    for user in users:
        rdb.append(user, 1)
    return users 

lines.count().pprint()
lines_update = lines.mapPartitions(db_update)
lines_update.pprint()

########### Processing Sessions Stream ###############

# Set the offset for Kafka stream
topic = "sessions"
partition = 0
start = 0
topicpartion = TopicAndPartition(topic, partition)
fromoffset = {topicpartion: int(start)}

# Connect to Kafka and split each message to list of strings
sessionStream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list":config['broker_list']}, fromOffsets = fromoffset)
lines = sessionStream.map(lambda x: x[1])
lines_list = lines.map(lambda line: line.split("\t"))  

# Count the number of sessions for each device in each batch
def deletion_filter(lines):
    rdb = redis.StrictRedis(redis_server, port=6379, db=0, decode_responses=True)    
    users_deletion = set()
    cursor = '0'
    while cursor != 0:
        cursor, keys = rdb.scan(cursor=cursor)
        #values = rdb.mget(*keys)
        users_deletion.update([user for user in keys if user is not None])
    print("Number of Deletion Requests: "+str(len(users_deletion)))     
    return [line for line in lines if line[0] not in users_deletion]

#device_counts_filter = lines_list.mapPartitions(deletion_filter).map(lambda l: l[4]).countByValue() 
#device_counts = lines_list.map(lambda l: l[4]).countByValue()

device_counts_filter = lines_list.mapPartitions(deletion_filter).map(lambda l: l[4]).map(lambda x: (x, 1)).reduceByKey(lambda x, y:x + y)
device_counts = lines_list.map(lambda l: l[4]).map(lambda x: (x, 1)).reduceByKey(lambda x, y:x + y)

# Count the cumulative number of sessions for each device
def update_count(new_count, count_sum):
    if not count_sum:
        count_sum = 0
    return sum(new_count) + count_sum

#device_counts_filter_sum = device_counts_filter.updateStateByKey(update_count)
#device_counts_filter_sum.pprint()
#device_counts_sum = device_counts.updateStateByKey(update_count)
#device_counts_sum.pprint()


def sendToSQL(rdd):
    connection = psycopg2.connect(host = 'ip-10-0-0-5', port = '5431', database = 'my_db', user = 'spark', password = 'spark')
    cursor = connection.cursor()
    timestamp = datetime.datetime.now()
    for line in rdd:
        query = 'INSERT INTO device_counts VALUES (%s, %s, %s)'
        data = (timestamp, line[0], line[1])
        cursor.execute(query, data)
    connection.commit()
    connection.close()

def sendToSQL_filter(rdd):
    connection = psycopg2.connect(host = 'ip-10-0-0-5', port = '5431', database = 'my_db', user = 'spark', password = 'spark')
    cursor = connection.cursor()
    timestamp = datetime.datetime.now()
    for line in rdd:
        query = 'INSERT INTO device_counts_filter VALUES (%s, %s, %s)'
        data = (timestamp, line[0], line[1])
        cursor.execute(query, data)
    connection.commit()
    connection.close()


device_counts_filter.foreachRDD(lambda rdd: rdd.foreachPartition(sendToSQL_filter))
device_counts.foreachRDD(lambda rdd: rdd.foreachPartition(sendToSQL))

device_counts_filter.pprint()
device_counts.pprint()



ssc.start()
ssc.awaitTermination()
