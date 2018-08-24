import socket
import os
import time
import struct
import hashlib

ip_address = '127.0.0.1'
port_number = 2345

seqList = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111]
indexing = 0

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

data,addr = server_sock.recvfrom(2000)
real_checksum = data[0:20]
hash_checksum = data[20:]
ACK = struct.unpack("!b",data[20:21])[0]		
h = hashlib.sha1()					
h.update(hash_checksum)		
temp = h.digest()
total_size = 0		
							
if(temp == real_checksum):	
	seqNum = seqList[indexing] << 4
	ACK = seqList[indexing]
	indexing = (indexing + 1) % 8
	ACK_byte = (seqNum|ACK).to_bytes(1, "big")
				
	server_sock.sendto(ACK_byte,addr)		
	print("Send file info ACK..")	
	info = data[21:]
	fileSize = struct.unpack("!i", info[:4])[0]			
#	fileSize = struct.unpack("!i",data[20:])[0]		
	fileName = info[4:]			
	print("File Name: "+fileName.decode())			
	print("File Size:",fileSize) 
	total_size = fileSize				
	info_file = open("./"+fileName.decode(),"wb")		
	print("File Path:",os.path.realpath(fileName).decode())	

transfered_size = 0
count = 0
check_ACK_f = 1
while transfered_size != total_size:
	msg,addr = server_sock.recvfrom(1045)	
	check_hash = msg[20:1045]			
	real_hash = msg[0:20]			
	real_data = msg[21:1045]			
	sequence_num = struct.unpack("!b",msg[20:21])[0]
	h = hashlib.sha1()				
	h.update(check_hash)				
	temp = h.digest()

	if count == 7:
		print("Wait for 5 ...")
		time.sleep(5)
	#	print("Wait for 5..")
		count += 1
	elif real_hash != temp:
		seqNum = seqList[indexing] << 4
		send_NAK = 0b1111
		NAK_sending = (seqNum|send_NAK).to_bytes(1, "big")
		server_sock.sendto(NAK_sending,addr)
		print("* Packet corrupted!! *** - Send To Sender NAK(2)")
	else:
		checkingseq = seqList[check_ACK_f]<<4
		checkingACK = seqList[check_ACK_f]
		checkingtotal = (checkingseq|checkingACK).to_bytes(1, "big")	
		if msg[20:21] == checkingtotal: 
			count += 1
			check_ACK_f = (check_ACK_f + 1) % 8
			transfered_size += len(msg[21:])
			info_file.write(msg[21:])
			seqNum = seqList[indexing] << 4
			ACK = seqList[indexing]
			indexing = (indexing + 1) % 8
			sending = (seqNum|ACK).to_bytes(1, "big")
			server_sock.sendto(sending, addr)
			result = (float(transfered_size) / fileSize * 100)	
			print ("(current size / total size) = ",end = " ")
			print (str(transfered_size)+"/"+str(fileSize),end = " ")		
			print ("%.1f%%" % result)
		else:
			print("Discarding")	

print("End")
