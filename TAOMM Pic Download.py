import re
import requests
from bs4 import BeautifulSoup
from agent import headers
from json import loads
import os
import random
import time

def GetUrlList():
    url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
    html = requests.request('POST', url, headers ={'user-agent': headers()})
    json = loads(html.text)
    return json['data']['searchDOList']



def GetInfo(userid):
    url1 = 'https://mm.taobao.com/self/aiShow.htm?userId=%s' %userid
    req = requests.request('POST', url1 , headers ={'user-agent': headers()})

def GetAlbumList(userid):
    try:
        url1 = 'https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%%20=%s' %userid
        req = requests.request('POST', url1 , headers ={'user-agent': headers()})
        soup = BeautifulSoup(req.text,'html.parser')
        imglist = soup.find_all('a',attrs={'class':'mm-first'}) 
        list = []
        for image_array in imglist:
            image = image_array.find('img')
            link = image.get('src')
            # print (link)
            list.append(link)
        return list
    except :
        text = 'GetAlbumList wrong'
        return text

def SavePic(list,realName,n):
    path = os.getcwd()
    new_path = os.path.join(path , 'pictures','%s'%realName)
    if not os.path.exists(new_path) :
        os.makedirs(new_path)
    try:
        req = requests.request('GET', 'http:' + list , headers ={'user-agent': headers()})
        pic = req.content
        filename = '%s/%s%s.jpg'%(new_path, realName,n)
        with open(filename, 'wb') as f:  
            f.write(pic)  
    except:
        sleep_time=random.randint(1,3)
        time.sleep(sleep_time)
        print('Wait%ds'%sleep_time)


for i in GetUrlList():
    userId = i['userId']
    realName = i['realName']
    GetInfo(userId)
    n = 0
    for list in GetAlbumList(userId):
        n = n + 1
        SavePic(list,realName,n)
print('finished')

        
    