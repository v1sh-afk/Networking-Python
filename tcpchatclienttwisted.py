from twisted.internet import reactor, protocol
from twisted.internet.stdio import StandardIO

nickname = input("Choose your nickname: ")

class ChatClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write("NICK".encode('ascii'))

    def dataReceived(self, data):
        message = data.decode('ascii').strip()
        if message == 'NICK':
            self.transport.write(nickname.encode('ascii'))
        else:
            print(message)

class ChatClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return ChatClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

if __name__ == '__main__':
    reactor.connectTCP('127.0.0.1', 55555, ChatClientFactory())
    StandardIO(ChatClient())
    reactor.run()
