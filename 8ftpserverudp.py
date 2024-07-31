from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class FileReceiver(DatagramProtocol):
    def datagramReceived(self, datagram, address):
        with open("received_file.txt", "wb") as f:
            f.write(datagram)

if __name__ == '__main__':
    reactor.listenUDP(8000, FileReceiver())
    reactor.run()
