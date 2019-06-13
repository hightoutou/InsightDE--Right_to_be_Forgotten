# Spark Clusters
---

## Set up Kafka clusters

#### 1. Install Pegasus on local machine
reference: https://github.com/InsightDataScience/pegasus/blob/master/README.    md#install-pegasus-on-your-local-machine

#### 2. Spin up the Spark cluster on AWS

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

#### 3. Installing Spark

```bash
peg install spark-cluster ssh
peg install spark-cluster aws
peg install spark-cluster environment

peg install spark-cluster hadoop
peg service spark-cluster hadoop start

peg install spark-cluster spark
peg service spark-cluster spark start

```

#### 4. WordCount Example
Reference:https://github.com/InsightDataScience/data-engineering-ecosystem/wiki/spark-intro#word-count-problem-with-the-spark-shell-repl-on-the-master-node
(TBD)
