from twisted.internet import protocol, reactor

class StarProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory  # factory that stores all the clients connected to the server
        self.name = None  # name of the client that will connect to the server

    def connectionMade(self):
        '''establishing a connection to the server'''
        print('New client connected: ', self.transport.getPeer())
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Client disconnected")
        self.factory.remove(self)

    def dataReceived(self, data):
        message = data.decode().strip()
        if not self.name:
            self.name = message
            print(self.name, ' has connected to the server.')  # if the client has not connected
        else:
            if message.startswith('@'):
                # already existing client sends a message
                '''one client will send message to another client '''
                recipient, private_message = message[1:].split(":", 1)
                self.sendthroughServer(recipient, private_message)
            else:
                '''if destination is not specified, the message is simply sent to the server.'''
                self.transport.write(message)

    def sendthroughServer(self, recipient, message):
        self.transport.write(message)  # the message first goes to the server
        self.transport.write('message sending.....')
        self.sendPrivateMessage(recipient, message)  # destination through the server

    def sendPrivateMessage(self, recipient, message):
        for client in self.factory.clients:
            if client.name == recipient:
                client.transport.write(f"(Private) {self.name}: {message}\n".encode())
                break
        else:
            self.transport.write(f"Error: User {recipient} not found.\n".encode())

class StarFactory(protocol.Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        # the message is then sent to the
        return StarProtocol(self)

if __name__ == "__main__":
    reactor.listenTCP(8080, StarFactory())
    print("Server started. Listening on port 8080...")
    print("Enter client name to register. Enter @ before the starting of a message to send message to another client.")
    reactor.run()
