# MODULES

from socket import *
import sys, time

# VARIABLES

MESSAGE = "ping"
serverName = '127.0.0.1'
serverPort = 12000
loss = 0
min_rtt = 1
max_rtt = 0
average_rtt = 0
count = 0
# CREATE UDP CLIENT SOCKET
clientSocket = socket(AF_INET , SOCK_DGRAM)

# SET PACKET TIMEOUT TO 2 SECONDS. AFTER THAT THE CLIENT DROP DOWN THE LISTENING
clientSocket.settimeout(2)

#############################
######## MAIN PROGRAM #######
#############################

# FOR CYCLE TO MANAGE THE 10 UDP PACKETS
for i in range(1,11):
# TRY CONDITION NEEDED TO MANAGE THE EXCEPTION OF PACKET TIMEOUT 
	try:
		# TAKE TRACE OF INITIAL TIMESTAMP
		send_time_ms = int(round(time.time() * 1000))
		print('send_time_ms: ' ,send_time_ms)
		# SEND THE PACKET ENCODED TO THE SERVER serverName AND PORT serverPort
		clientSocket.sendto(MESSAGE.encode(),(serverName, serverPort))
		
		# RECEIVE THE PACKET RETURNED
		modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
		
		# TAKE TIMESTAMP OF PACKET
		recv_time_ms = int(round(time.time() * 1000))
		print('recv_time_ms: ' ,recv_time_ms)
		# CALCULATE THE RTT
		rtt_in_ms = round(recv_time_ms - send_time_ms, 3)
		
		# MINIMUM RTT : SIMPLE METHOD TO USE TERNARY OPERATOR 
		min_rtt = rtt_in_ms if rtt_in_ms < min_rtt else min_rtt
		
		# MAXIMUM RTT : SIMPLE METHOD TO USE TERNARY OPERATOR
		max_rtt = rtt_in_ms if rtt_in_ms > max_rtt else max_rtt
		
		# INCREASE THE average_rtt AND count VARIABLES TO OBTAIN THE RTT AVERAGE
		average_rtt += rtt_in_ms
		count += 1
	
		# PRINT SINGLE LINE SUCCESSFULL PACKET SENT
		print (modifiedMessage.decode()+' Sequence Number : ',i , time.asctime( time.localtime(time.time()) ), 'RTT : ', rtt_in_ms)
	except:
		# PRINT SINGLE LINE LOSS PACKET 
		print('LOSS Sequence Number:  ',i, time.asctime( time.localtime(time.time()) ))
		
		# INCREASE loss COUNTER
		loss += 1 
		
# END MAIN PROGRAM AND CLOSE CLIENT CONNECTION
clientSocket.close()

#### STATISTICS  ####
# Packet loss rate 
pack_loss_rate = loss * 10

# Packet successfull transmitted 
pack_success = 100 - pack_loss_rate

# Average RTT 
average_rtt = average_rtt / count

# PRINT STATISTICS
print('Packet loss rate :',pack_loss_rate,'%' , 'Packet successfull transmitted : ' ,pack_success , '%') 
print('Minimum RTT : ', min_rtt)
print('Maximum RTT : ', max_rtt)
print('Average RTT : ', average_rtt)


