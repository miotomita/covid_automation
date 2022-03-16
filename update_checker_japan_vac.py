import json
import pandas as pd
import requests as rq
from datetime import datetime,timedelta, timezone, date
import time
from bs4 import BeautifulSoup as bs
import re
import mojimoji
from japanera import Japanera
janera = Japanera()

#ほしい日付
#ワクチンは当日「公表」
target = (datetime.utcnow()+timedelta(hours=9)).date()

#停止時刻
limit_h = 20



target = date(2022,3,16)

def check_update(url):
    r = rq.get(url)
    soup = bs(r.content,'lxml')
    #日付部分のみ抜粋・整形
    line = [t.text for t in soup.select("[class='aly_tx_center']") if '公表' in t.text]
    latest = re.search(r'..[0-9]*年[0-9]*月[0-9]*日',mojimoji.zen_to_han(line[0])).group()
    latest = janera.strptime(latest, "%-E%-o年%m月%d日")[0].date()
    #更新フラグ、通知
    flag = True if latest >= target else False
    return flag

#チェック
update, failure = False, False

while not update:
    update = check_update('https://www.kantei.go.jp/jp/headline/kansensho/vaccine.html')   
    if ((datetime.utcnow() + timedelta(hours=9)).hour >=limit_h):
        failure = True
        break
    if not update:
        time.sleep(60*1)
        continue

text = '▼日本ワクチンのバックデータ:\n'\
+ datetime.now(timezone(timedelta(hours=+9), 'JST')).strftime('%Y年%m月%d日 %H:%M')\
+ ((f'\n\n！！！{str(limit_h)}時まで未更新です！！！\n\n首相官邸に問い合わせてください\n\n') if failure else '\n\n更新されました◎')\
+ "\n\n"+ "★「首相官邸のワクチン情報」\nhttps://www.kantei.go.jp/jp/headline/kansensho/vaccine.html"

str = {"text":text}

with open('./mhlw_sourcedata_update_log.json', 'w') as f:
    json.dump(str, f, ensure_ascii=False)
