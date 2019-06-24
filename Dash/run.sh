##############
#### run the entire streaming process
##############

### clear Redis DB
ssh ubuntu@ip-10-0-0-9 redis-cli FLUSHDB

### clear PostgreSQL DB
ssh ubuntu@ip-10-0-0-5 'sudo PGPASSWORD="spark" psql -U spark -d my_db -w -h localhost -p 5431 -c "DELETE FROM device_counts_filter;"'
ssh ubuntu@ip-10-0-0-5 'sudo PGPASSWORD="spark" psql -U spark -d my_db -w -h localhost -p 5431 -c "DELETE FROM device_counts;"'

### run kafka_producer on s3_reader
ssh ubuntu@ip-10-0-0-12 'python3 kafka_producer.py'
