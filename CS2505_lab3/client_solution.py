#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 20:55:13 2022

@author: june
"""

import socket as sk 
import sys
import math

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

server_address = (sys.argv[1], int(sys.argv[2]))
filename = sys.argv[3]
print('connecting to server at %s port %s' % server_address)
# Connect the socket to the host and port
sock.connect(server_address)

try:
    # Format HTTP request
    request = f"""GET /{filename} HTTP/1.1
Host: {server_address[0]}:{server_address[1]}
User-Agent: Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)
Accept: */*

"""

    # useragent and accept don't really matter here

    print(request) 
    sock.sendall(request.encode())
    print("Sent Request")

    # # Look for the response
    # amount_received = 0
    # amount_expected = 16 * math.ceil(len(message.encode()) / 16) # round up
    
    # while amount_received < amount_expected:
    #     # decode() function returns string object
    #     data = sock.recv(16).decode()
    #     amount_received += (len(data))
    #     # amount_received += (len(data))
    #     print('received "%s"' % data)
    
    buf = ""

    while not "</html>" in buf.lower():
        buf += sock.recv(16).decode()
        # receive until the HTML close tag
        # this is a bit slow and dumb but it's ok for this use case

    print(buf)

finally:
    print('closing socket')
    sock.close()