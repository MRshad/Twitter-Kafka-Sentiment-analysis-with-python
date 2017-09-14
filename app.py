import json
from kafka import SimpleProducer, KafkaClient
from kafka import KafkaProducer
import tweepy
import configparser
from pymongo import MongoClient



class TweeterStreamListener(tweepy.StreamListener ):
    """ A class to read the twitter stream and push it to Kafka"""
    
    def __init__(self, api, topic  ,track=['realmadrid'] ):
	config = configparser.ConfigParser()
	config.read('twitter-app-credentials.txt')
	bootstrap_servers = config['KAFKA']['bootstrap_servers']
        self.api = api
	self.topic = topic
	
        super(tweepy.StreamListener, self).__init__()
	self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
	self.producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
	
    def on_status(self, status):
        """ This method is called whenever new data arrives from live stream.
        We asynchronously push this data to kafka queue"""
        
        try:
	    print(self.topic)
            self.producer.send(str(self.topic), status._json)
        except Exception as e:
            print(e)
            return False
        return True

    def on_error(self, status_code):
        print("Error received in kafka producer")
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream
def mongoreadid(collection , field):
	""" reads a specific field in a specific collection from mongodb """
	config = configparser.ConfigParser()
	config.read('twitter-app-credentials.txt')
	mongo_url = config['MONGO']['url']
	client = MongoClient(mongo_url)
	db = client['admin']
	ids = db[collection]
	return list(map((lambda id: id[field]), ids.find()))
def stream_id (id):
	 
	return  tweepy.Stream(auth, listener = TweeterStreamListener(api, id ))

def mongoread(database,collection , field):
	""" reads a specific field in a specific collection from mongodb """
	config = configparser.ConfigParser()
	config.read('twitter-app-credentials.txt')
	mongo_url = config['MONGO']['url']
	client = MongoClient(mongo_url)
	db = client[database]
	ids = db[collection]
	return list(map((lambda id: id[field]), ids.find()))

if __name__ == '__main__':

    # Read the credententials from 'twitter-app-credentials.txt' file
    config = configparser.ConfigParser()
    config.read('twitter-app-credentials.txt')
    consumer_key = config['DEFAULT']['consumerKey']
    consumer_secret = config['DEFAULT']['consumerSecret']
    access_key = config['DEFAULT']['accessToken']
    access_secret = config['DEFAULT']['accessTokenSecret']
   
    # Create Auth object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    

    # Read the users' ids form mongodb 
    id_list=mongoreadid('ids', 'id')
    # Read the topics form mongodb 
    topic_list=mongoreadid('topics', 'topic')
    topic_list=['cars']
    # Create stream and bind the listener to it
    stream=list(map(lambda id : stream_id(id), id_list ))
    #Custom Filter rules pull all traffic for those filters in real time.
    #stream.filter(track = ['love', 'hate'], languages = ['en'])
    keywords = mongoread('admin','keywords' , 'keywords')
    try:
	stream[0].filter(track=['madrid'], languages = ['en'])
	stream[1].filter(track=['neymare'], languages = ['en'])
	#map(lambda id : stream[id].filter(track=topic_list, languages = ['en']) , id_list)
    except Exception as e:
	print(e)

