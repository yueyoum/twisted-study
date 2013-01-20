from twisted.internet import reactor

def output(data):
    print data


delayedCall = reactor.callLater(3, output, 'aaa')

def abort():
    if delayedCall.active():
        print 'cancelling'
        delayedCall.cancel()


reactor.callLater(4, abort)
reactor.callLater(5, reactor.stop)

reactor.run()
