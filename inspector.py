from imutils.perspective import four_point_transform
from imutils import contours as cnts
import numpy as np
import imutils
import cv2

def inspect (path) :
        
        im = cv2.imread(path, 0)

        h, w = im.shape

        im = im[0:int(h*0.114), 0:w]
        blurred = cv2.GaussianBlur(im, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)
       
        ret, thresh = cv2.threshold(edged, 200, 255, 0)
        im2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #cv2.drawContours(im, contours, 215, 0, 3)
        

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
        
        approx = cv2.approxPolyDP(cont, 0.03 * peri, True)
        cont = approx

        im3 = four_point_transform(im, cont.reshape(4, 2))

        
        ret, thresh2 = cv2.threshold(im3, 0, 255, cv2.THRESH_OTSU)
        im4, contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        markCnts = []
        
        for c in contours:
                (x, y, w, h) = cv2.boundingRect(c)
                ar = w / float(h)

                if w >= 35 and h >= 35 and ar >= 0.9 and ar <= 1.1:
                        markCnts.append(c)
        markCnts = cnts.sort_contours(markCnts, method = "left-to-right")[0]

        if len(markCnts) != 33 :
                raise ValueError
        
##        for c in markCnts :
##                a = im4.copy()
##                (x, y, w, h) = cv2.boundingRect(c)
##                print(str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + ' ')
##                cv2.drawContours(a, [c], -1, 0, 3)
##                cv2.imshow('image', a)
##                cv2.waitKey(0)
##                cv2.destroyAllWindows()
        
        ret, thresh3 = cv2.threshold(im3, 0, 255, cv2.THRESH_OTSU)

        marked = None
        for i, c in enumerate(markCnts):
                
                mask = np.zeros(thresh3.shape, dtype="uint8")
                
                cv2.drawContours(mask, [c], -1, 255, -1)

##                cv2.imshow('image', mask)
##                cv2.waitKey(0)
##                cv2.destroyAllWindows()
                
                mask = cv2.bitwise_and(thresh3, thresh3, mask=mask)

##                cv2.imshow('image', mask)
##                cv2.waitKey(0)
##                cv2.destroyAllWindows()
                
                total = cv2.countNonZero(mask)

                if marked is None or total < marked[0]:
                       marked = (total, i)
        return marked[1]

