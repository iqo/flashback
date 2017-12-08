
# file: rfcomm-server.py auth: Albert Huang <albert@csail.mit.edu> desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $
import os
import sys
from multiprocessing import Process
from multiprocessing import Queue
#sys.path.append(os.path.abspath('/home/pi/Documents/progamming/github/flashback'))
#sys.path.append('/home/pi/Documents/progamming/flashback')
#sys.path.insert(0,'/home/pi/Documents/programming/github/flashback')
sys.path.insert(0,'/usr/share/doc/bluetooth')


from TimeLapse import timeLapse
from bluetooth import *

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print "Waiting for connection on RFCOMM channel %d" % port

client_sock, client_info = server_sock.accept()
print "Accepted connection from ", client_info

queue = Queue()
print(queue)
try:
    while True:
        data = client_sock.recv(1024)
	print(data)
        if len(data) == 0:
		break
        elif data == "10":
		print("Starting timelapsinterval  [%s]" % data) 
		child_thread = Process(target=timeLapse, args=(queue, 10))
		child_thread.start()
		print("kuk")
	elif data == "20":
		child_thread = Process(target=timeLapse, args=(queue, 20))
		child_thread.start()
	elif data == "30":
		child_thread = Process(target=timeLapse, args=(queue, 30))
		child_thread.start()
	elif (data == "0") or (data == "stop"):
		child_thread.terminate()
		child_thread.join()
	elif (data == "e"):
		break
except IOError:
    pass

print "disconnected"

client_sock.close()
server_sock.close()
print "all done"
