#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
import requests as rq
from datetime import datetime,timedelta, timezone, date
import time


# In[2]:


url1 = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'
url2 = 'https://covid19.mhlw.go.jp/public/opendata/number_of_deaths_daily.csv'
url3 = 'https://covid19.mhlw.go.jp/public/opendata/confirmed_cases_cumulative_daily.csv'
url4 = 'https://covid19.mhlw.go.jp/public/opendata/deaths_cumulative_daily.csv'


# In[3]:


url_list = {url1:'新規感染者数',url2:'新規死者数',url3:'累計感染者数',url4:'累計死者数'}


# In[4]:


#ほしい日付
target = (datetime.utcnow()-timedelta(hours=15)).date()


# In[5]:


#テスト用
#target = (datetime.utcnow()-timedelta(hours=15) - timedelta(days=1)).date()


# In[6]:


#停止時刻
limit_h = 9


# In[7]:


def check_update(url):
    #ほしい日付（日本時間でみて、更新作業当日の１日前まで確報が入ればOK）   
    df = pd.read_csv(url)
    #csvデータの最新日
    latest = pd.to_datetime(df.Date).max().date()
    #更新フラグ、通知
    flag = True if latest >= target else False
    return flag


# In[8]:


failure = []


# In[9]:


(datetime.utcnow() + timedelta(hours=9)).hour


# In[10]:


update = False
url = url1

while not update:
    update = check_update(url)
    
    if ((datetime.utcnow() + timedelta(hours=9)).hour >=limit_h):
        failure = failure + [url_list[url]]
        break
    if not update:
        time.sleep(60*5)
        continue


# In[11]:


update = False
url = url2

while not update:
    update = check_update(url)
    
    if ((datetime.utcnow() + timedelta(hours=9)).hour >=limit_h):
        failure = failure + [url_list[url]]
        break
    if not update:
        time.sleep(60*5)
        continue


# In[12]:


update = False
url = url3

while not update:
    update = check_update(url)
    
    if ((datetime.utcnow() + timedelta(hours=9)).hour >=limit_h):
        failure = failure + [url_list[url]]
        break
    if not update:
        time.sleep(60*5)
        continue


# In[13]:


update = False
url = url4

while not update:
    update = check_update(url)
    
    if ((datetime.utcnow() + timedelta(hours=9)).hour >=limit_h):
        failure = failure + [url_list[url]]
        break
    if not update:
        time.sleep(60*5)
        continue


# In[14]:


success = set(url_list.values()) - set(failure)


# In[15]:


text = '▼厚労省の感染者・死者データ:\n'+ datetime.now(timezone(timedelta(hours=+9), 'JST')).strftime('%Y年%m月%d日 %H:%M')+ "\n\n"+ "★「データからわかる－新型コロナウイルス感染症情報－」\nhttps://covid19.mhlw.go.jp/?lang=ja"+ "\n" + (('更新されました◎：'+ (','.join(success))) if (len(success)>0) else '')+ "\n" + (('14時まで未更新です：'+ (','.join(failure))) if (len(failure)>0) else '')


# In[16]:


update = False
failure2 = False
url = 'https://covid19.mhlw.go.jp/public/partsdata/parts_current_situation.csv'

while not update:
    df5 = pd.read_csv(url)
    latest5 = (pd.to_datetime(df5.iloc[:,0]).max() - timedelta(days=1)).date()
    update = True if latest5 >= target else False
    if not update:
        if ((datetime.utcnow() + timedelta(hours=9)).hour >=limit_h):
            failure2 = True
            break
        time.sleep(60*5)
        continue


# In[17]:


text = text+ "\n\n"+ "★「国内の発生状況など」（空港海港の直近値取得用）\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html"+ "\n" + ('更新されました◎' if not failure2 else '14時まで未更新です。')


# In[18]:


print(text)


# In[19]:


str = {"text":text}


# In[20]:


with open('./mhlw_sourcedata_update_log.json', 'w') as f:
    json.dump(str, f, ensure_ascii=False)

