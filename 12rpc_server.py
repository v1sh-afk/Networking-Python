from twisted.internet import reactor, protocol


class RPCServerProtocol(protocol.Protocol):
    def dataReceived(self, data):
        request = data.decode().strip()
        result = self.processRequest(request)
        self.transport.write(result.encode())

    def processRequest(self, request):
        # Process the request and return the result
        # Replace this with your own server-side logic
        if request == "add 10 5":
            return str(10 + 5)
        else:
            return "Invalid request"


class RPCServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return RPCServerProtocol()


if __name__ == "__main__":
    reactor.listenTCP(8000, RPCServerFactory())
    print("RPC server is running...")
    reactor.run()

