from twisted.internet import reactor, protocol 
import os

class FileTransferClientProtocol(protocol.Protocol):
    def connectionMade(self): 
        try: 
            f = open("myfile.txt", "rb") 
            self.fileData = f.read() 
            f.close()
            if len(self.fileData) == 0: 
                print("File is empty.") 
                self.transport.loseConnection() 
            else: 
                self.transport.write(b"SEND") 
        except FileNotFoundError: 
            print("File not found.") 
            self.transport.loseConnection()

    def dataReceived(self, data): 
        if data == b"READY": 
            if self.fileData: 
                self.transport.write(self.fileData) 
            else: 
                self.transport.loseConnection() 
        elif data == b"RECEIVED":
            print("File transfer complete.") 
            self.transport.loseConnection() 
        else:
            print("Error:", data.decode()) 
            self.transport.loseConnection() 

class FileTransferClientFactory(protocol.ClientFactory): 
    protocol = FileTransferClientProtocol 

if __name__ == "__main__":
    reactor.connectTCP("localhost", 7000, FileTransferClientFactory()) 
    reactor.run() 
