from twisted.internet import reactor, protocol
class RPCClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(b"add 10 5")

    def dataReceived(self, data):
        result = data.decode().strip()
        print("Result:", result)
        self.transport.loseConnection()

class RPCClientFactory(protocol.ClientFactory):
    protocol = RPCClientProtocol

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

if __name__ == "__main__":
    from twisted.internet import endpoints

    endpoint = endpoints.TCP4ClientEndpoint(reactor, "localhost", 8000)
    factory = RPCClientFactory()
    endpoint.connect(factory)

    reactor.run()
