from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineOnlyReceiver 

class ChatProtocol(LineOnlyReceiver): 
    def __init__(self, factory): 
        self.factory = factory 
        self.name = None 
        self.state = "GETNAME" 
        self.client = None 

    def lineReceived(self, line):
        if self.state == "GETNAME": 
            self.handle_GETNAME(line.decode()) 
        else: 
            self.handle_CHAT(line.decode()) 

    def handle_GETNAME(self, name): 
        if name in self.factory.users: 
            self.sendLine("Name already taken, please choose another name.".encode()) 
            return 
        self.sendLine(f"Welcome, {name}!".encode()) 
        self.broadcastMessage(f"{name} has joined the chat room.") 
        self.name = name
        self.factory.users[name] = self
        self.state = "CHAT" 

    def handle_CHAT(self, message): 
        if message.lower() == "/quit": 
            self.transport.loseConnection() 
        else: 
            message = f"<{self.name}> {message}" 
            self.broadcastMessage(message) 

    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.items(): 
            if protocol != self: 
                protocol.sendLine(message.encode()) 

    def connectionMade(self): 
        self.sendLine("Connected to the chat server. Type '/quit' to exit.".encode()) 
        self.factory.clients.append(self) 

    def connectionLost(self, reason): 
        self.factory.clients.remove(self)

class ChatFactory(protocol.Factory): 
    def __init__(self): 
        self.users = {} 
        self.clients = [] 

    def buildProtocol(self, addr): 
        return ChatProtocol(self) 
           
if __name__ == "__main__": 
    reactor.listenTCP(9000, ChatFactory()) 
    print("Chat server started. Listening on port 9000...") 
    reactor.run() 