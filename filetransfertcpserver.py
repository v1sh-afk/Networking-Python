from twisted.internet import reactor, protocol
import os
import time

BUFFER_SIZE = 32
BUFFER_FILENAME = 1024
SERVER_PORT = 12345

class FileServer(protocol.Protocol):
    def connectionMade(self):
        print('Waiting for connection')

    def dataReceived(self, data):
        self.transport.pauseProducing()  # Pause receiving data

        start = time.time()  # Start timer
        client_addr = self.transport.getPeer()
        print(client_addr, ' connected')

        file_name = data.decode()  # Receive file name
        file_name = os.path.basename(file_name)

        fd = open(file_name, 'rb')  # Open file in read mode
        buf = fd.read(BUFFER_SIZE)  # Read from file equal to buffer size

        print('Sending Data')

        while buf:
            self.transport.write(buf)  # Send data to the client
            buf = fd.read(BUFFER_SIZE)

        fd.close()  # Close file

        end = time.time()  # End timer
        print(f"Time taken to upload: {end - start} sec")
        print(file_name, " uploaded")

        self.transport.loseConnection()  # Close connection

    def connectionLost(self, reason):
        reactor.stop()


class FileServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return FileServer()


if __name__ == '__main__':
    reactor.listenTCP(SERVER_PORT, FileServerFactory())
    print('Starting server on port', SERVER_PORT)
    reactor.run()
