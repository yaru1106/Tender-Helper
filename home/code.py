# -*- coding: utf-8 -*-
import json
from urllib import request
import pandas as pd
from collections import Counter
import requests
from bs4 import BeautifulSoup
import jieba
import re
from string import digits
from tkinter import _flatten

def run(tempurl):
    print("code")
    print(tempurl)
    tempurl = str(tempurl)
    page = 1
    list = []
    count = False
    while(1):
        url = tempurl+str(page)
        data = request.urlopen(url).read().decode("utf-8")
        json_data = json.loads(data)
        if not json_data['records']:
            print("此頁查無標案資料")
            break
        else:
            frame = pd.DataFrame.from_dict(json_data)
            qname = frame['query'][0]
            for i in json_data['records']:
                if(i['brief']['type']=='決標公告'):
                    name = i['brief']['companies']['names']
                    for j in name:
                        if(j!=qname):
                            list.append(j)
        page = page + 1

    if not list:
        top_ten = "查無標案資料"
        count = 0
    else:
        result = Counter(list)
        # 前10名
        if(len(result)<10):
            length = len(result)
        else:
            length = 10
        top_ten = result.most_common(length)
        count = 0
        for i in top_ten:
            count = count + 1
            #print("第%d名：%s 競爭次數共計%d次" % (count,i[0],i[1]))
    return top_ten,count


def runid(tempurl):
    print("codeid")
    #url = 'https://pcc.g0v.ronny.tw/api/searchbycompanyname?query=%E9%B4%BB%E6%B5%B7&page='
    print(tempurl)
    tempurl = str(tempurl)
    page = 1
    list = []

    while(1):
        url = tempurl+str(page)
        data = request.urlopen(url).read().decode("utf-8")
        json_data = json.loads(data)
        if not json_data['records']:
            print("此頁查無標案資料")
            break
        else:
            frame = pd.DataFrame.from_dict(json_data)
            qname = frame['query'][0]
            for i in json_data['records']:
                if(i['brief']['type']=='決標公告'):
                    name = i['brief']['companies']['names']
                    for j in name:
                        if(j!=qname):
                            list.append(j)
        page = page + 1

    if not list:
        top_ten = "查無標案資料"
        count = 0
    else:
        result = Counter(list)
        # 前10名
        if(len(result)<11):
            length = len(result)
        else:
            length = 11
        top_ten = result.most_common(length)
        top_ten = top_ten[1:]
        count = 0
        for i in top_ten:
            if count==0:
                continue
            count = count + 1
            #print("第%d名：%s 競爭次數共計%d次" % (count,i[0],i[1]))
    return top_ten,count

def datarun(tempurl):
    print("datarun")
    print(tempurl)
    tempurl = str(tempurl)
    page = 1
    Ydata = [] #得標資料
    Ndata = [] #流標資料
    categorylist = [] #類別資料
    total_count = 0
    money = []
    windate = []
    while(1):
        url = tempurl+str(page)
        data = request.urlopen(url).read().decode("utf-8")
        json_data = json.loads(data)
        if not json_data['records']:
            print("此頁查無標案資料")
            break

        company_name = json_data['query']
        # total_data = len(json_data['records'])
        for i in json_data['records']:
            #找有決標的
            if(i['brief']['type']=='決標公告'):
                print("決標時間")
                print(i['date'])
                #標案爬蟲
                tender_url = i['tender_api_url']
                tender_data = request.urlopen(tender_url).read().decode("utf-8")
                tender_json_data = json.loads(tender_data)
                # if not json_data['records']:
                #     print("empty")
                for j in tender_json_data['records']:
                    if (j['date']==i['date'] and  j['brief']['type']=='決標公告'):
                        if(j['detail']['決標品項:第1品項:得標廠商1:得標廠商']==company_name):
                            print("得標了")
                            try:
                                categorylist.append(j['detail']['已公告資料:標的分類'])
                                Ydata.append([j['date'],i['brief']['title'],j['detail']['機關資料:機關名稱'],j['detail']['已公告資料:標的分類'],j['detail']['已公告資料:預算金額'],j['detail']['決標品項:第1品項:得標廠商1:得標廠商'],j['detail']['決標資料:總決標金額']])
                                total_count = total_count+1
                                windate.append(j['date'])
                                test1 = j['detail']['已公告資料:預算金額'][:-1].replace(",","")
                                test2 = j['detail']['決標資料:總決標金額'][:-1].replace(",","")
                                money.append(int(test1) - int(test2))
                            except Exception as e:
                                print(e)
                                print(i['brief']['title'])
                        else:
                            print("沒得標")
                            try:
                                Ndata.append([j['date'],i['brief']['title'],j['detail']['機關資料:機關名稱'],j['detail']['已公告資料:標的分類'],j['detail']['已公告資料:預算金額'],j['detail']['決標品項:第1品項:得標廠商1:得標廠商'],j['detail']['決標資料:總決標金額']])
                                total_count = total_count+1
                            except Exception as e:
                                print(e)
                                print(i['brief']['title'])
                        break; #找到對應標案就跳出
                if(total_count==20):
                    break
        print('total_count')
        print(total_count)
        if(total_count==20):
            break
        page = page+1
    test = Counter(categorylist)
    # categoryResult = {}
    label = []
    data = []
    for key in test:
        # categoryResult['label'] = key
        # categoryResult['count'] = categoryResult.get(key, 0) + 1
        label.append(key)
        data.append(int(test[key]))
    # categoryResult = Counter(categorylist)
    windate = windate[: :-1]
    money = money[: :-1]
    return Ydata,Ndata,label,data,total_count,company_name,windate,money

