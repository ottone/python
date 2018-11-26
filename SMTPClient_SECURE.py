# Skeleton Python Code for the Mail Client 
# USING STARTTLS

from socket import *

msg = "\r\n I love computer networks!" 
endmsg = "\r\n.\r\n"
mailserver = 'smtp.gmail.com'
port = 587

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver,port))
recv = clientSocket.recv(1024).decode() 
if recv[:3] != '220':
	print('220 reply not received from server.')
else:
	print("Risposta del Server alla connessione :", recv)

# Send HELO command and print server response. 
input = ("Send an HELO command...")
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv = clientSocket.recv(1024).decode() 
if recv[:3] != '250':
	print('250 reply not received from server.')
else:
	print("Risposta del Server : ", recv)
	
# Send MAIL FROM command and print server response.
command = 'STARTTLS\r\n'
clientSocket.send(command.encode())
recv = clientSocket.recv(1024).decode()
print("Risposta del Server al comando STARTTLS: ", recv)
mailfrom = 'MAIL FROM: <alice@local.com>\r\n'
print("Invio MAIL FROM al server : ", mailfrom)
clientSocket.send(mailfrom.encode())
recv = clientSocket.recv(1024).decode()

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
