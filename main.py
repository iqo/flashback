from multiprocessing import Process
from multiprocessing import Queue
import time
import os

def child_func(queue, interval):

    print "Child Started"
    # put anything into queue after `child_func` get invoked, indicates
    # your child process is working
    queue.put("started...")  
    i = 0
    while True:
        file = open("testfile.txt","a")
        file.write(str(i)+" : ")
        time.sleep(1)
        i += 1
        file.close()


if __name__ == '__main__':

    queue = Queue()
    #child_thread = Process(target=child_func,args=(queue,))
    #child_thread.start()

    # stop sleeping until queue is not empty
    #while queue.empty():
    #    time.sleep(2)
    print "Parent Starting Process"

    while True:
        var = raw_input("First: ")
        if (var == "timelaps"):
            interval = raw_input("Time: ")
            child_thread = Process(target=child_func, args=(queue, interval))
            child_thread.start()
        if (var == "stop"):
            print "Parent Done"
            child_thread.terminate()
            print "Child Cancelled by Parent"
            child_thread.join()
        elif(var == "exit"):
            break
        else:
            continue

