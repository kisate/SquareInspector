from imutils.perspective import four_point_transform
from imutils import contours as cnts
import numpy as np
import imutils
import cv2

class BigContourError(ValueError):
        pass
class MarkContoursError(ValueError):
        pass

def inspect (path, contours) :
        
        im = cv2.imread(path, 0)
        h, w = im.shape
        im = im[0:int(h*0.114), 0:w]

        cont = contours['Big Contour']

        markConts = contours['Mark Contours']
        
        im3 = four_point_transform(im, cont.reshape(4, 2))

        ret, thresh3 = cv2.threshold(im3, 0, 255, cv2.THRESH_OTSU)

        marked = None
        for i, c in enumerate(markConts):
                
                mask = np.zeros(thresh3.shape, dtype="uint8")
                
                cv2.drawContours(mask, [c], -1, 255, -1)

                mask = cv2.bitwise_and(thresh3, thresh3, mask=mask)

                total = cv2.countNonZero(mask)

                if marked is None or total < marked[0]:
                       marked = (total, i)
        return marked[1]

