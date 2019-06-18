#####################
# Useful Commands for the Kafka cluster
#####################


# Create two topics sessions and requests on kafka-cluster

/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 2 --topic sessions
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 2 --topic requests


# Console producer to write messeages to a topic

/usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic requests


# console consumer to check the contents of a topic

/usr/local/kafka/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic sessions


# delete a topic
/usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic sessions

# describe a topic
/usr/local/kafka/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic sessions
