from twisted.internet import protocol, reactor, endpoints, defer
from twisted.protocols.basic import LineReceiver
from twisted.web.client import getPage

class CacheProtocol(LineReceiver):
    def lineReceived(self, line):
        if not line.startswith("http://"):
            return

        deferredData = self._getPage(line)
        deferredData.addCallback(self.sendAndClose)

    def _getPage(self, line):
        if line in self.factory.caches:
            print 'found in cache', line
            return defer.succeed(self.factory.caches[line])

        print 'fetching', line
        d = getPage(line)
        d.addCallback(self._storeCache, line)
        return d

    def _storeCache(self, data, line):
        print 'fetched', line
        self.factory.caches[line] = data
        return data

    def sendAndClose(self, data):
        self.transport.write(data)
        self.transport.loseConnection()


class CacheFactory(protocol.ServerFactory):
    protocol = CacheProtocol
    caches = {}


endpoints.serverFromString(reactor, "tcp:8080").listen(CacheFactory())
reactor.run()

