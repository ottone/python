# From socket import all module
from socket import *

serverPort = 6789

serverName = input("Inserisci l'indirizzo ip del server:")

# Inizio connessione con il server web
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

sentence = input('web page da richiedere:')

httpMessage="GET /"+sentence+" HTTP/1.1" 


clientSocket.send(httpMessage.encode())

modifiedSentence, serverAddress = clientSocket.recvfrom(999999)

message = modifiedSentence.decode()
print(message)
	
clientSocket.close()
