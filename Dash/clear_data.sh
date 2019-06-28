#!/bin/bash

### clear Redis DB
ssh ubuntu@ip-10-0-0-9 redis-cli FLUSHDB

### clear PostgreSQL DB
ssh ubuntu@ip-10-0-0-5 'sudo PGPASSWORD="spark" psql -U spark -d my_db -w -h localhost -p 5431 -c "DELETE FROM device_avg_time_filter;"'
