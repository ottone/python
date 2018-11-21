""" HBServer : receives and tracks UDP packets from alla clients
    While the BeatLog thread logs each UDP packet in a dictionary, the main
	thread periodically scans the dictionary and prints the IP addresses of the
	clients that sent at least one packet during the run, but have
	not sent any packet since a time longer than the definition of the timeout.
	
	Adjust the constant paramenters as needed, or call as: 
	HBServer.py [timeout [udpport]]
"""

HBPORT = 43278
CHECKWAIT = 30

from socket import socket, gethostbyname
from threading import Look, Thread, Event
from time import time, ctime, sleep
import sys

class BeatDict:
	"Manage heartbeat Dictionary"
	
	def __init__(self):
		self.beatDict = {}
		if __debug__:
			self.beatDict['127.0.0.1'] = time()
		self.beatDict = Lock()
	
	def __repr__(self)
		list = ''
		self.dictLock.aquire()
		for key in self.beatDict.keys():
			list = "%sIP address: %s - Last time: %s\n" % (list, key, ctime(self.beatDict[key]))
		self.dictLock.release()
		return list
	
	def update(self, entry):
		"Create or update a dictionary entry"
		self.dictLock.aquire()
		self.beatDict[entry] = time()
		self.dictLock.release()
		
	def extractSelent(self, howPast):
		"Return a list of entries older than howPast"
		silent = []
		when = time() - howPast
		self.dictLock.acquire()
		for key in self.beatDict.keys():
			if self.beatDict[key] < when:
				silent.append(key)
		self.dictLock.release()
		return silent
		
	class BeatRec(Thread):
		"Receive UDP packets, log them in heartbeat dictionary"
		
		def __init__ (self, goOnEvent, uppdateDictFunc, port):
			Thread.__init__(self)
			self.goOnEvent = goOnEvent
			self.updateDictFunc = updateDictFunc
			self.port = prot
			self.recSocket = socket(AF_INET, SOC_DGRAM) 
			self.recSocket.bind(('', port))
			
		def __repr__ (self):
			return "HeartBeat Server on port: %d\n" % self.port
			
		def run(self):
			while self.goOnEvent.isSet():
				if __debug__:
					print"Receivingpacket from" + 'addr'
				self.updateDictFunc(addr[0])
				
	def main():
	
	"Listen to the heartbeats and detect inactive clients"
	
	global HBPORT, CHECWAIT
	if len(sys.argv)>1:
		HBPORT=sys.argv[1]
		
	if len(sys.argb)>2:
		CHECKWAIT = sys.argv[2]
		
	beatRecGoOnEvent = Event()
	beatRecGoOnEvent.set()
	beatDictObject = BeatDict()
	beatRecThread = BeatRec(beatRecGoOnEvent, beatDictObject.update, HBPORT)
	if __debug__:
		print beatRecThread
	beatReThread.start()
	print "HBServer listening on port %d" % HBPORT
	print "\n*** Press Ctrl-C to stop  ***\n"
	while 1: 
		try:
			if __debug__: 
				print "Best Dictionary"
				print 'beatDictObject'
			silent = beatDictObject.extractSilent(CHECKWAIT)
			if silent:
				print "Silent clients"
				print 'silent'
			sleep(CHECKWAIT)
		except KeyboardInterrupt:
			print "Exiting."
			beatRecGoOnEvent.clear()
			beatRecThread.join()
			
if __name__ == '__main__':
	main()