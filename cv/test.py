import cv2
import numpy as np
import pytesseract

# img = cv2.imread('image.jpg')

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
mn = 0b00000001
mx = 0b10000000
def t(pixel):
    return bool((pixel & mx)) or ( not (pixel & mn))

def tt(row):
    for i in row:
        row[i] = t(i)

#thresholding
def thresholding(image):
    img = get_grayscale(image)
    r, c = img.shape
    for ri in range(0,r):
        for ci in range(0,c):
            img[ri][ci] = t(img[ri][ci])
    # return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return img

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)



from pytesseract import Output
image = cv2.imread('testxx.PNG')

# gray = get_grayscale(image)
# thresh = thresholding(image)
# opening = opening(gray)
# canny = canny(gray)

img = get_grayscale(image)

# cv2.contrastStretching(img, image, 0, 0, img[0].size(), img.size())



h, w = img.shape
d = pytesseract.image_to_data(img, output_type=Output.DICT) 


n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


cv2.imshow('img', img)
cv2.waitKey(0)