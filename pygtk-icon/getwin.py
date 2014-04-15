#!/usr/bin/python2.7
import gtk
import wnck
import glib
import sys
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


class WindowTitle(object):
    def __init__(self):
        self.title = None
        glib.timeout_add(100, self.get_title)
# The glib.timeout_add() function sets a function (specified by callback) to be called 
# at regular intervals (specified by interval, with the default priority, glib.PRIORITY_DEFAULT
# First Parameter is in milliseconds, so every 100 milliseconds self.get_title is called
    def get_title(self):
        try:
            title = wnck.screen_get_default().get_active_window().get_name()
            if self.title != title:
                if "weetray" in str(title):
                    reactor.connectTCP('localhost', conf["socket_port"], EchoClientFactory('stop'))
                    reactor.run()
                    sys.exit()
                self.title  = title
        except AttributeError:
            pass
        return True

# Enter the main event loop, and wait for user interaction 
WindowTitle()
gtk.main()
