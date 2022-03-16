import json
import pandas as pd
import requests as rq
from datetime import datetime,timedelta, timezone, date
import time
#part1: 厚労省、データからわかる新型コロナのバックデータ
#https://covid19.mhlw.go.jp/?lang=ja
url1 = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'
url2 = 'https://covid19.mhlw.go.jp/public/opendata/number_of_deaths_daily.csv'
url3 = 'https://covid19.mhlw.go.jp/public/opendata/confirmed_cases_cumulative_daily.csv'
url4 = 'https://covid19.mhlw.go.jp/public/opendata/deaths_cumulative_daily.csv'

url_list = {url1:'新規感染者数',url2:'新規死者数',url3:'累計感染者数',url4:'累計死者数'}

#ほしい日付
target = (datetime.utcnow()-timedelta(hours=15)).date()

#停止時刻
limit_h = 15

def check_update(url):
    #ほしい日付（日本時間でみて、更新作業当日の１日前まで確報が入ればOK）   
    df = pd.read_csv(url)
    #csvデータの最新日
    latest = pd.to_datetime(df.Date).max().date()
    #更新フラグ、通知
    flag = True if latest >= target else False
    return flag

#14時までに更新が確認できなかったものを放り込む
failure = []


#url1: 新規感染のcsvをチェック
update = False
url = url1

while not update:
    update = check_update(url)
    
    if ((datetime.utcnow() + timedelta(hours=9)).hour >=limit_h):
        failure = failure + [url_list[url]]
        break
    if not update:
        time.sleep(60*1)
        continue

#url2: 新規死者のcsvをチェック
update = False
url = url2

while not update:
    update = check_update(url)
    
    if ((datetime.utcnow() + timedelta(hours=9)).hour >=limit_h):
        failure = failure + [url_list[url]]
        break
    if not update:
        time.sleep(60*1)
        continue
        
#url3: 累計感染のcsvをチェック
update = False
url = url3

while not update:
    update = check_update(url)
    
    if ((datetime.utcnow() + timedelta(hours=9)).hour >=limit_h):
        failure = failure + [url_list[url]]
        break
    if not update:
        time.sleep(60*1)
        continue


#url4: 累計死者のcsvをチェック
update = False
url = url4

while not update:
    update = check_update(url)
    
    if ((datetime.utcnow() + timedelta(hours=9)).hour >=limit_h):
        failure = failure + [url_list[url]]
        break
    if not update:
        time.sleep(60*1)
        continue

#更新が確認できたものリスト
success = set(url_list.values()) - set(failure)

#slack投稿用
text1 = "\n\n"+ "★「データからわかる－新型コロナウイルス感染症情報－」\nhttps://covid19.mhlw.go.jp/?lang=ja"+ "\n" + (('更新されました◎：'+ (','.join(success))) if (len(success)>0) else '')+ "\n" + ((f'{str(limit_h)}時まで未更新です：'+ (','.join(failure))) if (len(failure)>0) else '')

#part2
#国内の発生状況のcsv
#https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html
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
        time.sleep(60*1)
        continue

text2 = "\n\n"+ "★「国内の発生状況など」（空港海港の直近値取得用）\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html"+ "\n" + ('更新されました◎' if not failure2 else f'{str(limit_h)}時まで未更新です。')

text = '▼厚労省の感染者・死者データ:\n'+ datetime.now(timezone(timedelta(hours=+9), 'JST')).strftime('%Y年%m月%d日 %H:%M')
text = (text + '\n\n！！！未更新です！！！\n\n厚労省に問い合わせてください（代表から「データがわかる〜」の担当を呼び出し）\n\n') if (len(failure)+failure2)>0 else text
text = text + text1 + text2
print(text)

str = {"text":text}

with open('./mhlw_sourcedata_update_log.json', 'w') as f:
    json.dump(str, f, ensure_ascii=False)
