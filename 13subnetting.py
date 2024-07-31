from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineOnlyReceiver
import ipaddress

SUBNET = ipaddress.IPv4Network("192.168.0.0/24")
print(SUBNET)
class SubnetCheckerProtocol(LineOnlyReceiver):
    def connectionMade(self):
        self.sendLine(b"Enter an IP address to check:")

    def lineReceived(self, line):
        ip_address = line.strip().decode()
        if self.is_in_subnet(ip_address):
            self.sendLine(b"IP address is within the subnet")
        else:
            self.sendLine(b"IP address is outside the subnet")
        self.transport.loseConnection()

    def is_in_subnet(self, ip_address):
        try:
            ip = ipaddress.IPv4Address(ip_address)
            return ip in SUBNET
        except ipaddress.AddressValueError:
            return False

class SubnetCheckerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return SubnetCheckerProtocol()

if __name__ == "__main__":
    reactor.listenTCP(8000, SubnetCheckerFactory())
    print("Subnet checker server is running...")
    reactor.run()
