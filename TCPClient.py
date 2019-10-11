from socket import *
serverName = '127.0.0.1'
serverPort = 12000
while True:
  clientSocket = socket(AF_INET, SOCK_STREAM)
  clientSocket.connect((serverName, serverPort))
  sentence = input('Frase in minuscolo:')
  clientSocket.send(sentence.encode())
  modifiedSentence, serverAddress = clientSocket.recvfrom(2048)
  print(modifiedSentence.decode())
  clientSocket.close()
