from twisted.internet import reactor, protocol

class StopAndWaitServer(protocol.Protocol):
    def connectionMade(self):
        print("Client connected:", self.transport.getPeer())
        self.send_message()

    def send_message(self):
        message = input("Enter message: ")
        self.transport.write(message.encode())
        print("Message sent to client:", message)
        self.expected_ack = "ACK"
        # self.schedule_resend()

    def schedule_resend(self):
        self.resend_call = reactor.callLater(5, self.resend_message)

    def resend_message(self):
        print("ACK not received. Resending message...")
        self.send_message()

    def dataReceived(self, data):
        ack = data.decode()
        print("ACK received:", ack)
        if ack == self.expected_ack:
            # self.resend_call.cancel()
            print("ACK received. Message acknowledged.")
            self.send_message()
        else:
            print("Invalid ACK received.")
            self.schedule_resend()

    def connectionLost(self, reason):
        print("Client disconnected:")

class StopAndWaitServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return StopAndWaitServer()

server_port = 8000
factory = StopAndWaitServerFactory()
reactor.listenTCP(server_port, factory)
reactor.run()
