from twisted.internet import reactor, protocol
import struct

class RARPClient(protocol.Protocol):
    def connectionMade(self):
        rarp_packet_format = "!6s4s6s4s"
        request_packet = struct.pack(
            rarp_packet_format,
            bytes([00, 11, 22, 33, 44, 55]),  # Example source hardware address
            bytes([0, 0, 0, 0]),  # Example source protocol address
            bytes([17, 18, 19, 20, 21, 22]),  # Example target hardware address
            bytes([26, 27, 28, 29])  # Example target protocol address
        )
        a = input("Enter MAC address:")
        to_server = {'mac': a, 'req_format': request_packet, 'req': 'RARP_REQUEST'}
        self.transport.write(str(to_server).encode())
    
    def dataReceived(self, data):
        recv = eval(data.decode())
        rarp_packet_format = "!6s4s6s4s"
        (
            Source_Hardware_Address,
            Source_Protocol_Address,
            Target_Hardware_Address,
            Target_Protocol_Address
        ) = struct.unpack(rarp_packet_format, recv.get('reply_format'))
        
        print("Received RARP reply:")
        print("Source Hardware Address:", ":".join("{:02x}".format(byte) for byte in Source_Hardware_Address))
        print("Source Protocol Address:", ".".join(str(byte) for byte in Source_Protocol_Address))
        print("Target Hardware Address:", ":".join("{:02x}".format(byte) for byte in Target_Hardware_Address))
        print("Target Protocol Address:", ".".join(str(byte) for byte in Target_Protocol_Address))
        
        if recv.get('data').startswith('RARP_REPLY'):
            reply_parts = recv.get('data').split()
            if len(reply_parts) == 3:
                mac_address = reply_parts[1]
                ip_address = reply_parts[2]
                print(f"Received RARP reply: MAC = {mac_address}, IP = {ip_address}")
                self.transport.loseConnection()
            else:
                print("Invalid RARP reply")
                self.transport.loseConnection()
        else:
            print("Invalid MAC Address given!")
            self.transport.loseConnection()

class RARPClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return RARPClient()
    
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

reactor.connectTCP('localhost', 1234, RARPClientFactory())
reactor.run()
