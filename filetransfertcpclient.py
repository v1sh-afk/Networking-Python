from twisted.internet import reactor, protocol
import os
import time

BUFFER_SIZE = 32
HOST = 'localhost'
PORT = 12345

class FileClient(protocol.Protocol):
    def connectionMade(self):
        print('Connecting to', HOST)
        self.transport.write(file_name.encode())  # Send filename

        self.file_name = file[0] + "+Protocol=TCP" + "+" + str(os.getpid()) + "." + file[1]
        self.file = open(self.file_name, 'wb')

        print('Receiving Data')

    def dataReceived(self, data):
        self.file.write(data)

    def connectionLost(self, reason):
        self.file.close()  # Close the file
        reactor.stop()

if __name__ == '__main__':
    print("Enter the corresponding number to download book:")
    print("1. Atlas Shrugged by Ayn Rand")
    print("2. Don Quixote by Miguel de Cervantes")
    print("3. Shogun by James Clavell")
    print("4. The Stand by Stephen King")
    print("5. War and Peace by Leo Tolstoy")

    file_number = int(input())

    if file_number == 1:
        file_name = "Atlas Shrugged.txt"
    elif file_number == 2:
        file_name = "Don Quixote.txt"
    elif file_number == 3:
        file_name = "Shogun.txt"
    elif file_number == 4:
        file_name = "The Stand.txt"
    elif file_number == 5:
        file_name = "War and Peace.txt"

    file = file_name.split('.')

    factory = protocol.ClientFactory()
    factory.protocol = FileClient

    reactor.connectTCP(HOST, PORT, factory)
    print('Connected')
    start = time.time()  # Start timer
    reactor.run()

    end = time.time()  # End timer
    print(f"Time taken to download: {end - start} sec")
    file_stat = os.stat(file_name)
    file_size = file_stat.st_size
    throughput = round((file_size * 0.001) / (end - start), 3)
    print("Downloaded", file_name)
    print("Throughput:", throughput, "kB/s")
