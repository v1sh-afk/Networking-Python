from twisted.internet import reactor, protocol


class ChatroomServer(protocol.Protocol):
    def __init__(self):
        self.clients = []

    def connectionMade(self):
        # Add the connected client to the list
        self.clients.append(self.transport)

    def dataReceived(self, data):
        message = data.decode().strip()
        if message == "/quit":
            self.transport.loseConnection()
            print(f"Client {self.transport.getPeer()} has left the chat.")
        else:
            print(f"Received from {self.transport.getPeer()}: {message}")
            self.broadcast(message)

    def broadcast(self, message):
        for client in self.clients:
            if client != self.transport:
                client.write(message.encode())

    def connectionLost(self, reason):
        # Remove the disconnected client from the list
        self.clients.remove(self.transport)


class ChatroomServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ChatroomServer()


if __name__ == '__main__':
    # Replace 'localhost' with the actual server IP or hostname
    server_host = '127.0.0.1'  # Replace with the actual server IP address
    server_port = 8000

    # Start listening on the specified IP and port
    reactor.listenTCP(server_port, ChatroomServerFactory(), interface=server_host)
    print("Server started on {}:{}".format(server_host, server_port))

    # Start the Twisted reactor to run the server
    reactor.run()
