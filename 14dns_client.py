from twisted.internet import reactor, protocol

class DNSClientProtocol(protocol.Protocol):
    def connectionMade(self):
        domain = input("Enter a domain name: ")
        self.transport.write(domain.encode())

    def dataReceived(self, data):
        response = data.decode()
        print("Response:", response)
        self.transport.loseConnection()

class DNSClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return DNSClientProtocol()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

if __name__ == "__main__":
    reactor.connectTCP("localhost", 53, DNSClientFactory())
    reactor.run()
