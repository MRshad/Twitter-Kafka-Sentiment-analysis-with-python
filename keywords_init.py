from pymongo import MongoClient
import sys
import configparser


def mongoread(database,collection , field):
	""" reads a specific field in a specific collection from mongodb """
	config = configparser.ConfigParser()
	config.read('twitter-app-credentials.txt')
	mongo_url = config['MONGO']['url']
	client = MongoClient(mongo_url)
	db = client[database]
	ids = db[collection]
	return list(map((lambda id: id[field]), ids.find()))
def mongoadd(topic,database,collection ):
	""" insert a topic in a specific field in a specific collection in mongodb """
	config = configparser.ConfigParser()
	config.read('twitter-app-credentials.txt')
	mongo_url = config['MONGO']['url']
	client = MongoClient(mongo_url)
	db = client[database]
	ids = db[collection]
	ids.insert_one(topic).inserted_id
def mongo_update(topic, data,database,collection ):
	""" insert a topic in a specific field in a specific collection in mongodb """
	config = configparser.ConfigParser()
	config.read('twitter-app-credentials.txt')
	mongo_url = config['MONGO']['url']
	client = MongoClient(mongo_url)
	db = client[database]
	ids = db[collection]
	ids.update({'_id':topic},data)
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: topic_init.py  topic keyword1,keyword2 ", sys.stderr)
        	exit(-1)
	database='admin'
	collection = 'keywords'
	field = '_id'
	# read list already added topics
	old_topic_list = mongoread(database,collection , field)
	# read new topics to add	
	topics = sys.argv[1].split(',')
	keywords = sys.argv[2].split(';')
	
	# filtering already added topics
	to_add_list = filter(lambda topic: topic not in old_topic_list ,  topics)  
	# adding new keywords
	map(lambda topic : mongoadd({'keywords':keywords , '_id':topic},database,collection ),to_add_list )
	# filtering to update list
	to_update_list = filter(lambda topic: topic  in old_topic_list ,  topics)  
	# updating keywords
	map(lambda topic : mongo_update(topic,{'keywords':keywords , '_id':topic},database,collection ),to_update_list )
