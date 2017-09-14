import json
import operator
import numpy as np
import matplotlib.pyplot as plt
from kafka import KafkaConsumer
from pymongo import MongoClient
import os

def mongoreadid(collection , field):
	""" reads a specific field in a specific collection from mongodb """
	client = MongoClient("mongodb://root:123@localhost:27017/tracking?authSource=admin")
	db = client['admin']
	ids = db[collection]
	return list(map((lambda id: id[field]), ids.find()))
def main_client(topic):
	consumer = KafkaConsumer(topic,
                         bootstrap_servers=['localhost:9092'],
			 value_deserializer=lambda m: json.loads(m.decode('ascii')))
	consumer.subscribe(topic)


	for message in consumer:
		print(message.value)
		insertmongo(message.value,topic)

def insertmongo(data , mycollection ):
	client = MongoClient("mongodb://root:123@localhost:27017/tracking?authSource=admin")
	db = client['admin']
	collection = db[mycollection]
   
	_id = collection.insert_one(data).inserted_id
	print("********-----------inserted---------------*****")
def printt(topic):
	print(topic)
if __name__=="__main__":
	print("started")
	# Read the users' ids form mongodb 
	id_list=mongoreadid('ids', 'id')
	
	# Read the topics form mongodb 
	topic_list=mongoreadid('topics', 'topic')
	# open consumers
	map(lambda topic : os.system('python tweet_consumer.py ' + str(topic)) ,id_list)
	
