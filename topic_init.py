from pymongo import MongoClient
import sys



def mongoread(database,collection , field):
	""" reads a specific field in a specific collection from mongodb """
	client = MongoClient("mongodb://root:123@localhost:27017/tracking?authSource=admin")
	db = client[database]
	ids = db[collection]
	return list(map((lambda id: id[field]), ids.find()))
def mongoadd(topic,database,collection , field):
	""" insert a topic in a specific field in a specific collection in mongodb """
	client = MongoClient("mongodb://root:123@localhost:27017/tracking?authSource=admin")
	db = client[database]
	ids = db[collection]
	ids.insert_one(topic).inserted_id

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: topic_init.py   topic1,topic2 ", sys.stderr)
        	exit(-1)
	database='admin'
	collection = 'topics'
	field = 'topic'
	# read list already added topics
	old_topic_list = mongoread(database,collection , field)
	# read new topics to add	
	topics = sys.argv[1].split(',')
	print(topics)
	# filtering already added topics
	to_add_list = filter(lambda topic: topic not in old_topic_list ,  topics)  
	# adding new topics 
	map(lambda topic : mongoadd({'topic':topic},database,collection , field),to_add_list )
