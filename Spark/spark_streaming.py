"""
This is a script to use Spark Streaming to consume the sessions data stream and requests data stream from Kafka.
"""


from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
import yaml

# Intialize parameters
users_deletion = set(['egmo531wtv', 'ks6hq5c4m4', 'pwituw3s7v', '87fdgatj2f', 'ldgl5jmdo2'])

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

# Create Spark Context
sc = SparkContext(appName="streaming_process")
user_deletion_broad = sc.broadcast(users_deletion)

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

#print(type(lines))



########### Processing Sessions Stream ###############

# Set the offset for Kafka stream
topic = "sessions"
partition = 0
start = 0
topicpartion = TopicAndPartition(topic, partition)
fromoffset = {topicpartion: int(start)}

# Connect to Kafka
sessionStream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list":config['broker_list']}, fromOffsets = fromoffset)
lines = sessionStream.map(lambda x: x[1])
#lines.pprint()

# Count the number of sessions for each device
lines_list = lines.map(lambda line: line.split("\t"))  

#device_counts = lines_list.map(lambda l: l[4]).countByValue()
#device_counts.pprint()

def update_count(new_count, count_sum):
    if not count_sum:
        count_sum = 0
    return sum(new_count) + count_sum

device_counts_filter =  lines_list.filter(lambda x: x[0] not in user_deletion_broad.value).map(lambda l: l[4]).countByValue()
device_counts_filter_sum = device_counts_filter.updateStateByKey(update_count)
device_counts_filter_sum.pprint()


ssc.start()
ssc.awaitTermination()
