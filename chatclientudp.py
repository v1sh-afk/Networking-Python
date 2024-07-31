from twisted.internet import reactor, protocol, stdio


class ChatBox(protocol.DatagramProtocol):
    def __init__(self, nickname):
        self.nickname = nickname.encode()
        self.server_addr = None

    def startProtocol(self):
        self.server_addr = ('127.0.0.1', 8000)
        self.transport.write(b'login|' + self.nickname, self.server_addr)

    def datagramReceived(self, data, addr):
        message = data.decode().strip()
        print(message)

    def sendData(self, data):
        self.transport.write(data.encode(), self.server_addr)


class ChatBoxFactory(protocol.ClientFactory):
    def __init__(self, nickname):
        self.nickname = nickname

    def buildProtocol(self, addr):
        chatbox = ChatBox(self.nickname)
        chatbox.server_addr = addr
        return chatbox

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()


class ChatConsole(stdio.StandardIO):
    def __init__(self, chatbox):
        self.chatbox = chatbox
        stdio.StandardIO.__init__(self, chatbox)

    def write(self, data):
        self.chatbox.sendData(data)


def run_chat_client(nickname):
    chatbox = ChatBox(nickname)
    reactor.listenUDP(0, chatbox)

    chatconsole = ChatConsole(chatbox)

    reactor.run()

if __name__ == '__main__':
    nickname = input("Enter your nickname: ")
    run_chat_client(nickname)
