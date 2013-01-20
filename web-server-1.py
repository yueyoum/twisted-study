import sys

from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
from twisted.internet import reactor, endpoints
from twisted.python import log

log.startLogging(sys.stdout)

class LongRunning(Resource):
    def render_GET(self, request):

        request.write('A')
        reactor.callLater(1, request.write, 'B')
        reactor.callLater(2, request.write, 'C')
        reactor.callLater(3, request.finish)
        return NOT_DONE_YET


root = Resource()
root.putChild('long', LongRunning())
factory = Site(root)

endpoints.serverFromString(reactor, "tcp:8080").listen(factory)

reactor.run()

