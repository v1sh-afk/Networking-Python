from twisted.internet import reactor, protocol
from twisted.protocols import basic

class DropLink(basic.LineOnlyReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        self.factory.clients.append(self)
        print("New client connected to bus backbone.")

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print("Client disconnected.")

    def lineReceived(self, line):
        message = line.decode().strip()
        if not self.name:
            self.name = message
            print(f"{self.name} connected to bus.")
        else:
            if message.startswith("@"):
                recipient, private_message = message[1:].split(":", 1)
                self.sendPrivateMessage(recipient, private_message)
            else:
                print(f"{self.name}: {message}")
                self.broadcastMessage(f"{self.name}: {message}")

    def sendPrivateMessage(self, recipient, message):
        for client in self.factory.clients:
            if client.name == recipient:
                client.sendLine(f"(Private) {self.name}: {message}".encode())
                break
        else:
            self.sendLine(f"Error: User {recipient} not found.".encode())

    def broadcastMessage(self, message):
        for client in self.factory.clients:
            if client != self:
                client.sendLine(message.encode())


class BusBackbone(protocol.Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        return DropLink(self)

if __name__ == "__main__":
    reactor.listenTCP(8000, BusBackbone())
    print("Bus server started.")
    print("Enter your name as the first message to register. To send a message to a particular username, use '@username: message'.")
    reactor.run()
