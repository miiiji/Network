import socket
import os
import time
import struct
import hashlib

ip_address = '127.0.0.1'
port_number = 2345

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open....")

data,addr = server_sock.recvfrom(2000)
real_checksum = data[0:20]
hash_checksum = data[20:]
ACK = struct.unpack("!b",data[20:21])[0]		
h = hashlib.sha1()					
h.update(hash_checksum)		
temp = h.digest()		
			
if(temp == real_checksum):			
	ACK_2 = (ACK)				
	seq_2 = ACK_2				
	seq_2 = seq_2 << 4				
	ACK_2 = ACK_2 & 0b1111				
	ACK_byte = ((seq_2|ACK_2).to_bytes(1,"big"))		
	print(ACK_byte)					
	server_sock.sendto(ACK_byte,addr)		
	print("Send file info ACK..")			
	fileSize = struct.unpack("!i",data[21:25])[0]		
	fileName = data[25:]				
	print("File Name: "+fileName.decode())			
	print("File Size:",fileSize) 				
	info_file = open("./"+fileName.decode(),"wb")		
	print("File Path:",os.path.realpath(fileName).decode())	

transfered_size = 0
					
msg,addr = server_sock.recvfrom(1045)
count = 0
#front = count%8
#end = (count+3)%8
#sequence_num = struct.unpack("!b",msg[20:21])[0]
old_s_num = ACK
while True:						
	count += 1			
	check_hash = msg[20:1045]			
	real_hash = msg[0:20]			
	real_data = msg[21:1045]			
	sequence_num = struct.unpack("!b",msg[20:21])[0]		

	h = hashlib.sha1()				
	h.update(check_hash)					
	temp = h.digest()					
				
	if(real_hash == temp):	
		send_seq = sequence_num >> 4				
		send_seq = send_seq&0b00001111				
	#	print(send_seq)				
		send_ACK = sequence_num&0b00001111			
	#	print(send_ACK)
		if(send_seq == send_ACK): #받은 시퀀스와 애크가 같으면 				
			send_seq = send_seq << 4				
			send_ACK = send_ACK & 0b1111			
		#	print(send_seq)					
		#	print(send_ACK)				
			r_sending = ((send_seq|send_ACK).to_bytes(1,"big"))				
		#	print(r_sending)				
			server_sock.sendto(r_sending,addr)			
			info_file.write(real_data)			
			transfered_size += len(real_data)			
			result = (float(transfered_size) / fileSize * 100)	
			print ("(current size / total size) = ",end = " ")
			print (str(transfered_size)+"/"+str(fileSize),end = " ")		
			print ("%.1f%%" % result)
			if len(real_data)<1024:
				break;
			old_s_num = sequence_num
			msg,addr = server_sock.recvfrom(1045)	

	
print("File Receive End.")
