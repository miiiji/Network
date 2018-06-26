import socket
import struct
import re
import os
import ipaddress

recv_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
print("===========================================================")
print("                  Ethernet                         ")
print("===========================================================")

def convertBytesToMacAddr(bytes_addr):
	mac_addr = ""
	splitedStr = re.findall('..',bytes_addr)

	for i in range(0, len(splitedStr)):
		mac_addr += splitedStr[i]
		if i < len(splitedStr) - 1:
			mac_addr += ":"

	return mac_addr


while True:
	packet = recv_socket.recvfrom(4096)
	
	ethernet_header = struct.unpack('!6s6s2s', packet[0][0:14])
	dst_ethernet_addr = ethernet_header[0].hex()
	src_ethernet_addr = ethernet_header[1].hex()
	protocol_type = "0x"+ethernet_header[2].hex()

#	print(str(packet[0]),"\n")
#	print(str(packet[1]))
	print("Destination MAC address : ",convertBytesToMacAddr(dst_ethernet_addr))
	print("Source MAC address : ",convertBytesToMacAddr(src_ethernet_addr))
	print("Type : ",protocol_type)
#	print("--------------------------------------")
	

	print("==========================================================")
	print("                   IPv4                               ")
	print("==========================================================")

	if(protocol_type == '0x0800'):
		Internet_header = struct.unpack('!B B H H H B B H 4s 4s',packet[0][14:34])
		Version = Internet_header[0]>>4
		Version_r = Version&0b00001111
		length = Internet_header[0]&0b00001111
		length_r = length*4
		DSCP = Internet_header[1]>>2
		DSCP_r = DSCP&0b00111111
		ECN_r = Internet_header[1]&0b00000011
		total = Internet_header[2]
		Iden = Internet_header[3]
		Flags = Internet_header[4]>>13
		Flags_r = Flags&0b0000000000000111
		Fragment = Internet_header[4]&0b0001111111111111
		TTL = Internet_header[5]
		Protocol = Internet_header[6]
		Checksum = Internet_header[7]
		Source = Internet_header[8]
		Source_r = socket.inet_ntoa(Source)
		Destination = Internet_header[9]
		Destination_r=socket.inet_ntoa(Destination)
	
	
		print("Version : ",Version)
		print("Internet Header Length : ",length_r)
		print("DSCP :", DSCP)
		print("ECN :", ECN_r)
		print("Total length:",total)
		print("Identification :",Iden)
		print("Flags :",Flags_r)
		print("Fragment offset :",Fragment)
		print("TTL : ",TTL)
		print("Protocol : ",Protocol)
		print("Header Checksum : ",Checksum)
		print("Source IP address : ",Source_r)
		print("Destination : ",Destination_r)

		break	
