import socket

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 8888  # Arbitrary non-privileged port

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections (up to 1)
server_socket.listen(1)

print('Waiting for a client to connect...')

# Accept a connection from a client
client_socket, client_address = server_socket.accept()

print('Connected by', client_address)

while True:
    # Receive data from the client
    data = client_socket.recv(1024)
    if not data:
        break

    # Send the received data back to the client
    client_socket.sendall(data)

# Close the connection with the client
client_socket.close()
server_socket.close()
