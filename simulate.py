from twisted.internet import protocol, reactor
import socket
import time


class PingProtocol(protocol.DatagramProtocol):
    def __init__(self, host):
        self.host = host

    def startProtocol(self):
        self.transport.connect(self.host, 80)

    def datagramReceived(self, data, addr):
        print("Ping response from {}: {}".format(addr[0], data.decode()))

    def ping(self):
        self.transport.write(b"Ping")


class TracerouteProtocol(protocol.DatagramProtocol):
    def __init__(self, host, ttl=1):
        self.host = host
        self.ttl = ttl
        self.startTime = 0
        self.socket = None
        self.timeoutCall = None

    def startProtocol(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, self.ttl)
        self.socket.bind(('0.0.0.0', 0))
        self.transport.connect(self.host, 80)
        self.transport.write(b"Traceroute")
        self.startTime = time.time()
        self.timeoutCall = reactor.callLater(5, self.timeoutCallback)

    def datagramReceived(self, data, addr):
        elapsedTime = (time.time() - self.startTime) * 1000
        print("Traceroute response from {} ({} ms)".format(addr[0], elapsedTime))
        self.timeoutCall.cancel()
        reactor.stop()

    def timeoutCallback(self):
        print("Traceroute timeout")
        reactor.stop()

    def traceroute(self):
        self.transport.write(b"Traceroute")


# Resolve domain name to IP address
def resolve_address(host):
    try:
        ip_address = socket.gethostbyname(host)
        return ip_address
    except socket.gaierror:
        print("Error: Unable to resolve host address")
        return None


# Simulate ping
def simulate_ping(host):
    ip_address = resolve_address(host)
    if ip_address:
        ping_protocol = PingProtocol(ip_address)
        reactor.listenUDP(0, ping_protocol)
        ping_protocol.ping()


# Simulate traceroute
def simulate_traceroute(host):
    ip_address = resolve_address(host)
    if ip_address:
        for ttl in range(1, 31):
            traceroute_protocol = TracerouteProtocol(ip_address, ttl)
            reactor.listenUDP(0, traceroute_protocol)
            traceroute_protocol.traceroute()


# Test
simulate_ping("google.com")
simulate_traceroute("google.com")

# Run the reactor
reactor.run()
