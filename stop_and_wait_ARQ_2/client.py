import socket
import os
import struct
import hashlib

serverIP = '127.0.0.1'
serverPort = 2345

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clnt_sock.settimeout(4)
print("Connect to Server...")
print("Receiver IP = "+serverIP)
print("Receiver Port = " + str(serverPort))
file_name = input("Input file name : ")
count = 0
count_2 =0
sequence_number = count%2
check_ACK = (count+1)%2

file_size = os.path.getsize(file_name)
byte_size = file_size.to_bytes(4, byteorder = "big")
sequence_byte = sequence_number.to_bytes(1, byteorder = "big")
checksum_1 = sequence_byte+byte_size+file_name.encode()

r_checksum_1 = hashlib.sha1()
r_checksum_1.update(checksum_1)
r_checksum_1 = r_checksum_1.digest()
print("Send File info(file Name, file Size, seqNum) to Server...")
clnt_sock.sendto(r_checksum_1+checksum_1, (serverIP,serverPort))					
r_ACK = clnt_sock.recv(4)
r_ACK = struct.unpack("!i",r_ACK)[0]
old_ACK = r_ACK
check_ACK_f = (r_ACK+1)%2
checking = r_ACK
if(r_ACK == check_ACK):
	print("Start File send")
	count_2+=1
	count+=1
	file_path = os.path.join(os.getcwd(),file_name)
	f = open(file_path,"rb")
	transfered_size = 0	
	data = f.read(1024)
	while data:
		r_sequence_number = count%2
		r_check_ACK = (count+1)%2
		sequence_bytes = r_sequence_number.to_bytes(1,byteorder = "big")

		checksum = sequence_bytes+data
		r_checksum = hashlib.sha1()
		r_checksum.update(checksum)
		r_checksum = r_checksum.digest()
#		print("1"+str(r_checksum))
		if (count_2 == 3):
			r_checksum = "123"
			r_checksum = r_checksum.rjust(20).encode()
#		print("2"+str(r_checksum))	

		clnt_sock.sendto(r_checksum+checksum,(serverIP, serverPort))		
		if(checking != 3): 
			transfered_size += len(data)
			result = (float(transfered_size) / file_size * 100)
			print("(current size / total size) = ",end =" ")
			print(str(transfered_size)+"/"+str(file_size),end=" ")
			print("%.1f%%" % result)
		
		try:	
#			check_ACK_f = clnt_sock.recv(4)	
#			check_ACK_f = struct.unpack("!i",check_ACK_f)[0]			   		
#			checking = check_ACK_f
		#	print("check",check_ACK_f)
			while(True):
		#	
				check_ACK_f = clnt_sock.recv(4)			
				check_ACK_f = struct.unpack("!i",check_ACK_f)[0]			   		
				checking = check_ACK_f
				if(check_ACK_f!=old_ACK):
					break 
			
		except socket.timeout:
			print ("*TimeOut!!***")
			count_2 += 1
			old_ACK = check_ACK_f
			data = data
			transfered_size -= len(data)
			print("Retransmission :",end=" ")	
	
		if(check_ACK_f ==2):
			data = data
			transfered_size -= len(data)
			old_ACK = check_ACK_f
			print("* Received NAK - Retransmit!")	
			print("Retransmission :",end=" ")
			count_2+=1
	#		break;
		elif(check_ACK_f == r_check_ACK):
			old_ACK = check_ACK_f
			data = f.read(1024)
			count+=1
			count_2+=1
		elif(check_ACK_f == old_ACK):
			checking = 3

		if len(data) == 0:
			transfered_size += 1024
			result = (float(transfered_size) / file_size * 100)
			print("(current size / total size) = ",end =" ")
			print(str(transfered_size)+"/"+str(file_size),end=" ")

			print("%.1f%%" % result)
			break;
	#		clnt_sock.sendto(r_checksum+checksum,(serverIP, serverPort))			
	#		print(
print("File send end")
#print("fReceived Message from Server : " +(clnt_sock.recv(1024)).decode('utf-8'))
