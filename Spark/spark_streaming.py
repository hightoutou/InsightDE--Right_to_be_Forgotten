"""
This is a script to use Spark Streaming to consume the sessions data stream and requests data stream from Kafka.
"""


from pyspark import SparkContext
from pyspark.streaming import StreamingContext, StreamingListener
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
import yaml
import redis

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
lines.count().pprint()

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
        values = rdb.mget(*keys)
        users_deletion.update([value for value in values if value is not None])
    print(users_deletion)     
# Count the number of sessions for each device in each batch
    #users_deletion = set(['egmo531wtv', 'ks6hq5c4m4', 'pwituw3s7v', '87fdgatj2f', 'ldgl5jmdo2'])
    return [line for line in lines if line[0] not in users_deletion]

device_counts_filter = lines_list.mapPartitions(deletion_filter).map(lambda l: l[4]).countByValue() 

# Count the cumulative number of sessions for each device
def update_count(new_count, count_sum):
    if not count_sum:
        count_sum = 0
    return sum(new_count) + count_sum

device_counts_filter_sum = device_counts_filter.updateStateByKey(update_count)
device_counts_filter_sum.pprint()

ssc.start()
ssc.awaitTermination()
