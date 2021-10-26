try:
    import traceback
    import os
    import json
    import glob
    import string
    import time
    import requests
    import re
    import urllib
    from bs4 import BeautifulSoup
    from itertools import groupby as g
    R = open('SL.json',"r").read()
    li = eval(R.replace('\n',""))
    splitter = "/"
    sta = ""
    chrs = []
    for x in string.ascii_lowercase:
        chrs.append(x)
        chrs.append(2*x)
    def f(chnumber):
            count = 0
            lastpage = ''
            widths = ["720","900"]
            credit = True
            if splitter == "\\":
                files = glob.glob(sta+"*.jpg")
                for f in files:
                    os.remove(f)
            else:
                os.system('rm *.jpg')
            images2 = BeautifulSoup(urllib.request.urlopen(urllib.request.Request('https://www.asurascans.com/solo-leveling-chapter-{}'.format(chnumber), headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})),features="html.parser").findAll('img')
            for img in images2:
                x = img.get('src')
                ch = x[-x[::-1].find("/"):]
                if img.get('width') in widths:
                    if credit:
                        res = requests.get(lastpage)
                        file = open(sta+"{}.jpg".format(chrs[count]),"wb")
                        count += 1
                        file.write(res.content)
                        file.close()
                        credit = False
                    res = requests.get(img.get('src'))
                    lastsize = img.get('height')
                    file = open(sta+"{}.jpg".format(chrs[count]),"wb")
                    count += 1
                    file.write(res.content)
                    file.close()
                lastpage = img.get('src')
            if int(lastsize) < 1500:
                os.remove(sta+"{}.jpg".format(chrs[count-1]))
    def g():
            from os import path
            from imgur_python import Imgur
            import glob
            imgur_client = Imgur({
            "client_id": "9ad42d14e2256fc",
            "client_secret": "74aec9a23650719f2dac416b3f0cd99d6b3437c7",
            "access_token": "306276876099fe3a9c8a628b666bdcf5a59ef396",
            "expires_in": "315360000",
            "token_type": "bearer",
            "refresh_token": "e77033ecc87aecb84b840012e8bcb16e286daa34",
            "account_username": "Ugi0",
            "account_id": 152145920 })
            images = []
            filess = glob.glob(sta+"*.jpg")
            filess.extend(glob.glob(sta+"*.gif"))
            leng = len(filess)
            for i,x in enumerate(sorted(filess)):
                print("{}/{}".format(i+1,leng))
                file = path.realpath(x)
                while True:
                    try:
                        e = imgur_client.image_upload(file, 'Untitled', '')
                        break
                    except:
                        print("Error")
                        time.sleep(60)
                t = e['response']['data']['link']
                images.append(t[-t[::-1].find("/"):][:t[-t[::-1].find("/"):].find('.')])
                time.sleep(8)
            resp = imgur_client.album_create([], "Solo Leveling", "A Solo Leveling chapter, with credits.. Hopefully.", "hidden")
            y = resp['response']['data']['id']
            imgur_client.album_add(y,[images])
            r = imgur_client.gallery_album(y, "Solo Leveling", 0, '')['url']
            r = r[-r[::-1].find("/"):]
            return r
    print(li['chapters'].keys())
    for number in range(110,159):
        if str(number) not in li['chapters']:
            f(number)
            ending = g()
            li['chapters'][str(number)] = {'title':'','volume': '', 'last_updated': str(int(time.time())), 'groups': {'AsuraScans': '/proxy/api/imgur/chapter/{}'.format(ending)}}
            file = open('SL.json', "w")
            file.write(str(li))
            file.close()
            print("Chapter:",number)
            for x in range(60*10):
                time.sleep(1)
except KeyboardInterrupt:
    handle = open('SL.json',"r").read()
    parsed = json.dumps(eval(handle),indent=4)
    write_file = open('SL.json', "w")
    write_file.write(parsed)
    write_file.close()
