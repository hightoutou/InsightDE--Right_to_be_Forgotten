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
import time
        
# read config file
with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

fpath = config['s3_fpath_user'] + '_' + str(sys.argv[1]) + '.csv'
producer = KafkaProducer(bootstrap_servers = config['bootstrap_servers_address'])   

dt = 4/float(sys.argv[2]) - 1/600
for user in smart_open(fpath, 'rb'):
    # send the sessions
    producer.send('requests', user[:-1])
    producer.flush()        
    time.sleep(dt)

