import inspector 
import glob, os
from shutil import copyfile
import os, errno

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

for file in glob.glob("tocheck/*.jpg") :
    if i == 0 :
        try :
            n = inspector.inspect(str(file))
            last = str(n)
            copyfile(file, 'sorted/{}/{}'.format(n, file[8:]))
        except inspector.BigContourError :
            print('Big contour error : ' + file)
            copyfile(file, 'sorted/error/{}'.format(file[8:]))
            last = 'error'
        except inspector.MarkContoursError :
            print('Mark contours error : ' + file)
            copyfile(file, 'sorted/error/{}'.format(file[8:]))
            last = 'error'
        i=1
    else :
        i = 0
        copyfile(file, 'sorted/{}/{}.jpg'.format(last, file[8:]))
        
    j+=1
##s = "Scan_0023.jpg"
##print(s + " " + str(inspector.inspect(s)))

        
