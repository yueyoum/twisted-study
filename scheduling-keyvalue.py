from twisted.internet import reactor

class KeyValueStore(object):
    EXPIRE_TIME = 5
    def __init__(self):
        self.store = {}
        self.expire = {}


    def setExpireTime(self, key):
        self.expire[key] = reactor.callLater(self.EXPIRE_TIME, self.delete, key)

    def delete(self, key):
        self.cancelExpire(key)
        del self.store[key]

    def cancelExpire(self, key):
        delayedCall = self.expire.pop(key, None)
        if delayedCall and delayedCall.active():
            delayedCall.cancel()


    def set(self, key, value):
        self.cancelExpire(key)
        self.store[key] = value
        self.setExpireTime(key)

    def get(self, key):
        return self.store.get(key, None)


if __name__ == '__main__':
    store = KeyValueStore()
    store.set('a', 1)
    def store_get():
        print store.get('a')
    for i in range(10):
        reactor.callLater(i, store_get)

    reactor.callLater(i+1, reactor.stop)

    reactor.run()


