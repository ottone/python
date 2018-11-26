#""" PYHEARTBEAT CLIENT: SENDS AN UDP PACKET TO A GIVEN SERVER EVERY 10 SECONDS
#    ADJUST THE CONSTANT PARAMENTER AS NEEDED, OR CALL AS: PYHBCLIENT.PY SERVERIP  [UDPPORT]
#"""

from socket import *
from time import time, ctime, sleep
import sys

SERVERIP = '127.0.0.1'		#	LOCAL HOST, JUST FOR TESTING
HBPORT = 43278				# 	AN ARBITRARY UDP PORT
BEATWAIT = 10 				# 	NUMBER OF SECONDS BETWEEN HEARTBEATS

if len(sys.argv) > 1:
	SERVERIP=sys.argv[1]

if len(sys.argv) > 2:
	HBPORT=int(sys.argv[2])
	
hbsocket = socket(AF_INET, SOCK_DGRAM)
print('HBClient sending to IP: ', SERVERIP , 'port :', HBPORT)
print('\n*** Press Ctrl - C to terminate ***\n')

while 1:
	hbsocket.sendto('Thump!', (SERVERIP,HBPORT))
	if __debug__:
		print('Time: ' , ctime(time()))
	sleep(BEATWAIT)
		
