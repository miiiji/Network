import socket

ip_address = '127.0.0.1'
port_number = 3333

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")
while True:
	print("-------------------------------------------------------")
	print("Listening...")
	data,addr = server_sock.recvfrom(5000)
	data_type = data[:1]
	print("Type of Message: ",data_type.decode())
	message = data[1:]
	print("Received Message from client : ", message.decode())

	if data_type.decode() == '0':
		message_r = message.decode().upper()
		print("Converted Message : ",message_r)
	if data_type.decode() == '1':
		message_r = message.decode().lower()
		print("Converted Message : ",message_r)
	if data_type.decode() == '2':
		message_r  = message.decode()
		message_r = message_r.swapcase()
#	length = len(message_r)
#	for i in range(length):
#		if message_r[i]>='a' and message_r[i]<='z':
#			message_r[i].swapcase()
#		if message_r[i]>='A' and message_r[i]<='Z':
#			message_r[i].swapcase()
		print("Converted Message : ",message_r)
	if data_type.decode() == '3':
		message_r = message.decode()
		message_r=''.join(reversed(message_r))
		print("Converted Message : ",message_r)
	server_sock.sendto(message_r.encode(),addr)
	print("Send to Client Converted Message .....")
