""" PyHeartBqeat server: receives and tracks UDP packets from all clients.

While the BeatLog thread logs each UDP packet in a dictionary, the main
thread periodically scans the dictionary and prints the IP addresses of the
clients that sent at least one packet during the run, but have
not sent any packet since a time longer than the definition of the timeout.

Adjust the constant parameters as needed, or call as:
    PyHBServer.py [timeout [udpport]]
"""

HBPORT = 43278
CHECKWAIT = 30

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
# DALLA MODULO THREADING IMPORTA LA CLASSE THREAD. IL MODULO THREADING DI PYTHON INCLUDE ANCHE UN SEMPLICE MECCANISCO DI LOCK,
# CHE PERMETTE DI IMPLEMENTARE LA SINCRONIZZAZIONE TRA I THREAD. 
from threading import Lock, Thread, Event  
from time import time, ctime, sleep
import sys

class BeatDict:
    "Manage heartbeat dictionary"
		
# IL METODO LOCK NON E' ALTRO CHE UN OGGETTO ACCESSIBILE DA PIU THREAD. TIPICAMENTE ACCESSIBILE CON IL METODO LOCK() DEFINITO 
# NEL MODULO THREADING. UNA VOLTA OTTENUTO IL LOCK SI POSSONO UTILIZZARE DUE METODI CHE PERMETTONO DI SINCRONIZZARE L'ESECUZIONE
# DI DUE THREAD: IL METODO ACQUIRE ED IL METODO RELEASE. 
    
	def __init__(self):
		self.beatDict = {}
		if __debug__:
			self.beatDict['127.0.0.1'] = time(  )
		self.dictLock = Lock(  ) 

# IL METODO ACQUIRE PER ACQUISIRE IL CONTROLLO DEL LOCK. ACCETTA UN PARAMETRO OPZIONALE CHE SE NON SPECIFICATO O IMPOSTATO A TRUE
# FORZA IL THREAD A SOSPENDERE LA SUA ESECUZIONE FINCHE IL LOCK VERRA' RILASCIATO E POTRA' QUINDI ESSERE ACQUISITO, SE INVECE IL
# METODO ACQUIRE VIENE ESETUITO CON ARGOMENTO PARI A FALSE ESSO RITORNA IMMEDIATAMENTE UN RISULTATO BOOLEANO CHE VALE TRUE SE IL
# LOCK E' STATO ACQUISITO OPPURE FALSE IN CASO CONTRARIO, IL METODO RELEASE PER RILASCIARE IL CONTROLLO DEL LOCK

    def __repr__ (self):
        list = ''
        self.dictLock.acquire(  )
        for key in self.beatDict.keys(  ):
		list = "%sIP address: %s - Last time: %s\n" % (
			list, key, ctime(self.beatDict[key]))
        self.dictLock.release(  )
        return list

# AQUISIZIONE LOCK, ESECUZIONE CODICE : PONE L'INDICE ENTRY DEL DIZIONARIO BEATDICT UGUALE AL VALORE RESTITUITO DA TIME()  E RILASCIO LOCK

    def update(self, entry):
        "Create or update a dictionary entry"
        self.dictLock.acquire(  )
        self.beatDict[entry] = time(  )
        self.dictLock.release(  )

# CREAZIONE DELLA LISTA SILENT  LISTA SERIE ORDINATA (CON INDICE) DI VALORI DI TIPO QUALSIASI.
# ACQUISIZIONE LOCK
# IL METODO KEYS() RITORNA LA LISTA DELLE CHIAVI DISPONIBILI NEL DIZIONARIO
# RILASCIO LOCK

    def extractSilent(self, howPast):
	    "Returns a list of entries older than howPast"
        silent = []
		when = time(  ) - howPast
		self.dictLock.acquire(  )
		for key in self.beatDict.keys(  ):
				if self.beatDict[key] < when:
					silent.append(key)
		self.dictLock.release(  )
        return silent

# LA CREAZIONE DI UN THREAD NECESSITA DELLA DEFINIZIONE DELLA SEGUENTE CLASSE CHE EREDITI DALLA CLASSE THREAD INCLUSA NEL MODULO THREADING
# LA CLASSE (BEATREC IN QUESTO CASO) DEVE RISPETTARE UNA PRECISA STRUTTURA DI SEGUITO RIPORTATA. QUINDI THREAD E' LA SUPER CLASSE

class BeatRec(Thread):
    "Receive UDP packets, log them in heartbeat dictionary"
	# METODO __INIT__  COSTRUTTORE DEL THREAD DICHIARA I PARAMETRI DI INIZIALIZZAZIONE 
    def __init__(self, goOnEvent, updateDictFunc, port):
        Thread.__init__(self)
        self.goOnEvent = goOnEvent
        self.updateDictFunc = updateDictFunc
        self.port = port
        self.recSocket = socket(AF_INET, SOCK_DGRAM)
        self.recSocket.bind(('', port))

    def __repr__(self):
        return "Heartbeat Server on port: %d\n" % self.port
	
	# METODO RUN 
    def run(self):
        while self.goOnEvent.isSet(  ):
            if __debug__:
                print "Waiting to receive..."
            data, addr = self.recSocket.recvfrom(6)
            if __debug__:
                print "Received packet from " + `addr`
            self.updateDictFunc(addr[0])

def main(  ):
    "Listen to the heartbeats and detect inactive clients"
    global HBPORT, CHECKWAIT
    if len(sys.argv)>1:
        HBPORT=sys.argv[1]
    if len(sys.argv)>2:
        CHECKWAIT=sys.argv[2]
	
	# L'OGGETTO EVENT() E' UN MECCANISMO PER LA COMUNICAZIONE TRA I THREADS UN THREAD SEGNALA UN EVENTO E UN ANLTRO EVENTO ASPETTA PER LUI
	# UN OGGETTO EVENTO GESTISCE UN FLAG INTERNO CHE PUO ESSERE SETTATO S TUE CON IL METODO SET() E SETTATO A FALSE CON IL METODO CLEAR()
	# IL METODO WAIT() CLOCCA IL THREAD FINCHE' IL FLAG INTERNO E' TRUE
    beatRecGoOnEvent = Event(  )    		
    beatRecGoOnEvent.set(  )
    beatDictObject = BeatDict(  )
	
    # CREAZIONE DEL THREAD 
	beatRecThread = BeatRec(beatRecGoOnEvent, beatDictObject.update, HBPORT)
    
	if __debug__:
        print beatRecThread	
    # AVVIO DEL THREAD. IL METODO START SI LIMITA AD ESEGUIRE IL CONTENUTO DEL METODO RUN CON PARAMTRI DI INIZIALIZZAZIONE  FORNITI
	# IL METODO START NON E' BLOCCANTE: QUANDO ESSO VIENE ESEGUITO IL CONTROLLO PASSA SUBITO ALLA RIGA SUCCESSIVA MENTRE IL THREAD
	# VIENE AVVIATO IN BACKGROUND
	beatRecThread.start(  )
    print "PyHeartBeat server listening on port %d" % HBPORT
    print "\n*** Press Ctrl-C to stop ***\n"
    while 1:
        try:
            if __debug__:
                print "Beat Dictionary"
                print `beatDictObject`
            silent = beatDictObject.extractSilent(CHECKWAIT)
            if silent:
                print "Silent clients"
                print `silent`
            sleep(CHECKWAIT)
        except KeyboardInterrupt:
            print "Exiting."
            beatRecGoOnEvent.clear(  )
			# TERMINE DEL THREAD
            beatRecThread.join(  )

if __name__ == '__main__':
    main(  )
