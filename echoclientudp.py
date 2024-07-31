from twisted.internet import reactor, protocol

class EchoClient(protocol.DatagramProtocol):
    def startProtocol(self):
        self.transport.write(b"Hello, server!", ("127.0.0.1", 8000))

    def datagramReceived(self, data, addr):
        print(f"Received from {addr}: {data.decode()}")

if __name__ == '__main__':
    client = EchoClient()
    reactor.listenUDP(0, client)
    print("Echo client started. Sending data to server...")
    reactor.run()
