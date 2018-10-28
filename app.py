import requests
from flask import Flask,render_template,json,config,request
from flask_sqlalchemy import SQLAlchemy
from main import recordAudio, bot
#from gtts import gTTS
app=Flask(__name__)
app.config['DEBUG']=True

@app.route('/voice_assistant', methods=['GET','POST'])
def voice_assistant():
    txt=recordAudio()
    url='https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20181027T233108Z.1dcc6673818e795c.6b2bd8112a5f748b44298d1f4ec7785926fad057&lang=en&text=+txt'
    lang_data=[]
    r = requests.get(url).json()
    language={
       'result': r['text'][0],
    }


    lang_data=lang_data.append(language)
    en_data=lang_data[0]
    output = bot(en_data)

    return render_template('index.html')



if __name__=="__main__":
    app.debug =True
    app.run()
