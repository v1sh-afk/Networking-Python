import socket

HOST = 'localhost'  # The server's hostname or IP address
PORT = 8888  # The port used by the server

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Send data to the server
message = input('Enter a message to send to the server: ')
client_socket.sendall(message.encode())

# Receive data from the server
data = client_socket.recv(1024)

print('Received from server:', data.decode())

# Close the connection with the server
client_socket.close()
