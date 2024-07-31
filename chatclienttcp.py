from twisted.internet import reactor, protocol, stdio
from twisted.protocols.basic import LineReceiver


class ChatBox(LineReceiver):
    delimiter = b'\n'

    def __init__(self, nickname):
        self.nickname = nickname

    def connectionMade(self):
        self.sendLine(f'login|{self.nickname}'.encode())

    def lineReceived(self, line):
        message = line.decode().strip()
        print(message)

    def sendData(self, data):
        self.sendLine(data.encode())


class ChatBoxFactory(protocol.ClientFactory):
    def __init__(self, nickname):
        self.nickname = nickname

    def buildProtocol(self, addr):
        chatbox = ChatBox(self.nickname)
        return chatbox

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()


class ChatConsole(LineReceiver):
    delimiter = b'\n'

    def __init__(self, chatbox):
        self.chatbox = chatbox

    def connectionMade(self):
        self.sendLine("Connected to the chat server. Start typing your messages:".encode())

    def lineReceived(self, line):
        self.chatbox.sendData(line.decode().strip())

    def rawDataReceived(self, data):
        pass


def run_chat_client(nickname):
    chatbox_factory = ChatBoxFactory(nickname)
    reactor.connectTCP('127.0.0.1', 8000, chatbox_factory)

    stdio.StandardIO(ChatConsole(chatbox_factory.buildProtocol(None)))

    reactor.run()


if __name__ == '__main__':
    nickname = input("Enter your nickname: ")
    run_chat_client(nickname)
