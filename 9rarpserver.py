from twisted.internet import reactor, protocol
import struct

class RARPServer(protocol.Protocol):
    def connectionMade(self):
        print("client connected")
 
    def dataReceived(self, data):
        global rarp_table
        rec = eval(data.decode())
        ip_address = '0.0.0.0'
        
        rarp_packet_format = "!6s4s6s4s"
        rarp_data = struct.unpack(rarp_packet_format, rec.get('req_format'))
        (
            Source_Hardware_Address,
            Source_Protocol_Address,
            Target_Hardware_Address,
            Target_Protocol_Address
        ) = rarp_data
        
        print("Received RARP packet:")
        print("Source Hardware Address:", ":".join("{:02x}".format(byte) for byte in Source_Hardware_Address))
        print("Source Protocol Address:", ".".join(str(byte) for byte in Source_Protocol_Address))
        print("Target Hardware Address:", ":".join("{:02x}".format(byte) for byte in Target_Hardware_Address))
        print("Target Protocol Address:", ".".join(str(byte) for byte in Target_Protocol_Address))
 
        if rec.get('req') == "RARP_REQUEST":
            for i in rarp_table:
                if i == rec.get('mac'):
                    ip_address = rarp_table[i]
                else:
                    continue 
            l = []
            for i in ip_address.split('.'):
                l.append(int(i))
                
            mac_address = rec.get('mac')
            response_packet = struct.pack(
                rarp_packet_format,
                Target_Hardware_Address,
                Target_Protocol_Address,
                Source_Hardware_Address,
                bytes(l),
            )
            
            to_client = {'reply_format': response_packet}
            
            if ip_address != '0.0.0.0':
                rarp_reply = f'RARP_REPLY {mac_address} {ip_address}\n'
                to_client['data'] = rarp_reply
                self.transport.write(str(to_client).encode())
                print("IP Address sent")
            else:
                self.transport.write(b'hi')
                print("Invalid MAC received")
    
    def connectionLost(self, reason):
        print("client removed")
        return

class RARPServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return RARPServer()

rarp_table = {}
rarp_table['00:11:22:33:44:55'] = '192.168.1.1'

reactor.listenTCP(1234, RARPServerFactory())
reactor.run()
