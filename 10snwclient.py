from twisted.internet import reactor, protocol

class StopAndWaitClient(protocol.Protocol):
    def connectionMade(self):
        print("Connected to server.")
        self.send_ack()

    def send_ack(self):
        self.transport.write(input("Enter ack: ").encode())
        print("ACK sent")

    def dataReceived(self, data):
        message = data.decode()
        print("Message received:", message)
        self.send_ack()

    def connectionLost(self, reason):
        print("Connection lost:", reason.getErrorMessage())

class StopAndWaitClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return StopAndWaitClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason.getErrorMessage())
        reactor.stop()

server_address = 'localhost'
server_port = 8000
factory = StopAndWaitClientFactory()
reactor.connectTCP(server_address, server_port, factory)
reactor.run()
