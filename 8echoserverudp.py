from twisted.internet import reactor,protocol

class UDPServer(protocol.DatagramProtocol):
    def datagramReceived(self, data, addr):
        print("Recieved message from",addr[0],": ",data.decode())
        self.transport.write(data,addr)
        
    


server_port=8000
server=reactor.listenUDP(server_port,UDPServer())
print("Server started on port",server_port)

reactor.run()