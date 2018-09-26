# -*- coding:utf-8 -*-
import socket
import sys
import time


if __name__ == "__main__":
	
	ip, port = sys.argv[1].split(":")
	ip_port = (ip, int(port))
	
	sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sk.connect(ip_port)
	count = 0
	while count <= 100:
		sk.sendall('Hello World')
		server_reply = sk.recv(1024)
		print server_reply
		count += 1
		time.sleep(2)
	
	sk.close()