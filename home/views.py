from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse
# python manage.py runserver 0.0.0.0:8000 heroku
#import code
from home.code import run
from home.code import runid
from home.code import datarunid
from home.code import datarun
from home.code import computedata
from nltk.metrics.distance import jaccard_distance
import requests
from bs4 import BeautifulSoup
import json
import urllib.parse


h = {'User-Agent': 'python-requests/2.18.4', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

def example(request):
    return render(request, 'home/example.html')

#competitor競爭者分析
def analytic2(request):
    return render(request, 'home/analytic2.html')

def competitor(request):
    return render(request, 'home/competitor.html')

def predict(request):
    return render(request, 'home/predict.html')

def tendsearch(request):
    return render(request, 'home/tendsearch.html')

def home(request):
    return render(request, 'home/index.html')

def tender(request):
    return render(request, 'home/tender.html')

def unit(request):
    return render(request, 'home/unit.html')

# def tender(request, pk):
#     articles = Article.objects.all()
#     return render(request, 'home/tender.html?'.format9(pk))

def search(request):
    return render(request, "home/search.html")

def searchbycompany(request):
    return render(request, "home/searchbycompany.html")

def searchbyid(request):
    return render(request, "home/searchbyid.html")

def date(request):
    return render(request, "home/date.html")


def comdata(request):
    print("comdata")
    str_req = str(request)
    str_req = str_req[33:]
    str_req = str_req[:-2]
    resp = requests.get("https://ronnywang.github.io/pcc-viewer/searchbycompany.html"+str_req+"&page=1",headers = h)
    url = "https://pcc.g0v.ronny.tw/api/searchbycompanyname"+str_req+"&page="
    print(url)
    Ydata,Ndata,label,data,total_count,company_name,windate,money = datarun(url)
    win = len(Ydata)
    lose = total_count-win
    return render(request, "home/comdata.html",{'Ydata': Ydata,'Ndata':Ndata,'label':label,'data':data,'total_count':total_count,'company_name':company_name,'win':win,'lose':lose,'windate':windate,'money':money})#

def comdataid(request):
    str_req = str(request)
    str_req = str_req[35:]
    str_req = str_req[:-2]
    resp = requests.get("https://ronnywang.github.io/pcc-viewer/searchbyid.html"+str_req+"&page=1",headers = h)
    url = "https://pcc.g0v.ronny.tw/api/searchbycompanyid"+str_req+"&page="
    Ydata,Ndata,label,data,total_count,company_name,windate,money = datarunid(url)
    win = len(Ydata)
    lose = total_count-win
    return render(request, "home/comdata.html",{'Ydata': Ydata,'Ndata':Ndata,'label':label,'data':data,'total_count':total_count,'company_name':company_name,'win':win,'lose':lose,'windate':windate,'money':money})#


def analytic(request):
    str_req = str(request)
    str_req = str_req[34:]
    str_req = str_req[:-2]
    resp = requests.get("https://ronnywang.github.io/pcc-viewer/searchbycompany.html"+str_req+"&page=1",headers = h)
    url = "https://pcc.g0v.ronny.tw/api/searchbycompanyname"+str_req+"&page="
    temp_result,count = run(url)
    final = set(computedata(url))
    result = []
    for i in temp_result:
        # j = list(tuple(i))
        j = {'name':i[0],'count':i[1]}
        rival_url = "https://pcc.g0v.ronny.tw/api/searchbycompanyname?query="+urllib.parse.quote(j['name'], safe='')+"&page="
        rival_result = set(computedata(rival_url))
        print(rival_result)
        try:
            p = round(len(final.intersection(rival_result))/len(final.union(rival_result))*100,2)
        except:
            p = 0
        j['similarity'] = p
        result.append(j)

    return render(request, "home/competition.html", {'result': result,'count':count})


def analyticid(request):

    print("viewid")
    str_req = str(request)
    str_req = str_req[36:]
    str_req = str_req[:-2]
    resp = requests.get("https://ronnywang.github.io/pcc-viewer/searchbyid.html"+str_req+"&page=1",headers = h)
    url = "https://pcc.g0v.ronny.tw/api/searchbycompanyid"+str_req+"&page="
    temp_result,count = runid(url)
    final = set(computedata(url))
    result = []
    for i in temp_result:
        j = list(tuple(i))
        rival_url = "https://pcc.g0v.ronny.tw/api/searchbycompanyname?query="+urllib.parse.quote(j[0], safe='')+"&page="
        rival_result = set(computedata(rival_url))
        print(rival_result)
        try:
            p = round(len(final.intersection(rival_result))/len(final.union(rival_result))*100,2)
        except:
            p = 0
        j.append(p)
        result.append(j)
    return render(request, "home/competition.html", {'result': result,'count':count})

def test(request, pk):
    return render(request, 'home/tender.html?'.format9(pk))
