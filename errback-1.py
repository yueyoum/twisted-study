import sys
from twisted.internet import reactor
from twisted.web.client import getPage

def out_put(content):
    return content

def err(reason):
    return 'errors'


def finish(data):
    print data
    reactor.stop()

d = getPage(sys.argv[1])
d.addCallbacks(out_put, err)
d.addCallback(finish)

reactor.run()

