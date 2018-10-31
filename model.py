#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tensorflow as tf
import tflearn
import random


# In[ ]:


#get_ipython().system('pip install tflearn')


# In[ ]:


#get_ipython().system('apt-get install -y -qq software-properties-common python-software-properties module-init-tools')
#get_ipython().system('add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null')
#get_ipython().system('apt-get update -qq 2>&1 > /dev/null')
#get_ipython().system('apt-get -y install -qq google-drive-ocamlfuse fuse')
#from google.colab import auth
# auth.authenticate_user()
# from oauth2client.client import GoogleCredentials
# creds = GoogleCredentials.get_application_default()
# import getpass
# get_ipython().system('google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL')
# vcode = getpass.getpass()
# get_ipython().system('echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}')


# In[ ]:


# get_ipython().system('mkdir -p drive')
# get_ipython().system('google-drive-ocamlfuse drive')
#

# In[ ]:


import json
with open('intents.json') as json_data:
    intents = json.load(json_data)


# In[ ]:


import nltk
nltk.download('punkt')


# In[ ]:


words=[]
documents=[]
classes=[]
ignore_words=['?']

stemmer = LancasterStemmer()

# loop through each sentence in our intents patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
     # tokenize each word in the sentence
         w=nltk.word_tokenize(pattern)
     # add to our words list
         words.extend(w)
    # add to documents in our corpus
         documents.append((w, intent['tag']))
     # add to our classes list
         if intent['tag'] not in classes:
             classes.append(intent['tag'])


# stem and lower each word and remove duplicates
words=[stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words=sorted(list(set(words)))

# remove duplicates
classes=sorted(list(set(classes)))


# In[ ]:


# print (len(documents), "documents",documents)
# print (len(classes), "classes", classes)
# print (len(words), "unique stemmed words", words)


# In[ ]:


# create our training data
training=[]
output=[]

# create an empty array for our output
output_empty=[0]*len(classes)

# training set, bag of words for each sentence
for doc in documents:
    bag=[]
     # list of tokenized words for the pattern
    pattern_words=doc[0]
    pattern_words=[stemmer.stem(word.lower()) for word in pattern_words]
     # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

     # output is a '0' for each tag and '1' for current tag
    output_row=list(output_empty)
    output_row[classes.index(doc[1])]=1

    training.append([bag,output_row])

# shuffle our features and turn into np.array.
random.shuffle(training)
training=np.array(training)

# create train and test lists
train_x = list(training[:,0])
train_y = list(training[:,1])


# In[ ]:


# reset underlying graph data
tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
# Start training (apply gradient descent algorithm)
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
model.save('model.tflearn')


# In[ ]:


# save all of our data structures
import pickle
pickle.dump({'words':words,'classes':classes,'train_x':train_x,'train_y':train_y},open('drive/Colab Notebooks/chatbot/training_data','wb'))
