import subprocess
from twisted.internet import reactor

class Ping:
    def ping(self,host):
        process=subprocess.Popen(['ping',host], stdout=subprocess.PIPE)
        output,_=process.communicate()
        print(output.decode())

protocol=Ping()
protocol.ping('google.com')
reactor.run()