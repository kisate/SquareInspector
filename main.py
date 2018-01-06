from imutils.perspective import four_point_transform
from imutils import contours as cnts
import numpy as np
import imutils
import cv2

# Загружаю изображение сразу в ч/б, размываю, чтобы убрать шум
im = cv2.imread('examples/crosses2.jpg', 0)
im = cv2.GaussianBlur(im, (5, 5), 0)

# Делаю бинарным и нахожу границы
ret, thresh = cv2.threshold(im, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Оставляю только область с самими квадратиками (2 по величине)
peri = cv2.arcLength(contours[1], True)

approx = cv2.approxPolyDP(contours[1], 0.02 * peri, True)
cont = approx

im3 = four_point_transform(im, cont.reshape(4, 2))

# Снова делаю бинарным и нахожу границы
ret, thresh2 = cv2.threshold(im3, 127, 255, 0)
im4, contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Нахожу границы квадратиков по отношению сторон и их минимальному размеру
markCnts = []
for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                markCnts.append(c)

# Получаю более контрастное бинарное изображение 
ret, thresh3 = cv2.threshold(im3, 0, 255, cv2.THRESH_OTSU)

# Сортирую квадратики сверху вниз
markCnts = cnts.sort_contours(markCnts, method = "top-to-bottom")[0]

# Нахожу квадратик с крестиком по минимальному количеству
# белых пикселей на изображении после наложения маски

marked = None
for i, c in enumerate(markCnts):
        
        mask = np.zeros(thresh3.shape, dtype="uint8")
        
        cv2.drawContours(mask, [c], -1, 255, -1)
        
        mask = cv2.bitwise_and(thresh3, thresh3, mask=mask)
        
        total = cv2.countNonZero(mask)

        if marked is None or total < marked[0]:
               marked = (total, i)
print(marked)
