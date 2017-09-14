import json
import operator
import numpy as np
import configparser
from kafka import KafkaConsumer
from pymongo import MongoClient
import sys


def mongoreadid(collection , field):
	""" reads a specific field in a specific collection from mongodb """
	config = configparser.ConfigParser()
	config.read('twitter-app-credentials.txt')
	mongo_url = config['MONGO']['url']
	client = MongoClient(mongo_url)
	db = client['admin']
	ids = db[collection]
	return list(map((lambda id: id[field]), ids.find()))
def main_client(topic):
	config = configparser.ConfigParser()
	config.read('twitter-app-credentials.txt')
	bootstrap_servers = config['KAFKA']['bootstrap_servers']
	consumer = KafkaConsumer(topic,
                         bootstrap_servers=bootstrap_servers,
			 value_deserializer=lambda m: json.loads(m.decode('ascii')))
	consumer.subscribe(topic)


	for message in consumer:
		print(message.value)
		insertmongo(message.value,topic)

def insertmongo(data , mycollection ):
	config = configparser.ConfigParser()
	config.read('twitter-app-credentials.txt')
	mongo_url = config['MONGO']['url']
	client = MongoClient(mongo_url)
	db = client['admin']
	collection = db[mycollection]
   
	_id = collection.insert_one(data).inserted_id
	print("********-----------inserted---------------*****")

if __name__=="__main__":
	if len(sys.argv) != 2:
		print("Usage: topic_init.py   topic1,topic2 ", sys.stderr)
		exit(-1)
	topic = sys.argv[1]
	
	main_client(str(topic))
	
