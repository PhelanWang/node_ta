# -*- coding:utf-8 -*-

import socket
import sys


if __name__ == "__main__":
    ip, port = sys.argv[1].split(":")
    ip_port = (ip, int(port))
    
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk.bind(ip_port)
    
    print 'server waiting...'
    count = 0
    while count <= 100:
        client_data, address = sk.recvfrom(1024)
        print client_data, address
        sk.sendto('Hello World', address)
        count += 1
    
    sk.close()