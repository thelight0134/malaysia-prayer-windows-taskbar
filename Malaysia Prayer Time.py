import requests
import datetime
import schedule
import os
import time
from bs4 import BeautifulSoup

prayerTimes = {}

def fetchToday():
    r = requests.get('https://www.e-solat.gov.my/index.php?r=esolatApi/xmlfeed&zon=WLY01')
    soup = BeautifulSoup(r.content, features='xml')

    prayItems = soup.findAll('item')
    prayDate = soup.find('dc:date').text

    for prayItem in prayItems:
        title = prayItem.find('title').text 
        description = prayItem.find('description').text + ' ' + prayDate.split(' ')[0]
        date_time_obj = datetime.datetime.strptime(description, '%H:%M:%S %d-%m-%Y')
        prayerTimes[title] = date_time_obj

def renameFile(currentPray):
    nextTime = prayerTimes[currentPray].strftime("%I.%M %p")
    newName = f'{currentPray} - {nextTime}'
    os.rename('Prayer Time/{}'.format(os.listdir('Prayer Time')[0]),f'Prayer Time/{newName}.lnk')

def getNextPray():
    toBeNextPray = ''
    for prayerTime in prayerTimes:
        if(datetime.datetime.now() < prayerTimes[prayerTime]):
            toBeNextPray = prayerTime
    if(toBeNextPray == ''):
        toBeNextPray = 'Imsak'
    return toBeNextPray

def init():
    fetchToday()

def job():
    nextPray = ''
    toBeNextPray = getNextPray()
    if(nextPray != toBeNextPray):
        renameFile(toBeNextPray)
        nextPray = toBeNextPray

init()
schedule.every().day.at("00:01").do(init)
schedule.every(1).minutes.do(job)
job()
while True:
    schedule.run_pending()
    time.sleep(20)
