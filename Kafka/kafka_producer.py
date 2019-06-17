#########################
# python3 file kafka_producer.py
# read data from s3 and send it to kafka-cluster
#########################


from kafka import KafkaProducer
import time
from smart_open import smart_open
import yaml

def main():

    with open("config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile)

    producer = KafkaProducer(bootstrap_servers = config['bootstrap_servers_address'])

    n = 0
    for msg in smart_open(config['s3_fpath'], 'rb'):
        producer.send('sessions', msg)
        producer.flush()
        print(msg)
        time.sleep(1)
        n += 1
        if n == 10:
            break
    return

if __name__ == '__main__':
    main()
