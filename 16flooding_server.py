from twisted.internet import reactor, protocol

class FloodingProtocol(protocol.Protocol):
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = []

    def connectionMade(self):
        print(f"Node {self.node_id} connected to the network.")
        self.startFlooding()    

    def connectionLost(self, reason):
        print(f"Node {self.node_id} disconnected from the network.")

    def dataReceived(self, data):
        message = data.decode()
        print(f"Node {self.node_id} received message: {message}")

    def sendMessage(self, message):
        for neighbor in self.neighbors:
            self.transport.write(message.encode(), neighbor)

    def startFlooding(self):
        message = f"Hello from Node {self.node_id}"
        self.sendMessage(message)
        reactor.callLater(1, self.startFlooding)

    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def removeNeighbor(self, neighbor):
        if neighbor in self.neighbors:
            self.neighbors.remove(neighbor)

    def startProtocol(self):
        pass

    def stopProtocol(self):
        reactor.stop()


class FloodingFactory(protocol.Factory):
    def __init__(self, node_id):
        self.node_id = node_id

    def buildProtocol(self, addr):
        return FloodingProtocol(self.node_id)


if __name__ == "__main__":
    node_id = "A"  # Replace with the ID of the current node
    factory = FloodingFactory(node_id)
    reactor.listenTCP(8000, factory)  # Replace with the desired port number
    reactor.run()
