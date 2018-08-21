import socket
import os
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
h = hashlib.sha1()
h.update(hash_checksum)
temp = h.digest()

if(temp == real_checksum):
	ACK = struct.unpack("!b",data[20:21])[0]
	ACK = (ACK+1)%2
	ACK_byte = ACK.to_bytes(4, byteorder = "big")
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

while True:
	check_hash = msg[20:1045]
	real_hash = msg[0:20]
	real_data = msg[21:1045]
	#sequence_num = msg[20]
	sequence_num = struct.unpack("!b",msg[20:21])[0]
	print("accept sequence number",sequence_num)
	send_ACK = (sequence_num+1)%2
	ACK_byte = send_ACK.to_bytes(4,byteorder = "big") 	
	print("sending ACK:",send_ACK)
	h = hashlib.sha1()
	h.update(check_hash)
	temp = h.digest()

	if(real_hash == temp):	
		server_sock.sendto(ACK_byte,addr)
		info_file.write(real_data)
		transfered_size += len(real_data)
		result = (float(transfered_size) / fileSize * 100)	
		print ("(current size / total size) = ",end = " ")
		print (str(transfered_size)+"/"+str(fileSize),end = " ")
		print ("%.1f%%" % result)
		if len(real_data)<1024:
			break;
		msg,addr = server_sock.recvfrom(1045)
	
print("File Receive End.")
