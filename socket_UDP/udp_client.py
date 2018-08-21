import socket

serverIP = '127.0.0.1'
serverPort = 3333

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("===========================================================")
print("\tString Change Program")
print("===========================================================")
print("type = 0,1,2,3")
print("if type == 0 : Change all letters to uppercase.")
print("if type == 1 : Change all letters to lowercase.")
print("if type == 2 : Change upper case to lower case and lower case to upper case.")
print("if type == 3 : Change the sentence backwards.")
print("===========================================================")
while True:
	client_type = input("Input Type : ")
	client_msg = input("Input yout Message : ")
	clnt_sock.sendto(client_type.encode()+client_msg.encode(), (serverIP, serverPort))
	print("Send Message to Server..")
	print("Received Message from Server :"+(clnt_sock.recv(1024)).decode())
	print("--------------------------------------------------")
