from twisted.internet import reactor, protocol, endpoints

class UpperProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write("hi, welcome\n")
        self.factory.amount +=1 
        print 'client amount =', self.factory.amount

    def connectionLost(self, reason):
        self.factory.amount -= 1
        print 'client amount =', self.factory.amount

    def dataReceived(self, data):
        self.transport.write(data.upper())
        #self.transport.loseConnection()



class MyFactory(protocol.ServerFactory):
    amount = 0


factory = MyFactory()
factory.protocol = UpperProtocol

endpoints.serverFromString(reactor, "tcp:8080").listen(factory)
reactor.run()
