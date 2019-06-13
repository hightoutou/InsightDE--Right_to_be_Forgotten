# Kafka Clusters
---

## Set up Kafka clusters

#### 1. Install Pegasus on local machine
reference: https://github.com/InsightDataScience/pegasus/blob/master/README.md#install-pegasus-on-your-local-machine

#### 2. Spin up the Kafka cluster on AWS

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

#### 3. Installing Kafka

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

#### 4. Check Kafka Configuration

reference: https://github.com/InsightDataScience/data-engineering-ecosystem/wiki/Kafka

#### 5. Kafka Manager(optional)

reference: https://github.com/InsightDataScience/data-engineering-ecosystem/wiki/Kafka
