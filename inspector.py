from imutils.perspective import four_point_transform
from imutils import contours as cnts
import numpy as np
import imutils
import cv2

def inspect (path) :

        im = cv2.imread(path, 0)

        h, w = im.shape

        im = im[0:int(h*0.13), 0:w]
       
        ret, thresh = cv2.threshold(im, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        
        peri = cv2.arcLength(contours[1], True)

        approx = cv2.approxPolyDP(contours[1], 0.02 * peri, True)
        cont = approx

        im3 = four_point_transform(im, cont.reshape(4, 2))

        
        ret, thresh2 = cv2.threshold(im3, 127, 255, 0)
        im4, contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        im5 = thresh2.copy()
        cv2.drawContours(im5, contours, -1, 0, 1)

        # cv2.imshow('image', im5)
        
        markCnts = []
        for c in contours:
                (x, y, w, h) = cv2.boundingRect(c)
                ar = w / float(h)

                if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                        markCnts.append(c)
        markCnts = cnts.sort_contours(markCnts, method = "left-to-right")[0]

        
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
                       marked = (total, i//2)
        return marked[1]
