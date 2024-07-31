from twisted.internet import protocol, reactor


class ChatServer(protocol.Protocol):

    def __init__(self):
        self.clients = []

    def connectionMade(self):
        print("Client connected")
        self.clients.append(self)

    def dataReceived(self, data):
        for client in self.clients:
            if client != self:
                client.transport.write(data)

    def connectionLost(self, reason):
        print("Client disconnected")
        self.clients.remove(self)


class ChatFactory(protocol.Factory):

    def buildProtocol(self, addr):
        return ChatServer()


if __name__ == "__main__":
    reactor.listenTCP(8000, ChatFactory())
    reactor.run()
