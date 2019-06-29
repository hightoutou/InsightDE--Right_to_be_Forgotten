# Right to be Forgotten
---

### Achieving GDPR compliance for streaming pipelines.
[slides link](https://docs.google.com/presentation/d/1NZEV2L6OCQwfJSpCsUan6cOmVcPRg0_UnywuBtEYJKI/edit#slide=id.g5c18997a73_1_1163)

## Tools Setup
---

### 0. Install Pegasus on local machine
reference: https://github.com/InsightDataScience/pegasus/blob/master/README.md#install-pegasus-on-your-local-machine

### 1. Set up Kafka Clusters

#### a. Spin up the Kafka cluster on AWS

configure file broker.yml
```
purchase_type: spot
subnet_id: <the VPC subnet id>
price: 0.1
num_instances: 3
key_name: <the pem key name>
security_group_ids: <security group id>
instance_type: m4.large
tag_name: kafka-cluster
vol_size: 100
role: worker
use_eips: true
```  

```bash
peg up broker.yml
peg describe kafka-cluster
```

#### b. Installing Kafka

```bash
peg install kafka-cluster ssh
peg install kafka-cluster aws
peg install kafka-cluster environment

peg install kafka-cluster zookeeper
peg service kafka-cluster zookeeper start
 
peg install kafka-cluster kafka
peg service kafka-cluster kafka start
%(note that there is a bug and the last command might just hang for no good reason. If so, just <ctrl-c> out of it)

``` 

#### c. Check Kafka Configuration

reference: https://github.com/InsightDataScience/data-engineering-ecosystem/wiki/Kafka

### 2. Set up Spark Clusters

#### a. Spin up the Spark cluster on AWS

configure file master.yml
```
purchase_type: spot
subnet_id: <the VPC subnet id>
price: 0.1
num_instances: 1
key_name: <the pem key name>
security_group_ids: <security group id>
instance_type: m4.large
tag_name: spark-cluster
vol_size: 100
role: master
use_eips: true
```

configure file worker.yml
```
purchase_type: spot
subnet_id: <the VPC subnet id>
price: 0.1
num_instances: 3
key_name: <the pem key name>
security_group_ids: <security group id>
instance_type: m4.large
tag_name: spark-cluster
vol_size: 100
role: worker
use_eips: true
```

```bash
peg up master.yml
peg up worker.yml
peg describe spark-cluster
```

#### b. Installing Spark

```bash
peg install spark-cluster ssh
peg install spark-cluster aws
peg install spark-cluster environment

peg install spark-cluster hadoop
peg service spark-cluster hadoop start

peg install spark-cluster spark
peg service spark-cluster spark start

```

#### c. WordCount Example
Reference:https://github.com/InsightDataScience/data-engineering-ecosystem/wiki/spark-intro#word-count-problem-with-the-spark-shell-repl-on-the-master-node


## Introduction
---

Most data storage and processing systems were originally designed to treat data as invaluable, with fault-tolerance designed to never lose data. However, new regulations like GDPR require data teams to allow users to purge their systems of all data associated with that user. 

For websites like Airbnb who have very large traffic, it's important to implement lots of streaming analytics to better understand the behaviors of users from different regions. When some users require to delete their data, we should have rapid response for both streaming analysis and historical analysis.

I'm going to build a streaming pipeline with the "right to be forgotten" feature to achieve GDPR compliance.


## Architecture
---

![alt text](https://github.com/hightoutou/InsightDE--Right_to_be_Forgotten/blob/master/images/Pipeline.png)


## Dataset
---

### 1. Session Stream
* 10M rows from [Airbnb New User Bookings Dataset](https://www.kaggle.com/c/airbnb-recruiting-new-user-bookings/data)
* User_id, action_type, device_type, elapsed_time

### 2. Requests Stream
* 100K unique user ids
* Simulate the stream of users’ deletion requests


## Engineering Challenge
---

### 1. Throughput 

![alt text](https://github.com/hightoutou/InsightDE--Right_to_be_Forgotten/blob/master/images/Throughput.png)

I increased the throughput from 700 messages per second to 10K messages per second.


### 2. Latency

![alt text](https://github.com/hightoutou/InsightDE--Right_to_be_Forgotten/blob/master/images/Latency_filtering.png)

The main part of latency comes from filtering stream according to the deletion table stored on Redis. I tested the performance for two different filtering methods. The choice between two methods depends on the size of deletion table and the minibatch size.



