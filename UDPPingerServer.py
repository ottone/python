# UDPPingerServer.py
# We will need the following module to generate andomized lost packets
import random 
from socket import *

# Create UDP Socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP Address  and port number to socket
serverSocket.bind(('', 12000))

while True:
	# Generate random number in the range of 0 to 10
	rand = random.randint(0,10)
	
	# Receive the client packet along with the address it is coming from 
	message, address = serverSocket.recvfrom(1024)
	
	# Capitalize the message from the client
	message = message.upper()
	
	# If rand is less then 4, we consider the packet lost and do not respod 
	if rand < 4:
		continue
	# Otherwise, the server responds. The server sits in an infinete loop listening for incoming UDP packets.
	serverSocket.sendto(message, address)