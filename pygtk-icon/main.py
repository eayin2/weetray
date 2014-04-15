#!/usr/bin/python2.7
import os
import sys
import signal
from subprocess import Popen, PIPE, call, STDOUT
import time
from twisted.internet import reactor, protocol as p
conf = {}
execfile("/usr/share/weetray/weetray.conf", conf)


class EchoClient(p.Protocol):
    def connectionMade(self):
        self.transport.write(self.factory.data)

    def dataReceived(self, data):
        #print 'Received:', data
        self.transport.loseConnection()
        # Stopping the reactor loop, after getting the server response
        reactor.stop()


class EchoClientFactory(p.ClientFactory):
    protocol = EchoClient
    def __init__(self, data):
        self.data = data

reactor.connectTCP('localhost', conf["socket_port"], EchoClientFactory('blink'))
reactor.run()
p1 = Popen(["/usr/share/weetray/osd_cat_extern"], stdout=PIPE, stderr=STDOUT, shell=False, preexec_fn=os.setsid)
p2 = Popen(["/usr/share/weetray/getwin.py"], stdout=PIPE, stderr=STDOUT, shell=False, preexec_fn=os.setsid)


