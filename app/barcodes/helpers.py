from pyzbar.pyzbar import decode
import numpy as np
import cv2

def getBarcode(pathBarcode):
    result = decode(cv2.imread(pathBarcode))
    return result[0].data if result else False

