from twisted.internet import reactor, protocol

class ChatroomServer(protocol.DatagramProtocol):
    def __init__(self):
        self.clients = []

    def datagramReceived(self, datagram, addr):
        message = datagram.decode().strip()
        if message == "/quit":
            self.clients.remove(addr)
            print(f"Client {addr} has left the chat.")
        else:
            print(f"Received from {addr}: {message}")
            self.broadcast(message, addr)

    def broadcast(self, message, sender_addr):
        for client in self.clients:
            if client != sender_addr:
                self.transport.write(message.encode(), client)

    def startProtocol(self):
        # Replace 'localhost' with the actual server IP or hostname
        server_host = '127.0.0.1'  # Replace with the actual server IP address
        server_port = 8000

        # Start listening on the specified IP and port
        self.transport.connect(server_host, server_port)
        print("Server started on {}:{}".format(server_host, server_port))

if __name__ == '__main__':
    reactor.listenUDP(8000, ChatroomServer())
    reactor.run()
