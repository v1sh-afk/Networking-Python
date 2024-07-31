from twisted.internet import protocol, reactor

class SMTPClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.sendLine(b'HELO client.example.com')

    def dataReceived(self, data):
        response = data.decode().strip()
        print('Server:', response)

        if response.startswith('250'):
            self.sendLine(b'MAIL FROM:<john@example.com>')
        elif response.startswith('250'):
            self.sendLine(b'RCPT TO:<sarah@example.com>')
        elif response.startswith('250'):
            self.sendLine(b'DATA')
        elif response.startswith('354'):
            self.sendLine(b'From: john@example.com\r\n'
                          b'To: sarah@example.com\r\n'
                          b'Subject: Hello Sarah\r\n'
                          b'\r\n'
                          b'Hi Sarah, how are you doing? Just wanted to say hello!\r\n'
                          b'.')
        elif response.startswith('250'):
            self.sendLine(b'QUIT')
        elif response.startswith('221'):
            self.transport.loseConnection()

    def sendLine(self, line):
        self.transport.write(line + b'\r\n')

    def connectionLost(self, reason):
        print('Connection lost:', reason)

class SMTPClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return SMTPClientProtocol()

if __name__ == '__main__':
    reactor.connectTCP('localhost', 25, SMTPClientFactory())
    reactor.run()
