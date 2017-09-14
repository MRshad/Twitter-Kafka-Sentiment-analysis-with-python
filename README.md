#Twitter Sentiment Analytics using Apache KafkaStreaming APIs and Python 

In this project, we are processing live data streams using Sklear libraries for Python. I performed a machine learning based sentiment analysis of real-time tweets. In addition, I made the project scalable enough thanks to Apache Kafka, which is a queuing service for data streams. 

##Requirements
One of the first requirements is to get access to the streaming data; in this case, real-time tweets. Twitter provides a very 
convenient API to fetch tweets in a streaming manner 
 
In addition, I also used Kafka to buffer the tweets before processing. Kafka provides a distributed queuing service which can be used to store the data when the data creation rate is more than processing rate. It also has several other uses. 

###Project Setup 
 

 
####Installing and Initializing Kafka 
Download and extract the latest binary from https://kafka.apache.org/downloads.html

#####Start zookeeper service:  
`$ bin/zookeeper-server-start.sh config/zookeeper.properties`
 
#####Start kafka service: 
`$ bin/kafka-server-start.sh config/server.properties`
 

 
####Using the Twitter Streaming API 
In order to download the tweets from twitter streaming API and push them to kafka queue, I have created a python script
app.py. The script will need your twitter authentication tokens (keys).

Once you have your authentication tokens, create or update the `twitter-app-credentials.txt` with these  credentials. it also contains the mongo url settings and the kafka bootstrap server. thos should be configured too.

After updating the text file with your twitter keys, you can start downloading tweets from the twitter stream API and push them to the twitterstream topic in Kafka. Do this by running the script as follows:   
`$ python app.py`   
Note: This program should be kept running for collecting tweets. 
 
#####To check if the data is landing in Kafka: 
`$ bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic yourtopic --from-beginning`
note that your topic is the topic you set using topic_init

#####Running the Stream Program:
`$ python app.py`

#####Reading and storing in MongoDB:
`$ python twitterStream.py`

#####Running analysis:
`$ python analysis.py`


