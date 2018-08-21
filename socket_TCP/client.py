import socket
import os
import struct

serverIP = '127.0.0.1'
serverPort = 2345

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clnt_sock.connect((serverIP,serverPort))
print("Connect to Server...")
print("Receiver IP = "+serverIP)
print("Receiver Port = " + str(serverPort))
file_name = input("Input file name : ")

file_size = os.path.getsize(file_name)
byte_size = file_size.to_bytes(4, byteorder = "big")
first_type = '0'

clnt_sock.send(first_type.encode()+file_name.ljust(11).encode()+byte_size)

second_type = '1'
file_path = os.path.join(os.getcwd(),file_name)
f = open(file_path,"rb")
transfered_size = 0	
data = f.read(1024)
while data:
	clnt_sock.send(second_type.encode()+file_name.ljust(11).encode()+byte_size+data)
	transfered_size += len(data)
	result = (float(transfered_size) / file_size * 100)
	print("(current size / total size) = ",end =" ")
	print(str(transfered_size)+"/"+str(file_size),end=" ")
	print("%.3f%%" % result)
	data = f.read(1024)
	if len(data) == 0:
		break;
print("File send end")
#print("Received Message from Server : " +(clnt_sock.recv(1024)).decode('utf-8'))
