#!/usr/bin/python3.6

#########################
# pyhton3 file kafka_producer.py
# read data from s3 and send it to kafka-cluster
#########################


from kafka import KafkaProducer
from smart_open import smart_open
import yaml
from random import randint
import sys
import json
from multiprocessing.pool import ThreadPool as Pool
        
# read config file
with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

def single_producer(i):
    """
    Kafka producer read from a single file
    """
    fpath = config['s3_fpath_session'] + '_' + str(i) + '.csv'
    producer = KafkaProducer(bootstrap_servers = config['bootstrap_servers_address'])   
    for msg in smart_open(fpath, 'rb'):
        # send the sessions
        producer.send('sessions', msg)
        producer.flush()        


pool_size = int(sys.argv[2])-int(sys.argv[1])+1

pool = Pool(pool_size)
for i in range(int(sys.argv[1]), int(sys.argv[2])+1):
    pool.apply_async(single_producer, (i,))
pool.close()
pool.join()



