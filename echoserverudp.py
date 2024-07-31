from twisted.internet import reactor, protocol

class EchoProtocol(protocol.DatagramProtocol):
    def datagramReceived(self, data, addr):
        print(f"Received from {addr}: {data.decode()}")
        self.transport.write(data, addr)
    def startProtocol(self):
        print("Echo server started. Listening on port 8000...")

if __name__ == '__main__':
    reactor.listenUDP(8000, EchoProtocol(), interface="127.0.0.1")

    reactor.run()
