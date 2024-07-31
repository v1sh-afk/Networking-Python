from twisted.internet import reactor,protocol

class UDPClient(protocol.DatagramProtocol):
    def startProtocol(self):
        self.transport.connect('127.0.0.2',8000)
        self.send_message()
    
    def send_message(self):
        message=input('Enter message: ')
        self.transport.write(message.encode())

    def datagramReceived(self, data, addr):
        print("Recieved message: ",data.decode())
        self.send_message()
    
client=reactor.listenUDP(0,UDPClient())
reactor.run()