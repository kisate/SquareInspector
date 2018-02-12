from imutils.perspective import four_point_transform
from imutils import contours as cnts
import numpy as np
import imutils
import cv2

class BigContourError(ValueError):
        pass
class MarkContoursError(ValueError):
        pass

DEBUG = False

def inspect (path, contours) :
        
        im = cv2.imread(path, 0)
        h, w = im.shape
        im = im[0:int(h*0.114), 0:w]

        cont = contours['Big Contour']

        markConts = contours['Mark Contours']
        
        cropped = four_point_transform(im, cont.reshape(4, 2))

        ret, thresh = cv2.threshold(cropped, 0, 255, cv2.THRESH_OTSU)

        if DEBUG :
                im2 = cropped.copy()
                cv2.drawContours(im2, markConts, -1, 0, 2)
                cv2.imshow('image', im2)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        
        marked = None
        for i, c in enumerate(markConts):
                
                mask = np.zeros(thresh.shape, dtype="uint8")
                
                cv2.drawContours(mask, [c], -1, 255, -1)

                mask = cv2.bitwise_and(thresh, thresh, mask=mask)

                total = cv2.countNonZero(mask)

                if marked is None or total < marked[0]:
                       marked = (total, i)
        return marked[1]

