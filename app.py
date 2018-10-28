import requests
from flask import Flask,render_template,json,config,request
from flask_sqlalchemy import SQLAlchemy
from main import recordAudio, bot, response
#from gtts import gTTS
app=Flask(__name__)
app.config['DEBUG']=True

@app.route('/vc', methods=['GET','POST'])
def vc():





    #output = bot(lang_data)

    return render_template('index.html')

@app.route('/background_process_test')
def background_process_test():


    txt='मुझे सब्सिडी पर कुछ जानकारी दीजिए'
    url='https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20181027T233108Z.1dcc6673818e795c.6b2bd8112a5f748b44298d1f4ec7785926fad057&lang=en&text='+txt
    lang_data=[]
    r = requests.get(url.format()).json()
    lang_data = r['text'][0]
    print(lang_data)
    res = response(lang_data)
    out_url='https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20181027T233108Z.1dcc6673818e795c.6b2bd8112a5f748b44298d1f4ec7785926fad057&lang=hi&text='+res
    x = requests.get(out_url.format()).json()
    out_str = x['text'][0]
    print(out_str)

    output = bot(out_str)





if __name__=="__main__":
    app.debug =True
    app.run()
