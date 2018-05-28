import datetime
from urllib.request import urlopen
from zipfile import ZipFile
import csv
import redis
now = datetime.datetime.now()
y_date = datetime.datetime.now() - datetime.timedelta(days=1)
todays_1600 = now.replace(hour=16, minute=0, second=0, microsecond=0)
week_n = datetime.datetime.today().weekday()
if week_n == 0:
    if now <= todays_1600:
        date = datetime.datetime.now() - datetime.timedelta(days=3)
    else:
        date = now
if week_n in range(1,5):
    if now <= todays_1600:
        date = y_date
    else:
        date = now
if week_n == 5:
    date = y_date
if week_n == 6:
    date = datetime.datetime.now() - datetime.timedelta(days=2)       
download_date = date.strftime("%d%m%y")
url = 'http://www.bseindia.com/download/BhavCopy/Equity/EQ' + download_date + '_CSV.ZIP'
response = urlopen(url)
filename = 'EQ' + download_date + '_CSV.ZIP'
temporary = open("/tmp/" + filename, "wb")
temporary.write(response.read())
temporary.close()
file = ZipFile("/tmp/" + filename)
file.extractall(path='/tmp/')
file.close()
redis_db = redis.StrictRedis(host="localhost", port=5000,charset="utf-8", decode_responses=True,db=1)
with open('/tmp/' + 'EQ' + download_date + '.CSV','r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for i in csv_reader:
        redis_db.rpush('name', i[1])
        redis_db.rpush('code', i[0])
        redis_db.rpush('open', i[4])
        redis_db.rpush('high', i[5])
        redis_db.rpush('low', i[6])
        redis_db.rpush('close', i[7])
