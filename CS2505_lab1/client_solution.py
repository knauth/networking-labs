import socket as sk # no wildcard imports
import sys
import math

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

# set values for host 'localhost' - meaning this machine and port number 10000
# the machine address and port number have to be the same as the server is using.
server_address = (sk.gethostbyname(sk.gethostname()), 9996)
# output to terminal some info on the address details
print('connecting to server at %s port %s' % server_address)
# Connect the socket to the host and port
sock.connect(server_address)

"""
I thought this was easy, but there's one issue that took me a lot of thinking
to analyze and solve. Here's the logic between the client and server:
    
Client: Sends its message, all at once
Server: Recieves message in 16B chunks, then sends back some acknowledgement
e.g. "Logged <your message>"
Client: receives until it has received the same amount of data it has sent,
then exits

Here's the problem- the server is sending more bytes than it receives. This
means that the client actually exits before the server is done replying.

We can't just tell the server "and once you're done receiving, tell the client",
because the server doesn't know when it's done receiving until the client is 
done sending (closes the socket), which the client can't do until it's done 
receiving the server's reply, which the server can't finish-

You get the picture.

There are a lot of solutions to this problem, and message length headers would
probably be the best, but I'm gonna do the easier thing- just make sure the 
server is sending 16B for every chunk it receives. Then have the client keep
receiving until it gets the length of its message *padded to the nearest 16B* back.
That way even if the client's final chunk isn't 16B (highly likely), it
still doesn't close the connection early.

I'm sure all this is obvious to whomever is reading/marking this, but I got
really frustrated while debugging this issue and so felt like writing about
what a pain it is.

God, I hate buffers.
"""

try:
    # Send data
    message = input("Send: ")
    print('sending "%s"' % message)
    # Data is transmitted to the server with sendall()
    # encode() function returns bytes object
    sock.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = 16 * math.ceil(len(message.encode()) / 16) # round up
    
    while amount_received < amount_expected: 
        # decode() function returns string object
        data = sock.recv(16).decode()
        amount_received += (len(data))
        # amount_received += (len(data))
        print('received "%s"' % data)
        
finally:
    print('closing socket')
    sock.close()