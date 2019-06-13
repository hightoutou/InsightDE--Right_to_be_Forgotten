# Right to be Forgotten

## Project Idea

Most data storage and processing systems were originally designed to treat data as invaluable, with fault-tolerance designed to never lose data. However, new regulations like GDPR require data teams to allow users to purge their systems of all data associated with that user. I'm going to build a data processing pipeline with the "right to be forgotten" for both streaming data and historical data. 


## Business Case

For websites like Airbnb who have very large traffic, it's important to implement lots of streaming analytics to better understand the behaviors of users. When some users require to delete their data, we should have rapid response for both streaming analysis and hostorical analysis.


## Dataset

1. Airbnb New User bookings(https://www.kaggle.com/c/airbnb-recruiting-new-user-bookings/data)
2. Simulated data for user's deletion requests


## Engineering Challenge

1. To integrate the deletion requests to streaming process.
2. Efficiently delete the historical data and modify the historical analyzed results for users who have deletion requests.


## Tech Stack
S3, Kafka, Spark, ProsgreSQL

