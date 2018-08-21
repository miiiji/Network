import socket
import os
import struct

ip_address = '127.0.0.1'
port_number = 2345

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((ip_address, port_number))
print("Server socket open....")

print("Listening....")
server_sock.listen()

client_sock,addr = server_sock.accept()

print("connected with client")

data = client_sock.recv(16)

fileType = data[0]
fileType = chr(fileType)
print(data[0])
print(data[1:12])
print(data[12:16]) 
if fileType == "0":
	fileName = data[1:12]
	fileSize = struct.unpack("!i",data[12:16])[0]
	print("File Name: "+fileName.decode())
	print("File Size:",fileSize) 
	info_file = open("./"+fileName.decode(),"wb")
	print("File Path:",os.path.realpath(fileName).decode())

msg = client_sock.recv(1040)
transfered_size = 0

while msg:
	if len(msg) == 0 :
		break;
	fileType_2 = msg[0]
	fileType_2 = chr(fileType_2)
	if fileType_2 == "1":
		real_data = msg[16:1040]
		info_file.write(real_data)
		transfered_size += len(real_data)
		result = (float(transfered_size) / fileSize * 100)	
		print ("(current size / total size) = ",end = " ")
		print (str(transfered_size)+"/"+str(fileSize),end = " ")
		print ("%.3f%%" % result)
		msg = client_sock.recv(1040)		

print("File Receive End.")

