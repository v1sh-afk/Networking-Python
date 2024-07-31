from twisted.internet import reactor, protocol
import struct

class ARPServer(protocol.Protocol):
    def connectionMade(self):
        print("client connected")
    
    def dataReceived(self, data):
        global arp_table
        rec = eval(data.decode())
        mac_address = '0:0:0:0:0:0'
        
        arp_packet_format = "!6s4s6s4s"
        arp_data = struct.unpack(arp_packet_format, rec.get('req_format'))
        (
            Source_Hardware_Address,
            Source_Protocol_Address,
            Target_Hardware_Address,
            Target_Protocol_Address
        ) = arp_data
        
        print("Received ARP packet:")
        print("Source Hardware Address:", ":".join("{:02x}".format(byte) for byte in Source_Hardware_Address))
        print("Source Protocol Address:", ".".join(str(byte) for byte in Source_Protocol_Address))
        print("Target Hardware Address:", ":".join("{:02x}".format(byte) for byte in Target_Hardware_Address))
        print("Target Protocol Address:", ".".join(str(byte) for byte in Target_Protocol_Address))
        
        if rec.get('req') == "ARP_REQUEST":
            for i in arp_table:
                if i == rec.get('ip'):
                    mac_address = arp_table[i]
                else:
                    continue
            
            l = []
            for i in mac_address.split(':'):
                l.append(int(i))
            
            ip_address = rec.get('ip')
            response_packet = struct.pack(
                arp_packet_format,
                Target_Hardware_Address,
                Target_Protocol_Address,
                Source_Hardware_Address,
                bytes(l),
            )
            
            to_client = {'reply_format': response_packet}
            
            if mac_address != '0:0:0:0:0:0':
                arp_reply = f'ARP_REPLY {ip_address} {mac_address}\n'
                to_client['data'] = arp_reply
                self.transport.write(str(to_client).encode())
                print("MAC Address sent")
            else:
                self.transport.write(b'hi')
                print("Invalid IP received")
    
    def connectionLost(self, reason):
        print("client removed")
        return

class ARPServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ARPServer()

arp_table = {}
arp_table['192.168.1.1'] = '00:11:22:33:44:55'

reactor.listenTCP(1234, ARPServerFactory())
reactor.run()
