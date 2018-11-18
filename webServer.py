#Skeleton Python Code for the Web Server

#import socket module
from socket import *
# import socket     # Aletenative (better) syntax  
import sys          # In order to terminate the program

# Create a TCP  server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 6789

print ('hostname is: ', gethostname())
#print ('hostname is: ', socket.gethostname()) # Alternative (better) syntax

#Prepare a sever socket. Bind the socket to server address and server port 
serverSocket.bind(('',serverPort))
# or 
# serverSocket.bind((gethostname(), serverPort))
# serverSocket.bind(socket.gethostname(), serverPort())   # Alternative (better) syntax

# Listen to at most 1  connection at a time
serverSocket.listen(1)


# Server should be up and running and listening to the incoming connections
while True:
	#Establish the connection
	print('Ready to serve...')
	
	# Set up the connection from the client
	connectionSocket, addr = serverSocket.accept()
	
	# If an exception occurs during the execution of try clause
	# the rest of the clause is skipped
	# If the exception type matches the word after except 
	# the except clause is execute
	
	try:
			# Receives the request message from the client
			message = connectionSocket.recv(2048).decode()
			print ('Message is:' , message)
			# Extract the path  of the requested object from the message
			# The path is the second part of HTTP header, identified by [1]
			filename = message.split()[1]
			print('filename is:', filename)
			# Becuase the extracted path of the HTTP request includes
			# a character '/', we read the path from the second caracter 
			f = open(filename[1:])
			# Store the entire content of the requested  file in a temporary buffer
			outputdata = f.read()
			#Send one HTTP response header line into socket
			connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
			#Send the content of the requested file to the client
			#for i in range(0, len(outputdata)):
				#connectionSocket.send(outputdata[i].encode())
			connectionSocket.send(outputdata.encode())
			#connectionSocket.send("\r\n".encode())
			# Close the client connection socket
			connectionSocket.close()
	except IOError:
			#Send response message for file not found
			connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
			connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
			#Close client socket
			connectionSocket.close()

serverSocket.close()
sys.exit()
#Terminate the program after sending the corresponding data 
