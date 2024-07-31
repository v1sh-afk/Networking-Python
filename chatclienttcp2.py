from twisted.internet import reactor, protocol, stdio
from twisted.protocols import basic

class ChatClient(basic.LineReceiver):
    from os import linesep as delimiter

    def __init__(self):
        self.nickname = None

    def connectionMade(self):
        self.nickname = self.factory.nickname
        self.sendLine(f"login|{self.nickname}".encode())

    def lineReceived(self, line):
        message = line.decode().rstrip(self.delimiter)
        self.factory.clientReceivedMessage(message)

    def connectionLost(self, reason):
        print("Connection lost.")
        reactor.stop()

    def sendLine(self, line):
        self.transport.write(line + self.delimiter.encode())


class ChatClientFactory(protocol.ClientFactory):
    def __init__(self, nickname, callback=None):
        self.nickname = nickname
        self.client = None
        self.callback = callback

    def startedConnecting(self, connector):
        print("Connecting to the chat server...")

    def buildProtocol(self, addr):
        print("Connected to the chat server. Start typing your messages:")
        self.client = ChatClient()
        self.client.factory = self
        if self.callback:
            self.callback(self.client)
        return self.client

    def clientReceivedMessage(self, message):
        print(message)

    def clientConnectionLost(self, connector, reason):
        print("Lost connection to the chat server. Exiting...")
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print("Failed to connect to the chat server. Exiting...")
        reactor.stop()


def start_chat(client):
    stdio.StandardIO(client)


if __name__ == "__main__":
    nickname = input("Enter your nickname: ")
    factory = ChatClientFactory(nickname, callback=start_chat)
    reactor.connectTCP('127.0.0.1', 8000, factory)

    reactor.run()
