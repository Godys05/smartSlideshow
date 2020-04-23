from time import sleep
from selenium import webdriver
from Weather import *
from driverPrefs import *
from fileManager import *
import datetime
import holidays
import requests
import json
import random
import API
import wget

imageCount = 4
search = ''
imagesPath = '/home/godys/Pictures/Unsplash/'
images = []

#Erase Previous Images
images = getImages(imagesPath)
if len(images) > 0:
    for image in images:
        if (os.path.exists(image)): os.remove(image)


#Set Browser Config
ch_options = getPrefs()
drive = None

#Set API variables
current_weather = Weather()
response = {}
API_KEY, CITY = API.getAPIdata()

#Search for Today's Events
mx_holidays = holidays.Mexico()
today = str(datetime.datetime.today()).split()[0]
today_holiday = mx_holidays.get(today)


if (today_holiday): #If event exists
    search = today_holiday
    search.replace(' ', '-')
else: #Otherwise get the current weather
    mainPage = ''
    req = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(CITY, API_KEY))
    response = json.loads(req.content)
    current_weather.main = response["weather"][0]["description"]
    current_weather.main.replace(' ', '-')
    search =  current_weather.main

#Launch the browser

drive = webdriver.PhantomJS('/home/godys/Documents/phantomjs/bin/phantomjs')
drive.maximize_window()
mainPage = 'https://unsplash.com/s/photos/'+search+'?orientation=landscape'

#Pick 5 random images from the results and download them

for i in range(imageCount):
    drive.get(mainPage)
    images = drive.find_elements_by_class_name('_2Mc8_')
    download_link = images[random.randint(0,len(images)-1)].get_attribute('href')+'/download?force=true&w=2400'
    session = requests.Session()
    cookies = drive.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    res = session.get(download_link)
    open('/home/godys/Pictures/Unsplash/image'+str(i)+'.jpg', 'wb').write(res.content)
    print(res.content)
    sleep(1)
drive.quit()

#Get every image exact path
images = getImages(imagesPath)

#Every two minutes change the background
while True:
    for image in images:
        os.system('/usr/bin/gsettings set org.gnome.desktop.background picture-uri '+image)
        sleep(120)