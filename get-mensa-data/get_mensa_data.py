#pip install pdf2image
#-- poppler --
#https://github.com/oschwartz10612/poppler-windows/releases/
#env: "C:\path\to\poppler-xx\bin"

import requests
import urllib.request
import json
import re
import traceback
from bs4 import BeautifulSoup
from pdf2image import convert_from_path
from PIL import Image

url = "https://www.stw-bremen.de/de/cafeteria/bremerhaven"
folder_location = "/home/docker-hbv-kms/repositories/NodeJS_Server4Pepper/public/"

def getMensaData():
    try:
        #download newest cafeteria plan
        response = requests.get(url)
        soup= BeautifulSoup(response.text, "html.parser")
        #create url string
        menucard = ((str(soup.select("a[href$='/print']")[0]).rsplit(' target', 1)[0]).split("href=",1)[1]).replace('"','')
        urllib.request.urlretrieve(menucard, folder_location+"Mensaplan.pdf")
        print("pdf downloaded")

        #pdf to img
        img = convert_from_path(folder_location+"Mensaplan.pdf", 500)[0]
        #crop image
        area = (0, 200, 4134, 2800) # R T L B
        cropped_img = img.crop(area)

        area = (0, 5200, 4134, 5800)
        cropped_img2 = img.crop(area)

        mergeImgs([cropped_img, cropped_img2]).save(folder_location+'images/mensaplan.png', 'JPEG')

        print("images created from pdf")

        #get all tbody tags from the site
        menulist = soup.select("tbody")

        menu = {}
        day = ["Montag","Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
        offer1 = []
        offer2 = []

        for i in range(10):
            tmp = (str(menulist[i]).split('description">',1)[1]).rsplit("</td><td",2)[0]
            tmp = tmp.replace("\n","").replace("\r","").replace("a1","").replace("amp;","")
            tmp = re.sub('<sup>.*?</sup>', '', tmp)
            if(i%2==0):
                offer1.append(tmp)
            else:
                offer2.append(tmp)
        menu["day"] = day
        menu["offer1"] = offer1
        menu["offer2"] = offer2


        with open(folder_location+"mensadata.json", "w+") as f:
            json.dump(menu, f, ensure_ascii=False)
        print("menu dataframe created")

    except Exception:
        traceback.print_exc()


def mergeImgs(imgs):
    min_img_width = min(i.width for i in imgs)

    total_height = 0
    for i, img in enumerate(imgs):
        # If the image is larger than the minimum width, resize it
        if(img.width > min_img_width):
            imgs[i] = img.resize((min_img_width, int(img.height / img.width * min_img_width)), Image.ANTIALIAS)
        total_height += imgs[i].height

    img_merge = Image.new(imgs[0].mode, (min_img_width, total_height))
    y = 0
    for img in imgs:
        img_merge.paste(img, (0, y))

        y += img.height
    return img_merge

getMensaData()