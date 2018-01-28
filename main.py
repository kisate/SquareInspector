import inspector 
import glob, os
from shutil import copyfile
i = 0
last = ''
j = 0
for file in glob.glob("tocheck/*.jpg") :
    if i == 0 :
        try :
            n = inspector.inspect(str(file))
            last = str(n)
            copyfile(file, 'sorted/{}/{}.jpg'.format(n, j))
        except ValueError :
            print('Error : ' + file)
            copyfile(file, 'sorted/error/{}.jpg'.format(j))
            last = 'error'
        i=1
    else :
        i = 0
        copyfile(file, 'sorted/{}/{}.jpg'.format(last, j))
        
    j+=1
##s = "Scan_0023.jpg"
##print(s + " " + str(inspector.inspect(s)))

        
