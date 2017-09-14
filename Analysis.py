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

sentiments=pd.read_csv("Sentiment_Analysis_Dataset.csv", sep=",",error_bad_lines=False)


# In[3]:




# In[3]:




# In[4]:

sentiments=sentiments.drop('ItemID', 1)
sentiments=sentiments.drop('SentimentSource', 1)


# In[5]:




# In[6]:

x=sentiments["SentimentText"]
y=sentiments["Sentiment"]


# to delete



print(x)
# In[7]:

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(min_df=2, ngram_range=(1, 2),    norm='l2')
X = vectorizer.fit_transform(x)


# In[8]:

from sklearn.model_selection import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
# to delete
X_train = X
y_train = y
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

#define topic for test
topic='car'
clients_data = mongo_read(topic,'text')

# In[9]:

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train, y_train)



topic='car'
clients_data = mongo_read(topic,'text')
print(clients_data)

#create new df 
df = pd.DataFrame({'text':clients_data})
print(df)
#.toarray()[0]
df_1 = vectorizer.transform(clients_data)

prediction = clf.predict(df_1)


print (prediction)

make_plot(prediction)



