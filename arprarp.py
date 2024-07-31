from twisted.internet import reactor, protocol
from twisted.protocols import basic

class ARPServerProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        if line == b'ARP':
            self.transport.write(b'ARP Response')
        else:
            self.transport.write(b'Unknown command')

class RARPServerProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        if line == b'RARP':
            self.transport.write(b'RARP Response')
        else:
            self.transport.write(b'Unknown command')

class ARPClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(b'ARP')

    def dataReceived(self, data):
        print('Received:', data.decode())

class RARPClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(b'RARP')

    def dataReceived(self, data):
        print('Received:', data.decode())

def main():
    # Start the ARP server
    arp_server_factory = protocol.ServerFactory()
    arp_server_factory.protocol = ARPServerProtocol
    reactor.listenTCP(8000, arp_server_factory)

    # Start the RARP server
    rarp_server_factory = protocol.ServerFactory()
    rarp_server_factory.protocol = RARPServerProtocol
    reactor.listenTCP(8001, rarp_server_factory)

    # Connect to the ARP server
    arp_client_factory = protocol.ClientFactory()
    arp_client_factory.protocol = ARPClientProtocol
    reactor.connectTCP('localhost', 8000, arp_client_factory)

    # Connect to the RARP server
    rarp_client_factory = protocol.ClientFactory()
    rarp_client_factory.protocol = RARPClientProtocol
    reactor.connectTCP('localhost', 8001, rarp_client_factory)

    reactor.run()

if __name__ == '__main__':
    main()
