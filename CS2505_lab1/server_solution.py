import socket as sk
import logging
import time

# easier than writing my own log function
logging.basicConfig(filename='server.log', 
                    filemode='a',
                    format='%(asctime)s - %(message)s',
                    level=logging.INFO)

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

# set values for server address
server_address = (sk.gethostbyname(sk.gethostname()), 9996)
# output to terminal some info on the address details
print('*** Server is starting up on {} port {}***'.format(
        server_address[0], 
        server_address[1]))
# Bind the socket to the host and port
sock.bind(server_address)

# Listen for one incoming connections to the server
sock.listen(1)

# we want the server to run all the time, so set up a forever true while loop
while True:

    # Now the server waits for a connection
    print('*** Waiting for a connection ***')
    # accept() returns an open connection between the server and client, along with the address of the client
    connection, client_address = sock.accept()
    
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            # decode() function returns string object
            data = connection.recv(16).decode()
            if data:
                print('received "%s"' % data)
                logging.info('received "%s"' % data)
                print('sending confirmation to the client')
                data = "Logged @" + time.strftime("%H:%M:%S") #16B exactly
                # encode() function returns bytes object
                connection.sendall(data.encode())
                print("done sending")
            
            else:
                print('no more data from', client_address)
                break
        
    finally:
        # Clean up the connection
        connection.close()

# now close the socket
sock.close();