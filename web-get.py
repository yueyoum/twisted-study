import sys
from twisted.internet import reactor, protocol, defer, endpoints

class HTTPGETProtocol(protocol.Protocol):
    def connectionMade(self):
        self.buffer = []
        self.sendRequest()

    def sendRequest(self):
        self.transport.write('GET %s HTTP/1.1\r\n' % self.factory.path)
        self.transport.write('User-Agent: twisted-python\r\n')
        self.transport.write('Host: %s\r\n' % self.factory.host)
        self.transport.write('Connection: close\r\n')
        self.transport.write('\r\n')

    def dataReceived(self, data):
        self.buffer.append(data)

    def connectionLost(self, reason):
        self.factory.deferred.callback(''.join(self.buffer))


def get(host, path):
    f = protocol.ClientFactory()
    f.protocol = HTTPGETProtocol
    f.path = path
    f.host = host
    f.deferred = defer.Deferred()
    endpoints.clientFromString(reactor, "tcp:host=%s:port=80" % host).connect(f)

    return f.deferred


if __name__ == '__main__':
    arg = sys.argv[1]
    arg = arg.lstrip('http://')
    if '/' in arg:
        host, path = arg.split('/', 1)
    else:
        host, path = arg, '/'
    print host, path
    def output(data):
        print data
        reactor.stop()

    d = get(host, path)
    d.addCallback(output)

    reactor.run()




