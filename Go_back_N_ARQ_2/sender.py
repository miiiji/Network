import socket
import os
import struct
import hashlib


serverIP = '127.0.0.1'
serverPort = 2345
DATA_MAX_SIZE = 1024

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clnt_sock.settimeout(3)

seqList = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111]
indexing = 0

window = [] 

print("Sender Socket open...")
print("Receiver IP = " + serverIP)
print("Receiver Port = " + str(serverPort))
print("Send File Info(file Name, file Size, seqNum) to Server...")
file_name = input("Input file name : ")
total_size = 0
transfered_size = 0
check_ACK_index = 0
current_window_size = []


total_size = file_size = os.path.getsize(file_name)
byte_size = file_size.to_bytes(4, byteorder = "big")
seqNum = seqList[indexing]<<4
ACK = seqList[indexing]
indexing = (indexing + 1) % 8
sending = (seqNum|ACK).to_bytes(1, "big")

checksum = sending+byte_size+file_name.encode()
h = hashlib.sha1()
h.update(checksum)
first_packet = h.digest() + sending +byte_size+file_name.encode()
window.append(first_packet)

file_path = os.path.join(os.getcwd(),file_name)
f = open(file_path, "rb")
count = -1

while transfered_size!= total_size:
	try:
		if count == -1:
			clnt_sock.sendto(window[0], (serverIP, serverPort))
			current_window_size.append(total_size)
			count+=1
	
		while len(window) != 5:
			seqNum = seqList[indexing]<<4
			ACK = seqList[indexing]
			r_sending = (seqNum|ACK).to_bytes(1, "big")
			data = f.read(1024)
			if len(data) == 0:
				break
			
			checksum = r_sending + data
			h = hashlib.sha1()
			h.update(checksum)
			real = h.digest() + r_sending + data
			window.append(real)
			if count == 6:		
				seqNum = seqList[indexing]<<4
				ACK = seqList[indexing]
				sending = (seqNum|ACK).to_bytes(1, "big")		
				r_checksum = "123"
				r_checksum = r_checksum.rjust(20).encode()
				wrong = r_checksum + sending + data
				clnt_sock.sendto(wrong, (serverIP, serverPort))
			else:			
				clnt_sock.sendto(real, (serverIP, serverPort))
			count += 1
			transfered_size += len(data)
			current_window_size.append(len(data))
			result = (float(transfered_size) / file_size * 100)
			print("(current size / total size) = ",end =" ")
			print(str(transfered_size)+"/"+str(file_size),end=" ")
			print("%.1f%%" % result)
			indexing = (indexing + 1) % 8

		check_ACK_f = clnt_sock.recv(1)
		checkingseq = seqList[check_ACK_index]<<4
		checkingACK = seqList[check_ACK_index]
		checkingtotal = (checkingseq|checkingACK).to_bytes(1, "big")
		if check_ACK_f == checkingtotal:	
			del window[0]
			del current_window_size[0]
			print(len(window))
			check_ACK_index = (check_ACK_index + 1) % 8
	
		else:
			print(" * Received NAK - Retransmit!")
			retransmit_data_size = sum(i for i in current_window_size)
			transfered_size -= retransmit_data_size
			for i in range(len(current_window_size)):
				clnt_sock.sendto(window[i], (serverIP, serverPort))
				transfered_size += current_window_size[i]
				result = (float(transfered_size) / file_size * 100)

				print("Retransmission : (current size / total size) = ",end =" ")
				print(str(transfered_size)+"/"+str(file_size),end=" ")
				print("%.1f%%" % result)
			

	except socket.timeout as e:
		print("*** Time Out!! ***")
		retransmit_data_size = sum(i for i in current_window_size)
		transfered_size -= retransmit_data_size
		for i in range(len(current_window_size)):
			data_packet = window[i]
			clnt_sock.sendto(data_packet, (serverIP, serverPort))
			result = (float(transfered_size) / file_size * 100)
			transfered_size += current_window_size[i]
			print("Retransmission :(current size / total size) = ",end =" ")
			print(str(transfered_size)+"/"+str(file_size),end=" ")
			print("%.1f%%" % result)
			

print("End")
f.close()


