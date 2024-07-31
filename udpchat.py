import socket
import threading

host = '127.0.0.1'
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))

print('SERVER IS LISTENING...')
clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        server.sendto(message, client[0])

def handle(client, address):
    while True:
        try:
            message, client_address = server.recvfrom(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        message, client_address = server.recvfrom(1024)
        print("Connected with {}".format(str(client_address)))

        server.sendto('NICK'.encode('ascii'), client_address)
        nickname, _ = server.recvfrom(1024)
        nicknames.append(nickname.decode('ascii'))
        clients.append(client_address)

        print("Nickname is {}".format(nickname.decode('ascii')))
        broadcast("{} joined!".format(nickname.decode('ascii')).encode('ascii'))
        server.sendto('Connected to server!'.encode('ascii'), client_address)

        thread = threading.Thread(target=handle, args=(client_address,))
        thread.start()

receive()
