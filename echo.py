# -*- coding: utf-8 -*-

from twisted.internet import reactor, protocol, endpoints

class UpperProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.amount +=1 
        #self.transport.write("hi, there are %d clients\n" % self.factory.amount)

    def connectionLost(self, reason):
        self.factory.amount -= 1

    def dataReceived(self, data):
        self.transport.write(data.upper())
        self.transport.loseConnection()



class MyFactory(protocol.ServerFactory):
    protocol = UpperProtocol
    amount = 0


endpoints.serverFromString(reactor, "tcp:8080").listen(MyFactory())
reactor.run()

# reactor 会一直循环，直到关闭socket连接
# reactor 使用factory作用于连接
# factory 为每一个client 建立一个protocol 实例
# factory 或者 protocol 通过实例，或者实现类的方法来添加功能

