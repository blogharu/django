from pyzbar.pyzbar import decode
import numpy as np
import cv2

print(decode(cv2.imread('./download.png')))
