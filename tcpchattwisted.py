from twisted.internet import reactor, protocol
from twisted.internet.protocol import Factory

class ChatServer(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
    def connectionMade(self):
        self.factory.clients.append(self)
        print("Client connected:", self.transport.getPeer().host)
    
    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print("Client disconnected:", self.transport.getPeer().host)
    
    def dataReceived(self, data):
        message = data.decode('ascii')
        print("Received message:", message)
        self.broadcast(message)
    
    def broadcast(self, message):
        for client in self.factory.clients:
            client.transport.write(message.encode('ascii'))

class ChatServerFactory(Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        return ChatServer(self)  # Pass the factory instance to the ChatServer constructor



    def clientConnectionLost(self, connector, reason):
        print("Lost a client connection")
        self.clients.remove(connector.protocol)

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed")

    def broadcast(self, message):
        for client in self.clients:
            client.transport.write(message.encode())

if __name__ == '__main__':
    factory = ChatServerFactory()  # Create an instance of ChatServerFactory
    reactor.listenTCP(55555, factory)
    print("Server started on 127.0.0.1:55555")
    reactor.run()

