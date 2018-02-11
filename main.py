import inspector 
import glob, os
from shutil import copyfile
import os, errno
import pickle

for i in range(33):
    try:
        os.makedirs("sorted/{}".format(i))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
try:
    os.makedirs("sorted/error")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
i = 0
last = ''
j = 0

files = glob.glob("tocheck/*.jpg")
ammount = len(files)

f = open('contours.cnt', 'rb')    
contours = pickle.load(f)
f.close()

for file in  files:
    if i == 0 :
        
        n = inspector.inspect(str(file), contours)
        last = str(n)
        copyfile(file, 'sorted/{}/{}'.format(n, file[8:]))
        
        i=1
    else :
        i = 0
        copyfile(file, 'sorted/{}/{}'.format(last, file[8:]))
    j+=1
    if j % 5 == 0 : print("{0:.02f}%".format(j/ammount*100))
print('Done')

        
