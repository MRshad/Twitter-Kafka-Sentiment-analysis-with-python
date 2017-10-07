import pandas as pd
import numpy as np
from pymongo import MongoClient
import matplotlib.pyplot as plt

# In[1]:
def mongo_read(collection , field):
	""" reads a specific field in a specific collection from mongodb """
	client = MongoClient("mongodb://root:123@localhost:27017/tracking?authSource=admin")
	db = client['admin']
	ids = db[collection]
	return list(map((lambda id: id[field]), ids.find()))

def make_plot(prediction):
    """
    This function plots the counts of positive and negative words for each timestep.
    """
    positiveCounts = []
    negativeCounts = []
    time = [1]


	
    positiveCounts = sum(prediction)
	
    negativeCounts= prediction.shape[0] - positiveCounts


    posLine = plt.plot(time, positiveCounts,'bo-', label='Positive')
    negLine = plt.plot(time, negativeCounts,'go-', label='Negative')
    #plt.axis([0, 1, 0, 5)
    plt.xlabel('Time step')
    plt.ylabel('sentiment')
    plt.legend(loc = 'upper left')
    plt.show()



def mongo_read(collection , field):
	""" reads a specific field in a specific collection from mongodb """
	client = MongoClient("mongodb://root:123@localhost:27017/tracking?authSource=admin")
	db = client['admin']
	ids = db[collection]
	return list(map((lambda id: id[field]), ids.find()))
# In[2]:
from sklearn.externals import joblib
clf = joblib.load('Nb_clf.pkl') 
 
vectorizer =joblib.load('vectorizer.pkl')
#define topic for test



topic='car'
clients_data = mongo_read(topic,'text')


df_1 = vectorizer.transform(clients_data)

prediction = clf.predict(df_1)


print (prediction)

make_plot(prediction)



