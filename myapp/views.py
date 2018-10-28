from django.shortcuts import render, redirect
import requests
from main import recordAudio, bot, response
# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def btn(request):

    txt=recordAudio()
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
    return redirect('/')
