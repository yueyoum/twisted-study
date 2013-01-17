from twisted.internet import protocol, reactor, endpoints
from twisted.protocols import basic

class MyProtocol(protocol.Protocol):
    def connectionMade(self):
        self.buffer = []

    def dataReceived(self, data):
        self.buffer.append(data)
        if '\r\n' in data:
            line, rest = ''.join(self.buffer).split('\n', 1)
            self.buffer = [rest]
            print line
        else:
            print 'no line'


class LineProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        print line


factory = protocol.ServerFactory()
#factory.protocol = MyProtocol
factory.protocol = LineProtocol

endpoints.serverFromString(reactor, "tcp:8080").listen(factory)
reactor.run()
