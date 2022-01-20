#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd
import requests
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup as bs
import re
import urllib


# In[3]:


url = 'https://www.kantei.go.jp/jp/headline/kansensho/vaccine.html'


# In[5]:


r = requests.get(url)


# In[9]:


soup = bs(r.content,'lxml')


# In[13]:


tags = [i for i in soup.select('.aly_tx_center') if '日別の実績' in i.text][0].select('span')


# In[17]:


file_url = [tag for tag in tags if '都道府県別' in tag.text][0].find('a', attrs={ 'href': re.compile('.xlsx') }).get('href')


# In[20]:


file_url = 'https://www.kantei.go.jp' + file_url if 'https://www.kantei.go.jp' not in file_url else file_url


# In[31]:


file_name= f".legacy_data/raw_files/{datetime.utcnow().strftime('%Y%m%d')}_kenbetsu_vaccination_data2.xlsx"


# In[30]:


urllib.request.urlretrieve(file_url, file_name)

