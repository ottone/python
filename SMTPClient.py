# Skeleton Python Code for the Mail Client

from socket import *

msg = "\r\n I love computer networks!" endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver mailserver = #Fill in start #Fill in end
# Create socket called clientSocket and establish a TCP connection with mailserver

mailserver = input("Choose a mail server: ")
name = ("Inserire il nome utente : ")
port = 25

msg = "HELO " + name 

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((mailserver,port))

#clientSocket.send(msg.encode()) 

recv = clientSocket.recv(1024).decode() 

print(recv)

if recv[:3] != '220':
	print('220 reply not received from server.')

# Send HELO command and print server response. 

heloCommand = 'HELO Alice\r\n'

clientSocket.send(heloCommand.encode())

recv1 = clientSocket.recv(1024).decode() 

print(recv1)

if recv1[:3] != '250':
	print('250 reply not received from server.')

# Send MAIL FROM command and print server response.

mailfrom = 'MAIL FROM: <alice@local.com>\r\n'
clientSocket.send(mailfrom.encode())
recv2 = clientSocket.recv(1024).decode()

print(recv2)

if recv2[:3] != '250':
	print('250 reply not received from server.')

# Send RCPT TO command and print server response.

rcptto = 'RCPT TO: <bob@local.com>\r\n'                                                                                               
clientSocket.send(mailfrom.encode())                                                                                                        
recv3 = clientSocket.recv(1024).decode()                                                                                                    
                                                                                                                                             
print(recv3)                                                                                                                                
                                                                                                                                              
if recv3[:3] != '250':                                                                                                                      
	print('250 reply not received from server.')

# Send DATA command and print server response.
# Fill in start
# Fill in end

# Send message data.
# Fill in start
# Fill in end

# Message ends with a single period.
# Fill in start
# Fill in end

# Send QUIT command and get server response.
# Fill in start
# Fill in end

