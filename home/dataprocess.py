# -*- coding: utf-8 -*-
import json
from urllib import request
import pandas as pd
from collections import Counter
import requests
from bs4 import BeautifulSoup
import logging
from gensim.models import word2vec
from gensim import models
# 以下為Python 語法
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = word2vec.LineSentence("data/try_utf8.txt")
model = word2vec.Word2Vec(sentences, size=300, workers=3, window=5, min_count=15, iter=5)
#保存模型，供日後使用
model.save("data/3-CISWord2Vec-try.model")
model.wv.save_word2vec_format("data/3-CISWord2Vec-try.model", binary = False)

# 算出文字向量之後，各種比較相似度的方法
# 以下為Python 語法

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
model = models.keyedvectors.KeyedVectors.load_word2vec_format("data/3-CISWord2Vec-try.model", binary = False)

#範例字串
str1 = "朱立倫"
str2 = "韓國瑜"
str3 = "總統"

#要用的話要打開
strLst = ["蔡英文","賴清德","朱立倫","韓國瑜","郭台銘","柯文哲"]

print("%s 相似詞前10 :" %str3)
res = model.most_similar(str3 ,topn = 20)
for item in res:
  print(item[0]+","+ str(item[1]))

print("")
print("%s vs %s Cosine 相似度: " % (str1,str3))
res = model.similarity(str1 , str3)
print(res)

print("")
print("%s 之於 %s，如 %s 之於 " % (str5,str3,str1))
res = model.most_similar([str5,str1], [str3], topn= 10)
for item in res:
  print(item[0]+","+ str(item[1]))

print("====================================")
for i in range(len(strLst)):
    print("%s 相似詞前10 :" % strLst[i])
    res = model.most_similar(strLst[i] ,topn = 20)
    for item in res:
      print(item[0]+","+ str(item[1]))
    print("====================================")
