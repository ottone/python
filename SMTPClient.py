# Skeleton Python Code for the Mail Client

from socket import *

msg = "\r\n I love computer networks!" 
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver mailserver = #Fill in start #Fill in end
# Create socket called clientSocket and establish a TCP connection with mailserver

mailserver = input("Choose a mail server: ")
name = input("Inserire il nome utente : ")
port = 25

clientSocket = socket(AF_INET, SOCK_STREAM)
print("Connessione al server : " , mailserver, " porta :  " , port)

clientSocket.connect((mailserver,port))
recv = clientSocket.recv(1024).decode() 

if recv[:3] != '220':
	print('220 reply not received from server.')
else:
	print("Risposta del Server alla connessione :", recv)

# Send HELO command and print server response. 

heloCommand = 'HELO Alice\r\n'
print("Saluto server con :", heloCommand)

clientSocket.send(heloCommand.encode())

recv = clientSocket.recv(1024).decode() 

if recv[:3] != '250':
	print('250 reply not received from server.')
else:
	print("Risposta del Server : ", recv)
	
	
# Send MAIL FROM command and print server response.

mailfrom = 'MAIL FROM: <alice@local.com>\r\n'
print("Invio MAIL FROM al server : ", mailfrom)
clientSocket.send(mailfrom.encode())
recv = clientSocket.recv(1024).decode()

print(recv[:3])

if recv[:3] != '250':
	print('250 reply not received from server.')
else:
	print("Rispost del server al MAIL FROM : ", recv)
	
	
# Send RCPT TO command and print server response.

rcptto = 'RCPT TO: <bob@local.com>\r\n'  
print("Invio RCPT TO al server: ", rcptto)                                                                                             
clientSocket.send(rcptto.encode())                                                                                                        
recv = clientSocket.recv(1024).decode()                                                                                                    
 
 
if recv[:3] != '250':  
	print('250 reply not received from server.')
else:
	print("Risposta RCPT TO del Server", recv) 
	
# Send DATA command and print server response.

data = input("Data della mail :")

clientSocket.send('DATA\r\n\r\n'.encode())                                                                                                        
recv = clientSocket.recv(1024).decode()                                                                                                                                                                                                 
print("Risposta dal server :", recv)

if recv[:3] != '250':                                                                                                                      
	print('250 reply not received from server.')
else:
	print(recv)
	
# Send message data.
print ("Invio Messaggio : ", msg)
clientSocket.send(msg.encode())
recv = clientSocket.recv(1024).decode()
print("Risposta dopo invio messaggio ",recv)
clientSocket.send(endmsg.encode())                                                                                                        
print("Fine Messaggio con : ", endmsg)
recv = clientSocket.recv(1024).decode()                                                                                                  
print("Risposta al fine msg",recv)
                                                                                                                                                                                                                                                
if recv[:3] != '250':                                                                                                                      
	print('250 reply not received from server.')
else:
	print(recv)
	
# Message ends with a single period.

# Send QUIT command and get server response.

clientSocket.send('QUIT\r\n'.encode())                                                                                                        
recv = clientSocket.recv(1024).decode()                                                                                                    

if recv[:3] != '250':                                                                                                                      
	print('250 reply not received from server.')
else:
	print(recv)
