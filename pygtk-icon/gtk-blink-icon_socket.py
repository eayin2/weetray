#!/usr/bin/python2.7
from twisted.internet import gtk2reactor
reactor = gtk2reactor.install()
from twisted.internet import reactor, protocol as p
import sys
import dbus
import xml.etree.ElementTree as ET
import elementtree
import time
import gtk
from subprocess import Popen, PIPE, STDOUT
''' Using twisted.internet.gtk2reactor to include the gtk app into reactors loop, else
    gtk.main() would block further execution and gtk.main can't be run with subprocess, because
    subprocess wants strings or list of strings as its parameter.
    After issuing gtk2reactor.install() we just have to set app = icon. Alternatively we could put
    the whole gtk definitions into a class and then run app = classname(). See: http://volteck.net/development/tag/twisted-2/
'''

def on_right_click(data, event_button, event_time):
    Popen(["/usr/bin/weetray-icon"],stdout=PIPE, stderr=STDOUT, shell=False)
    time.sleep(1)
    session_bus = dbus.SessionBus()
    proxy = session_bus.get_object('org.kde.konsole', "/Sessions")
    e = ET.fromstring(proxy.Introspect())
    for atype in e.findall('node'):
        session_id = atype.get('name')
        session_found = session_bus.get_object('org.kde.konsole', '/Sessions/' + session_id)
        if "weetray" in session_found.title(1):
            session_found.runCommand("/exit")
            time.sleep(1)
            session_found.runCommand("exit")
    icon.set_from_file("/usr/share/weetray/icons/red-tray.png")
    
def on_left_click(event):
    Popen(["/usr/bin/weetray-icon"],stdout=PIPE, stderr=STDOUT, shell=False)
    icon.set_blinking(False)
    icon.set_from_file("/usr/share/weetray/icons/green-tray.png")


class Echo(p.Protocol):
    def dataReceived(self, data):
        if (data == "blink"):
            icon.set_blinking(True)
        elif (data == "stop"):
            icon.set_blinking(False)
        elif (data == "start"):
            icon.set_from_file("/usr/share/weetray/icons/green-tray.png")
            icon.set_blinking(False)
        elif (data == "exit"):
            icon.set_blinking(False)
            icon.set_from_file("/usr/share/weetray/icons/red-tray.png")
            self.transport.loseConnection()
            self.transport.write(data)
        self.transport.write(data)


class EchoFactory(p.Factory):
    def buildProtocol(self, addr):
        return Echo()

if __name__ == '__main__':
    icon = gtk.status_icon_new_from_file("/usr/share/weetray/icons/green-tray.png")
    icon.connect('popup-menu', on_right_click)
    icon.connect('activate', on_left_click)
    app = icon
    try:
        reactor.listenTCP(5008, EchoFactory())
    except:
        sys.exit()
    reactor.run()
