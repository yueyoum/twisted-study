import sys
from twisted.internet import reactor, protocol, endpoints, defer

class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(self.factory.text)
        self.transport.write('\r\n')
        self.buffer = []

    def dataReceived(self, data):
        self.buffer.append(data)

    def connectionLost(self, reason):
        res = ''.join(self.buffer)
        self.factory.deferred.callback(res)


class ClientFactory(protocol.ClientFactory):
    protocol = ClientProtocol


def gotData(data, request):
    print 'response reqest for', request
    print data

if __name__ == '__main__':
    data = sys.argv[1:]
    endpoint = endpoints.clientFromString(reactor, "tcp:host=127.0.0.1:port=8080")
    deferred_list = []
    for _d in data:
        print 'sending', _d
        factory = ClientFactory()
        factory.protocol = ClientProtocol
        factory.text = _d

        d = defer.Deferred()
        d.addCallback(gotData, _d)
        deferred_list.append(d)

        factory.deferred = d
        endpoint.connect(factory)

    deferredList = defer.DeferredList(deferred_list)
    def finish(results):
        print 'finish'
        reactor.stop()

    deferredList.addCallback(finish)

    reactor.run()
