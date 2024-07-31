from twisted.internet import reactor, protocol


class DNSProtocol(protocol.Protocol):
    def dataReceived(self, data):
        request = data.strip()
        response = self.processRequest(request)
        self.transport.write(response)

    def processRequest(self, request):
        # Replace this logic with your own DNS processing
        # Here, we simply return a hardcoded response
        if request == b"www.example.com":
            return b"192.168.0.1"
        else:
            return b"Unknown domain"

class DNSFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return DNSProtocol()


if __name__ == "__main__":
    reactor.listenTCP(53, DNSFactory())
    print("DNS server is running...")
    reactor.run()
