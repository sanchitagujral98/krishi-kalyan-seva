#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer=LancasterStemmer
import numpy as np
import tensorflow as tf
import tflearn
import random


# In[2]:


# get_ipython().system('pip install tflearn')
#
#
# # In[4]:
#
#
# get_ipython().system('apt-get install -y -qq software-properties-common python-software-properties module-init-tools')
# get_ipython().system('add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null')
# get_ipython().system('apt-get update -qq 2>&1 > /dev/null')
# get_ipython().system('apt-get -y install -qq google-drive-ocamlfuse fuse')
# from google.colab import auth
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


# In[ ]:


import pickle
data=pickle.load(open('training_data','rb'))


# In[ ]:


words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']


# In[ ]:


import json
with open('intents.json') as json_data:
    intents = json.load(json_data)


# In[11]:



# # reset underlying graph data
tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
#load our saved model
model.load('model.tflearn')


# In[ ]:


def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer().stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))


# In[ ]:


error_thresh=0.25
def classify(sentence):
     # generate probabilities from the model
    results=model.predict([bow(sentence,words)])[0]
     # filter out predictions below a threshold
    results=[[i,r] for i,r in enumerate(results) if r>error_thresh]
     # sort by strength of probability
    results.sort(key=lambda x:x[1],reverse=True)
    return_list=[]
    for r in results:
        return_list.append((classes[r[0]],r[1]))
         # return tuple of intent and probability
    return return_list


# In[ ]:


context={}
def response(sentence,user_id='123',show_details=False):
    results=classify(sentence)
     # if we have a classification then find the matching intent tag
    if results:
         # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                 # find a tag matching the first result
                    if i['tag'] == results[0][0]:
                         # set context for this intent if necessary
                        if 'context_set' in i:
                            if show_details: print('context',i['context_set'])
                            context[user_id]=i['context_set']

                        # check if this intent is contextual and applies to this user's conversation
                        if not 'context_filter' in i or (user_id in context and 'context_filter' in i and i['context_filter']==context[user_id]):
                            if show_details: print('tag:', i['tag'])
                            # a random response from the intent
                            return random.choice(i['responses'])
            results.pop(0)


# In[22]:


#ans = response('tell me about wheat protection')

# print(ans)
# from gtts import gTTS
# import os
# import time
# tts = gTTS(text=ans, lang='en')
# tts.save('hello.mp3')
# os.system('vlc hello.mp3')


import speech_recognition as sr

import time
import os

from gtts import gTTS
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='hi')
    tts.save("audio.mp3")
    os.system("vlc audio.mp3")

def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio, language='hi')
        print("You said: " + data)
        print(type(data))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data

def bot(data):
    #ans = response(data)
    speak(data)

# from googletrans import Translator
# def converter(data):
#     translator = Translator()
#     con_data = translator.translate(data, dest='en')
#     return con_data

# initialization
#time.sleep(1)
#speak("Hi Frank, what can I do for you?")

#data = recordAudio()

    # con_data = converter(data)
#bot(data)
