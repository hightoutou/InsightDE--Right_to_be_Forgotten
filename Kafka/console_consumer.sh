########
# console consumer to check the contents of a topic
########

/usr/local/kafka/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic sessions

