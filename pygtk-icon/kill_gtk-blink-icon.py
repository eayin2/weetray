#!/usr/bin/python2.7
import sys
from twisted.internet import reactor, protocol as p
conf = {}
execfile("/usr/share/weetray/weetray.conf", conf)


class EchoClient(p.Protocol):
    def connectionMade(self):
        self.transport.write(self.factory.data)

    def connectionLost(self, reason):
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        reactor.stop()
 
    def clientConnectionFailed(self, connector, reason):
        reactor.stop()


class EchoClientFactory(p.ClientFactory):
    protocol = EchoClient
    def __init__(self, data):
        self.data = data

reactor.connectTCP('localhost', conf["socket_port"], EchoClientFactory('exit'))
reactor.run()
