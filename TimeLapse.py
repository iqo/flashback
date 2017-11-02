import os
from time import sleep
from datetime import datetime
from picamera import PiCamera

def timeLapse(timeInterval):
    camera = PiCamera()
    camera.hflip = True
    camera.vflip = True

    startYear = "%04d" % (datetime.now().year)
    startMonth = "%02d" % (datetime.now().month)
    startDay = "%02d" % (datetime.now().day)
    startHour = "%02d" % (datetime.now().hour)
    startMinutes = "%02d" % (datetime.now().minute)
    cwd = os.getcwd()
    fileNumber = 1


    pictureFolder = "flashback." + str(startYear)  + "." + str(startMonth) + "." + str(startDay)  + "." + str(startHour) + "." +  str(startMinutes)
    if not(os.path.exists(str(cwd) + '/pictures')):
        os.mkdir('pictures')

    if not(os.path.exists(str(cwd) + '/pictures/' + str(pictureFolder))):
        os.mkdir(str(cwd) +"/pictures/"  + pictureFolder)

    while(True):
        fileSerialNumber = "%04d" % (fileNumber)
        currentYear = "%04d" % (datetime.now().year)
        currentMonth = "%02d" % (datetime.now().month)
        currentDay = "%02d" % (datetime.now().day)
        currentHour = "%02d" % (datetime.now().hour)
        currentMinutes = "%02d" % (datetime.now().minute)
        camera.start_preview()
        sleep(5)
        camera.capture(str(cwd) + '/pictures/' + str(pictureFolder) + '/' +str(fileSerialNumber) + '_' + str(currentYear) + '.'+str(currentMonth) + '.' + str(currentDay) +'.' +str(currentHour)+ '.' +str(currentMinutes)  + '.jpg')

        camera.stop_preview()
        fileNumber = fileNumber + 1
        sleep(timeInterval)



    
timeLapse(25)
