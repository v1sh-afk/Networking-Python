from twisted.internet import reactor, protocol

class EchoProtocol(protocol.Protocol):
    def dataReceived(self, data):
        print("Received:", data.decode())
        self.transport.write(data)
        self.transport.loseConnection()

    def connectionMade(self):
        print('Client connected')
    
        

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return EchoProtocol()

if __name__ == '__main__':
    reactor.listenTCP(8000, EchoFactory())
    print("Echo server started. Listening on port 8000...")
    reactor.run()
