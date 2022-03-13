import json
import pandas as pd
import requests as rq
from datetime import datetime,timedelta, timezone, date
import time

def check_update():
  url =  'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
  df = pd.read_csv(url)
  #データの最新日
  upd_date = pd.to_datetime(df.columns[-1],format='%m/%d/%y').date()
  #ほしい日付（日本時間でみて、更新作業当日の１日前まで確報が入ればOK）
  prev_date = (datetime.utcnow()-timedelta(hours=15)).date()
  #更新フラグ、通知
  flag = True if upd_date >= prev_date else False
  msg = ('データが更新されました('+pd.to_datetime(upd_date).strftime('%Y/%m/%d')) if flag else "未更新です"
  return flag, msg

#初回チェック
update, text = check_update()

#未更新なら15時までトライ
while update==False:
  update, text = check_update()
  if ((datetime.utcnow() + timedelta(hours=9)).hour >15):
    text = '15時までに更新が確認できませんでした'
    print(datetime.now(timezone(timedelta(hours=+9), 'JST')).strftime('%Y/%m/%d日 %H:%M'), ':',text)
    break
  else:
    print(datetime.now(timezone(timedelta(hours=+9), 'JST')).strftime('%Y/%m/%d/ %H:%M'), ':',text)
    time.sleep(60*5)

#slack　#coronavirus_dataに投稿
WEB_HOOK_URL = 'https://hooks.slack.com/services/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'

alert = '▼Johns Hopkins University (JHU)の世界の感染者・死者数:\n'\
+ datetime.now(timezone(timedelta(hours=+9), 'JST')).strftime('%Y年%m月%d日 %H:%M')\
+ "\n\n" + text

rq.post(WEB_HOOK_URL, data=json.dumps({"text" : alert,}))
