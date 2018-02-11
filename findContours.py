from imutils.perspective import four_point_transform
from imutils import contours as cnts
import numpy as np
import imutils
import cv2
import pickle

class BigContourError(ValueError):
        pass
class MarkContoursError(ValueError):
        pass


im = cv2.imread("blank.jpg", 0)

h, w = im.shape

im = im[0:int(h*0.114), 0:w]
blurred = cv2.GaussianBlur(im, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)


im2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



max_s = 0
cont = contours[1]
t = True
for c in contours :
        (x, y, w, h) = cv2.boundingRect(c)
        ph, pw = im.shape
        if not (w*h >= pw*ph*0.95) : 
                if w*h > max_s :
                        max_s = w*h
                        cont = c


peri = cv2.arcLength(cont, True)

approx = cv2.approxPolyDP(cont, 0.02 * peri, True)
cont = approx

try :
        im3 = four_point_transform(im, cont.reshape(4, 2))
except ValueError:
        raise BigContourError

ret, thresh2 = cv2.threshold(im3, 0, 255, cv2.THRESH_OTSU)
im4, contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

markConts = []

for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        if w >= 35 and h >= 35 and ar >= 0.9 and ar <= 1.1:
                markConts.append(c)
                
markConts = cnts.sort_contours(markConts, method = "left-to-right")[0]


        
if len(markConts) != 33 :
        raise MarkContoursError

f = open('contours.cnt', 'wb')
contoursToWrite = {'Big Contour' : cont, 'Mark Contours' : markConts}
pickle.dump(contoursToWrite, f)
f.close()

