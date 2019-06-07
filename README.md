# Evolving-Classifier

## Project Idea

When people apply machine learning models on streaming data, the model performance will degrade with the change of the distribution and inherent features of the data stream.
I’m going to implement a machine learning pipeline that can automatically switch to a better model when the performance of current model becomes degrading.


## Business Case

Social media sites like Instagram provide users with content that makes it easy to buy drugs and connect with dealers. It’s urgent to have a good algorithm to classify drugs from images and prevent the transactions. However, since drugs keep evolving with time, we need to have an evolving classifier.


## Dataset

Simulating several image streams contain different kinds of illegal drugs(from old styles to up-to-date styles), and combining these streams to normal images not containing illegal drugs.
Size: TBD


## Engineering Challenge

1. Build a system to switch the ML model automatically according to the real-time model performance.
2. Ingest multiple image streams in real time.


## Tech Stack
Kafka, Kubernetes, Docker

