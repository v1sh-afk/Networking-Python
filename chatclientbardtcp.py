from twisted.internet import protocol, reactor
from twisted.internet.tcp import TcpClient


class ChatClient(TcpClient):

    def __init__(self, host, port):
        super().__init__(host, port)

    def connectionMade(self):
        print("Connected to chat server")

    def dataReceived(self, data):
        print(data)

    def sendMessage(self, message):
        self.transport.write(message)


if __name__ == "__main__":
    client = ChatClient("localhost", 8000)
    client.connect()

    message = input("Enter message: ")
    client.sendMessage(message)

    while True:
        message = input("Enter message: ")
        if message == "quit":
            break
        client.sendMessage(message)

    reactor.run()
