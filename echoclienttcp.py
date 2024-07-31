from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write("Hello, server!".encode("utf-8"))

    def dataReceived(self, data):
        print("Received:", data.decode("utf-8"))

    def connectionLost(self, reason):
        print("Connection lost.")

class EchoClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")

if __name__ == '__main__':
    reactor.connectTCP("127.0.0.1", 8000, EchoClientFactory())
    print("Echo client started. Connecting to server...")
    reactor.run()
