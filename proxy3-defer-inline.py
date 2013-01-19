from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from twisted.web.client import getPage
from twisted.internet import defer

import time


class ProxyProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        if not line.startswith("http://"):
            return

        self.getPage(line)

    @defer.inlineCallbacks
    def getPage(self, line):
        starttime = time.time()
        print 'fetching', line
        html = yield getPage(line)

        print 'fetched', line
        self.transport.write(html)
        self.transport.loseConnection()
        print 'took', time.time() - starttime

        


factory = protocol.ServerFactory()
factory.protocol = ProxyProtocol

endpoints.serverFromString(reactor, "tcp:8080").listen(factory)
reactor.run()

