import os
from time import sleep
from datetime import datetime
from picamera import PiCamera
from multiprocessing import Queue

def timeLapse(queue, timeInterval):
    camera = PiCamera()
    queue.put("started timelaps")
    print(queue)
 #   camera.hflip = True
#    camera.vflip = True

    startYear = "%04d" % (datetime.now().year)
    startMonth = "%02d" % (datetime.now().month)
    startDay = "%02d" % (datetime.now().day)
    startHour = "%02d" % (datetime.now().hour)
    startMinutes = "%02d" % (datetime.now().minute)
    cwd = os.getcwd()
    fileNumber = 1
    killFlag = 0


    pictureFolder = "flashback." + str(startYear)  + "." + str(startMonth) + "." + str(startDay)  + "." + str(startHour) + "." +  str(startMinutes)
    if not(os.path.exists(str(cwd) + '/pictures')):
        os.mkdir('pictures')
        #os.chmod('pictures', 777) 

    if not(os.path.exists(str(cwd) + '/pictures/' + str(pictureFolder))):
        os.mkdir(str(cwd) +"/pictures/"  + pictureFolder)
       # os.chmod('pictures/'+ str(pictureFolder), 777) 
    while(True):
        fileSerialNumber = "%04d" % (fileNumber)
        currentYear = "%04d" % (datetime.now().year)
        currentMonth = "%02d" % (datetime.now().month)
        currentDay = "%02d" % (datetime.now().day)
        currentHour = "%02d" % (datetime.now().hour)
        currentMinutes = "%02d" % (datetime.now().minute)
        #camera.start_preview()
        #sleep(5)
        camera.capture(str(cwd) + '/pictures/' + str(pictureFolder) + '/' +str(fileSerialNumber) + '_' + str(currentYear) + '.'+str(currentMonth) + '.' + str(currentDay) +'.' +str(currentHour)+ '.' +str(currentMinutes)  + '.jpg')

        #camera.stop_preview()
        fileNumber = fileNumber + 1
	print("picture")
        sleep(timeInterval)

    
#timeLapse(5)
