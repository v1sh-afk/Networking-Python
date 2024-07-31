from twisted.internet import reactor, protocol

class FloodingClient(protocol.Protocol):
    def __init__(self, node_id):
        self.node_id = node_id

    def connectionMade(self):
        print(f"Client {self.node_id} connected to the server.")
        self.sendMessage()

    def dataReceived(self, data):
        message = data.decode()
        print(f"Client {self.node_id} received message: {message}")

    def sendMessage(self):
        message = f"Hello from Client {self.node_id}"
        self.transport.write(message.encode())

    def connectionLost(self, reason):
        print(f"Client {self.node_id} disconnected from the server.")

    def startProtocol(self):
        pass

    def stopProtocol(self):
        reactor.stop()


class FloodingClientFactory(protocol.ClientFactory):
    def __init__(self, node_id):
        self.node_id = node_id

    def buildProtocol(self, addr):
        return FloodingClient(self.node_id)

    def clientConnectionFailed(self, connector, reason):
        print(f"Connection failed for Client {self.node_id}: {reason.getErrorMessage()}")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print(f"Connection lost for Client {self.node_id}: {reason.getErrorMessage()}")
        reactor.stop()


if __name__ == "__main__":
    node_id = "C"  # Replace with the ID of the client node
    factory = FloodingClientFactory(node_id)
    reactor.connectTCP("localhost", 8000, factory)  # Replace with the IP address and port of the server
    reactor.run()
