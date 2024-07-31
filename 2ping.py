import subprocess
from twisted.internet import reactor

class PingProtocol:
    def ping(self, host):
        process = subprocess.Popen(['ping', '-n', '4', host], stdout=subprocess.PIPE)
        output, _ = process.communicate()
        print(output.decode())
        
protocol = PingProtocol()
protocol.ping('google.com')
reactor.run()