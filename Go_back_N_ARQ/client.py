import socket
import os
import struct
import hashlib

serverIP = '127.0.0.1'
serverPort = 2345

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clnt_sock.settimeout(4)
windowsize = 4
window = []

print("Connect to Server...")
print("Receiver IP = "+serverIP)
print("Receiver Port = " + str(serverPort))
file_name = input("Input file name : ")
count = 0
end = (count+3)%8
count_2 = 0
front = count%8
sending_ACK = front
check_ACK = front

file_size = os.path.getsize(file_name)
byte_size = file_size.to_bytes(4, byteorder = "big")
sequence_number = front << 4
sending_ACK = sending_ACK & 0b1111
sending = ((sequence_number|sending_ACK).to_bytes(1,"big"))
checksum_1 = sending+byte_size+file_name.encode()

r_checksum_1 = hashlib.sha1()
r_checksum_1.update(checksum_1)
r_checksum_1 = r_checksum_1.digest()
print("Send File info(file Name, file Size, seqNum) to Server...")
clnt_sock.sendto(r_checksum_1+checksum_1,(serverIP,serverPort))					
r_ACK = clnt_sock.recv(1)
r_ACK = struct.unpack("!b",r_ACK)[0]
old_ACK = r_ACK
checking = r_ACK

if(r_ACK == check_ACK):
	file_path = os.path.join(os.getcwd(),file_name)
	f = open(file_path,"rb")
	transfered_size = 0
	count_2+=1	
	count+=1	
#	front = (count_2%8)
#	end = (count_2+3)%8
	for i in range(windowsize):
		r_sending_ACK = count%8
		r_check_ACK = count%8
		r_sequence_number = count%8
		window.append(r_sequence_number)

		r_sequence_number = r_sequence_number << 4
		r_sending_ACK = r_sending_ACK & 0b1111
		r_sending = ((r_sequence_number|r_sending_ACK).to_bytes(1,"big"))

		data = f.read(1024)
		if len(data)==0:
			break
		checksum = r_sending+data
				
		r_checksum = hashlib.sha1()
		r_checksum.update(checksum)
		r_checksum = r_checksum.digest()
		
	#	for_list.append(data)
		
		clnt_sock.sendto(r_checksum+checksum,(serverIP, serverPort))
		
	#	window.append(r_sequence_number)
		print(window)
		transfered_size += len(data)
		result = (float(transfered_size) / file_size * 100)
		print("(current size / total size) = ",end =" ")
		print(str(transfered_size)+"/"+str(file_size),end=" ")
		print("%.1f%%" % result)
		count += 1
			
	while True:
		check_ACK_f = clnt_sock.recv(1)
		check_ACK_f = struct.unpack("!b",check_ACK_f)[0]
		check_ACK_f = check_ACK_f&0b00001111
		data = f.read(1024)
#		print(check_ACK_f)
		del window[0]		
	
		if len(data)==0:
			break
		
		r_sending_ACK = count%8
		r_check_ACK = count%8
		r_sequence_number = count%8
		window.append(r_sequence_number)
		r_sequence_number = r_sequence_number << 4
		r_sending_ACK = r_sending_ACK & 0b1111
		r_sending = ((r_sequence_number|r_sending_ACK).to_bytes(1,"big"))
		checksum = r_sending+data

		r_checksum = hashlib.sha1()
		r_checksum.update(checksum)
		r_checksum = r_checksum.digest()

		clnt_sock.sendto(r_checksum+checksum,(serverIP, serverPort))

		

		transfered_size += len(data)
		result = (float(transfered_size) / file_size * 100)
		print("(current size / total size) = ",end =" ")
		print(str(transfered_size)+"/"+str(file_size),end=" ")
		print("%.1f%%" % result)
		count += 1
		print(window)    

	#		clnt_sock.sendto(r_checksum+checksum,(serverIP, serverPort))			
	#		print(
print("File send end")
#print("fReceived Message from Server : " +(clt_sock.recv(1024)).decode('utf-8'))
