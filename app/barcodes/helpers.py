from pyzbar.pyzbar import decode
import numpy as np
import cv2
from PIL import Image, ImageFile
from . import keys
import requests
import json
from barcodes.models import Barcode

def initBarcodes():
    # NUM_DATA is from below website
    # http://www.sdfi.co.kr/foodsafetykorea/list.asp?fs_id=C005&start_page=1&show_cnt=50
    NUM_DATA = 100844
    total = NUM_DATA//1000 if NUM_DATA%1000 == 0 else NUM_DATA//1000+1
    for i in range(total):
        print("{}/{}".format(i+1,total))
        url = 'http://openapi.foodsafetykorea.go.kr/api/{}/C005/json/{}/{}'.format(keys.BARCODE_KEY, i*1000+1, (i+1)*1000)
        response = requests.get(url)
        while response.status_code != 200:
            print(i+1,"FAILD", response.status_code)
            response = requests.get(url)
        result = json.loads(response.text)
        C005 = result['C005']
        rows = C005['row']
        for index, row in enumerate(rows):
            print(index, row['PRDLST_NM'])
            if len(row["END_DT"]) < 4 and len(row["CLSBIZ_DT"]) < 4:
                newEntry = Barcode(name=row['PRDLST_NM'], barcode=row["BAR_CD"])
                newEntry.save()

def djangoImg2Barcode(request):
    if Barcode.objects.all().count() < 10:
        initBarcodes()
    f = request.FILES.get('barcode')
    p = ImageFile.Parser()
    while 1:
        s = f.read(1024)
        if not s:
            break
        p.feed(s)
    img = p.close()
    result = decode(img)
    return result[0].data[:13] if result else False

def getBarcode(pathBarcode):
    result = decode(cv2.imread(pathBarcode))
    return result[0].data[:13] if result else False

def getBarcodeInformation(pathBarcode):
    barcode = getBarcode(pathBarcode)
    if barcode == False:
        return False
    url = 'http://openapi.foodsafetykorea.go.kr/api/{}/C005/json/1/5'.format(keys.BARCODE_KEY)

def resizeImg(img, size):
    return img.resize(size)


"""
print(getBarcode('./ttt.jpg'))

exit()

from os import listdir
from os.path import isfile, join

path = '/home/blogharu/Projects/django/summary/ICDAR_2015/my_train'
pathSave = '/home/blogharu/Projects/django/summary/ICDAR_2015/my_resize_img'
for i, f in enumerate(listdir(path),1):
    print(f)
    img = Image.open(path+'/'+f)
    img = img.resize((1280,720))
    img.save(pathSave+f'/img_{i}.jpg')
"""