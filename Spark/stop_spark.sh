#!/bin/bash

##############
#### stop the entire streaming process
##############

### stop spark_streaming on spark-cluster-1
ssh ubuntu@ip-10-0-0-8 'pkill -f spark_streaming_sessions.py'
ssh ubuntu@ip-10-0-0-8 'pkill -f spark_streaming_requests.py'


