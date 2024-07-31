from twisted.internet import protocol, reactor

class SMTPServerProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(b'220 smtp.example.com Simple Mail Transfer Service Ready\r\n')

    def dataReceived(self, data):
        request = data.decode().strip()

        if request.startswith('HELO') or request.startswith('EHLO'):
            self.transport.write(b'250 Hello ' + request.split()[1].encode() + b', pleased to meet you\r\n')
        elif request.startswith('MAIL FROM:'):
            self.transport.write(b'250 OK\r\n')
        elif request.startswith('RCPT TO:'):
            self.transport.write(b'250 OK\r\n')
        elif request == 'DATA':
            self.transport.write(b'354 Start mail input; end with <CRLF>.<CRLF>\r\n')
            self.state = 'DATA'
        elif self.state == 'DATA' and request == '.':
            self.transport.write(b'250 OK, message received and queued for delivery\r\n')
            self.state = 'IDLE'
        elif request == 'QUIT':
            self.transport.write(b'221 Goodbye\r\n')
            self.transport.loseConnection()
        else:
            self.transport.write(b'500 Command not recognized\r\n')

    def connectionLost(self, reason):
        print('Connection lost:', reason)


class SMTPServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return SMTPServerProtocol()


if __name__ == '__main__':
    reactor.listenTCP(25, SMTPServerFactory())
    reactor.run()
