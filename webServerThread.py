#Skeleton Python Code for the Web Server

import os
import _thread
#import socket module
#import os,thread
from socket import *
import sys          # In order to terminate the program

#************ CONSTANT VARIABLES **************
BACKLOG = 10 				# How many pending connections queue will hold
MAX_DATA_RECV = 2048		# Max number of bytes we receive at once

# Assign a port number
serverPort = 6789

def proxy_thread(conn, client_addr):
	
	try:
		# Get the request from browser
		request = conn.recv(MAX_DATA_RECV).decode()
		# print request message
		print('Request Message:', request)
		# parse the first line
		filename = request.split()[1]
		print('filename is:', filename[1:])
		filepath = "C:\\Users\\Francesco\\Documents\\GitHub\\python\\"
		print('Percorso + Filename :',filepath+filename[1:])
		f = open(filepath+filename)
		# Store the entire content of the requested  file in a temporary buffer
		outputdata = f.read()
		#Send one HTTP response header line into socket
		conn.send("HTTP/1.1 200 OK\r\n\r\n".encode())
		#Send the content of the requested file to the client
		for i in range(0, len(outputdata)):
			conn.send(outputdata[i].encode())
		conn.send("\r\n".encode())
		# Close the client connection socket
		conn.close()
		
	except IOError:
		# Send responce message for file not found
		conn.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
		conn.send("<html><head>File not found</head><body><h1>File not Found</h1></body></html>".encode())
		# Close client socket
		conn.close()
		


# Create a TCP  server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

#print ('hostname is: ', gethostname())
#Prepare a sever socket. Bind the socket to server address and server port 
serverSocket.bind(('',serverPort))

# Listen to at most 1  connection at a time
serverSocket.listen(BACKLOG)

#Establish the connection
print('Ready to serve...')

# Server should be up and running and listening to the incoming connections
while True:
	# Set up the connection from the client
	conn, client_addr = serverSocket.accept()
	# create a thread to handle request
	_thread.start_new_thread(proxy_thread,(conn, client_addr))
	
serverSocket.close()

#******************* END MAIN PROGRAM ******************

#*******************************************************
#*************** PROXY_THREAD FUNC *********************
# A thread to handle request from browser **************
#*******************************************************
	

		
	# If an exception occurs during the execution of try clause
	# the rest of the clause is skipped
	# If the exception type matches the word after except 
	# the except clause is execute
	
	#try:
			# Receives the request message from the client
	#		message = connectionSocket.recv(2048)
			#print ('Message is:' , message)
			# Extract the path  of the requested object from the message
			# The path is the second part of HTTP header, identified by [1]
			#filename = message.split()[1]
			#print('filename is:', filename)
			# Becuase the extracted path of the HTTP request includes
			# a character '/', we read the path from the second caracter 
			#f = open(filename[1:])
			# Store the entire content of the requested  file in a temporary buffer
			#outputdata = f.read()
			#Send one HTTP response header line into socket
			#connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
			#Send the content of the requested file to the client
			#for i in range(0, len(outputdata)):
			#	connectionSocket.send(outputdata[i].encode())
			#connectionSocket.send("\r\n".encode())
			# Close the client connection socket
			#connectionSocket.close()
	#except IOError:
			#Send response message for file not found
	#		connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
	#		connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
			#Close client socket
	#		connectionSocket.close()

serverSocket.close()
sys.exit()
#Terminate the program after sending the corresponding data 