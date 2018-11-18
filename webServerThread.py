#Python Code for the Web Server with Thread

import os
import _thread
from socket import *
import sys              # In order to terminate the program

#**********************************************
#************ CONSTANT VARIABLES **************
#**********************************************

BACKLOG = 10 				# How many pending connections queue will hold
MAX_DATA_RECV = 2048			# Max number of bytes we receive at once

serverPort = 6789			# Assign a port number

#**********************************************
#************ FUNCTION PROXY_THREAD ***********
#**********************************************

def proxy_thread(conn, client_addr):

# If an exception occurs during the execution of try clause the rest of the clause is skipped
# If the exception type matches the word after except the except clause is execute

	
	try:
		# Get the request from browser
		request = conn.recv(MAX_DATA_RECV).decode()
		# print request message
		print('Request Message:', request)
		# The path is the second part of HTTP header, identified by [1]
		filename = request.split()[1]
		# Becouse the extracted path of the HTTP  request includes 
		# a charatcter '/', we read the path from the second caracter
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

#************ END FUNCTION PROXY_THREAD **********

# Create a TCP  server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

#print ('hostname is: ', gethostname())

serverSocket.bind(('',serverPort))        #Prepare a sever socket. Bind the socket to server address and server port 

serverSocket.listen(BACKLOG)              # Listen to at most 1  connection at a time

print('Ready to serve...')                # Establish the connection 

# Server should be up and running and listening to the incoming connections

while True:
	conn, client_addr = serverSocket.accept() 				# Set up the connection from the client
	_thread.start_new_thread(proxy_thread,(conn, client_addr)) 		# Create a thread to handle request
	
serverSocket.close()
sys.exit()

#Terminate the program after sending the corresponding data 
