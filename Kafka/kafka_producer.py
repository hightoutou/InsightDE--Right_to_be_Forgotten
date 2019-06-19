#########################
# pyhton3 file kafka_producer.py
# read data from s3 and send it to kafka-cluster
#########################


from kafka import KafkaProducer
import time
from smart_open import smart_open
import yaml
from random import randint

def get_user_id():
    for user in smart_open('s3://airbnbbookingwqk/users_all.csv', 'rb'):
        yield(str(user, "utf-8")[:-1])

def main():
    
    # read config file
    with open("config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile)

    producer = KafkaProducer(bootstrap_servers = config['bootstrap_servers_address'])   
    users_deletion = get_user_id() # the set to save users who have deletion requests
    n = 0 # number of sessions
    offset = 0 # offset to random generate deletion request
    deletion_interval = randint(10,30)
    for msg in smart_open(config['s3_fpath'], 'rb'):
        #print(msg)
        
        # simulation for request stream
        if offset >= deletion_interval: 
            user_id = next(users_deletion)
            producer.send('requests', user_id.encode())   
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

