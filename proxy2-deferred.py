from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from twisted.web.client import getPage

#import urllib2
import time


class ProxyProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        if not line.startswith("http://"):
            return

        start = time.time()
        print 'fetching', line
        deferred = getPage(line)
        deferred.addCallback(self.afterGetData, line, start)


    def afterGetData(self, data, line, starttime):
        print 'fetched', line
        self.transport.write(data)
        self.transport.loseConnection()
        print 'took', time.time() - starttime
        


factory = protocol.ServerFactory()
factory.protocol = ProxyProtocol

endpoints.serverFromString(reactor, "tcp:8080").listen(factory)
reactor.run()

