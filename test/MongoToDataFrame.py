import pandas as pd
import datetime
import matplotlib.pyplot as pp
import time,os,sys

from pymongo import MongoClient
#   http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20180817&stockNo=2330

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"log")
# check log folder if exist or not
if not os.path.isdir(dirnamelog):
    os.mkdir(dirnamelog)

sys.path.append(dirnamelib)
import readConfig as readConfig
from logger import logger
import connectMongoDB

#global collection

t0 = time.time()
count = 0

configPath=os.path.join(strdirname,"config.ini")
localReadConfig = readConfig.ReadConfig(configPath)

mongo_host = localReadConfig.get_MongoDB('mongo_host')
mongo_db = localReadConfig.get_MongoDB('mongo_db')
mongo_collection = localReadConfig.get_MongoDB('mongo_collection')
mongo_username = localReadConfig.get_MongoDB('mongo_username') 
mongo_password = localReadConfig.get_MongoDB('mongo_password') 

str_last_year_month = localReadConfig.get_SeymourExcel("last_year_month")
str_last_year = str_last_year_month.split(',')[0]
str_last_month = str_last_year_month.split(',')[1]
str_stkidx =  localReadConfig.get_SeymourExcel("stkidx")
str_delay_sec = localReadConfig.get_SeymourExcel("delay_sec")

collection = connectMongoDB.MongoDBConnection.connect_mongo(mongo_host,mongo_db,
                    mongo_collection,mongo_username,mongo_password)   #連線資料庫

query = { 'stockno' : str_stkidx }
cursor = collection.find(query)  #依query查詢資料
stock =  pd.DataFrame(list(cursor))  #轉換成DataFrame
del stock['_id']  #刪除欄位_id
print(stock)
indexlist = []
for i in range(len(stock)):  #建立日期串列
    indexlist.append(stock['date'][i])  #stock['date'][i]為datetime.date物件
stock.index = indexlist  #索引值改成日期
stock = stock.drop(['date'],axis = 1)  #刪除日期欄位
mlist = []
for item in stock.index:   #建立月份串列
    mlist.append(item.month)
stock['month'] = mlist  #新增月份欄位
#print(stock)
result = stock
for item in result[result.close > 21]:  #收盤價大於21元
    print(item)
    
print(result[(result.index >= "2018-06-01") & (result.index <= "2018-06-30") & (result.close >= 21)])  #六月份大於21元

tmp = result.sort_values(by = 'close', ascending=False)   #依照收盤價排序
print(tmp[:3])  #取收盤價前三高

print(result.loc["2018-08-01":"2018-08-30"])  #只顯示2018六月份

print(result.loc["2018-08-01":"2018-12-31"].groupby('month').close.count())  #2018每個月幾個營業日

print(result.loc["2018-08-01":"2018-12-31"].groupby('month').shares.sum())  #2018每個月累計成交股數

result.loc["2018-08-01":"2018-12-31"].groupby('month').shares.sum().plot()  #2018月累計成交股數圖
pp.ylabel('shares')
pp.title('month of shares')

msg = 'End duration in {:.2f} seconds.'
logger.info(msg.format(time.time() - t0))