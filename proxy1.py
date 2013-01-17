from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic

import urllib2
import time

class ProxyProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        if not line.startswith("http://"):
            return

        self._parse(line)

    def _parse(self, line):
        start = time.time()
        print 'fetching', line
        data = urllib2.urlopen(line).read()
        print 'fetch done'

        self.transport.write(data)
        self.transport.loseConnection()

        print 'took', time.time() - start


factory = protocol.ServerFactory()
factory.protocol = ProxyProtocol

endpoints.serverFromString(reactor, "tcp:8080").listen(factory)
reactor.run()

