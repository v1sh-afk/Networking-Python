from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class FileSender(DatagramProtocol):
    def startProtocol(self):
        self.transport.connect('127.0.0.1', 8000)
        file_path = "myfile.txt"
        with open(file_path, 'rb') as f:
            self.file_data = f.read()
        self.transport.write(self.file_data)

if __name__ == '__main__':
    reactor.listenUDP(0, FileSender())
    reactor.run()