def datarunid(tempurl):
    print("datarunid")
    print(tempurl)
    tempurl = str(tempurl)
    page = 1
    Ydata = [] #得標資料
    Ndata = [] #流標資料
    categorylist = [] #類別資料
    total_count = 0
    money = []
    windate = []
    while(1):
        url = tempurl+str(page)
        print(url)
        data = request.urlopen(url).read().decode("utf-8")
        json_data = json.loads(data)
        print('json_data')
        #print(json_data['records'])
        if not json_data['records']:
            print("此頁查無標案資料")
            break

        company_name = json_data['query']
        # total_data = len(json_data['records'])
        for i in json_data['records']:
            #找有決標的
            if(i['brief']['type']=='決標公告'):
                print("決標時間")
                print(i['date'])
                #標案爬蟲
                tender_url = i['tender_api_url']
                tender_data = request.urlopen(tender_url).read().decode("utf-8")
                tender_json_data = json.loads(tender_data)
                # if not json_data['records']:
                #     print("empty")
                print("tender_json_data")
                print(tender_json_data['records'])
                for j in tender_json_data['records']:
                    print("j")
                    print(j)
                    if (j['date']==i['date'] and  j['brief']['type']=='決標公告'):
                        if(j['detail']['決標品項:第1品項:得標廠商1:得標廠商']==company_name):
                            print("得標了")
                            try:
                                categorylist.append(j['detail']['已公告資料:標的分類'])
                                Ydata.append([j['date'],i['brief']['title'],j['detail']['機關資料:機關名稱'],j['detail']['已公告資料:標的分類'],j['detail']['已公告資料:預算金額'],j['detail']['決標品項:第1品項:得標廠商1:得標廠商'],j['detail']['決標資料:總決標金額']])
                                total_count = total_count+1
                                windate.append(j['date'])
                                print("rrrrrr")
                                test1 = j['detail']['已公告資料:預算金額'][:-1].replace(",","")
                                test2 = j['detail']['決標資料:總決標金額'][:-1].replace(",","")
                                money.append(int(test1) - int(test2))
                            except Exception as e:
                                print(e)
                                print(i['brief']['title'])
                        else:
                            print("沒得標")
                            try:
                                Ndata.append([j['date'],i['brief']['title'],j['detail']['機關資料:機關名稱'],j['detail']['已公告資料:標的分類'],j['detail']['已公告資料:預算金額'],j['detail']['決標品項:第1品項:得標廠商1:得標廠商'],j['detail']['決標資料:總決標金額']])
                                total_count = total_count+1
                            except Exception as e:
                                print(e)
                                print(i['brief']['title'])
                        break; #找到對應標案就跳出
                    if (total_count==20):
                        break
        if (total_count==20):
            break
        page = page+1
    print('windate')
    print(windate)
    print(money)
    test = Counter(categorylist)
    # categoryResult = {}
    label = []
    data = []
    for key in test:
        # categoryResult['label'] = key
        # categoryResult['count'] = categoryResult.get(key, 0) + 1
        label.append(key)
        data.append(int(test[key]))
    # categoryResult = Counter(categorylist)
    windate = windate[: :-1]
    money = money[: :-1]
    return Ydata,Ndata,label,data,total_count,company_name,windate,money

def computedata(tempurl):

    print("computedata")
    # jieba.set_dictionary('dict.txt.big')
    print('tempurl')
    print(tempurl)

    tempurl = str(tempurl)
    page = 1
    Alldata = [] #標案名稱資料
    count = 0
    while(1):
        url = tempurl+str(page)
        data = request.urlopen(url).read().decode("utf-8")
        json_data = json.loads(data)
        if not json_data['records']:
            print("查無標案資料")
            break
        company_name = json_data['query']
        for i in json_data['records']:
            try:
                Alldata.append(i['brief']['title'])
                count = count + 1
            except Exception as e:
                print(e)
                print(i['brief']['title'])
            if(count==10):
                break
        if(count==10):
            break
        page = page+1

    if not Alldata:
        print("查無標案資料")
        final = []
    else:
        print(Alldata)
        print(len(Alldata))
        sentences = Alldata
        result = []
        for sentence in sentences:
            remove_digits = str.maketrans('', '', digits)
            sentence = sentence.translate(remove_digits)
            words = list(jieba.cut(sentence, cut_all=False))
            item = ['年度','年','月','、',')','(','（','）','上半年','下半年','至','及','暨','止','-','[',']','~','_']
            words = list(set(words)-set(item))
            result.append(words)
        result = list(_flatten(result))
        final = list(set(result))
        print(final)
    return final
