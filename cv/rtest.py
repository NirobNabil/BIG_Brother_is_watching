import numpy as np
import cv2
import timeit
from matplotlib import pyplot as pt
import pytesseract 
from pytesseract import Output

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


mx = 0b11110000
mn = 0b11110000
# def t(p):
#     return ( not ( (not ((p & mx) ^ mx)) | (not (p & mn)) ) ) * 255

def t(p):
    return ( not ( (p > 240) | (p < 40) ) ) * 255

#thresholding
def thresholding(image):
    img = get_grayscale(image)
    # img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    r, c = img.shape
    for ri in range(0,r):
        for ci in range(0,c):
            img[ri][ci] = t(img[ri][ci])
    return img


image = cv2.imread('test_green.PNG')

thresh = thresholding(image)

pt.figure(1)
pt.imshow(thresh, cmap="gray")
# pt.figure(2)
# pt.imshow(get_grayscale( image), cmap="gray")
pt.show()

img = thresh
# d = pytesseract.image_to_data(img, output_type=Output.DICT)

# n_boxes = len(d['text'])
# for i in range(n_boxes):
#     if int(d['conf'][i]) > 60:
#         (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
#         img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# cv2.imshow('img', img)
# cv2.waitKey(0)

custom_config = r'--oem 3 --psm 6'
# x = pytesseract.image_to_string(img, config=custom_config)
# print()
# cv2.imshow('img', thresh)
# cv2.waitKey(0)