#########################
# pyhton3 file kafka_producer.py
# read data from s3 and send it to kafka-cluster
#########################


from kafka import KafkaProducer
import time
from smart_open import smart_open
import yaml
from random import randint

def main():
    
    # read config file
    with open("config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile)

    producer = KafkaProducer(bootstrap_servers = config['bootstrap_servers_address'])   
    users_deletion = set() # the set to save users who have deletion requests
    n = 0 # number of sessions
    offset = 0 # offset to random generate deletion request
    deletion_interval = randint(10,30)
    for msg in smart_open(config['s3_fpath'], 'rb'):
        #print(msg)
        
        # simulation for request stream
        if offset >= deletion_interval: 
            user_id = str(msg, "utf-8").split('\t')[0]
            if user_id not in users_deletion:
                producer.send('requests', user_id.encode())
                users_deletion.add(user_id)
                print(user_id, deletion_interval)
                offset = 0
                deletion_interval = randint(10,30)
            
        
        # send the sessions
        producer.send('sessions', msg)

        producer.flush()
        
        offset += 1
        n += 1
        if n == 1000:
            break
        time.sleep(0.1)
    return

if __name__ == '__main__':
    main()

