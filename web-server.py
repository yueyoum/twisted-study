import sys

from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import reactor, endpoints
from twisted.python import log

log.startLogging(sys.stdout)

class Index(Resource):
    def render_GET(self, request):
        return 'Hello'

class Page(Resource):
    def render_GET(self, request):
        return 'One page'

root = Resource()
root.putChild('', Index())
root.putChild('page', Page())
factory = Site(root)

endpoints.serverFromString(reactor, "tcp:8080").listen(factory)

reactor.run()
