import weechat, string, pynotify
from subprocess import Popen
weechat.register("lnotify", "kevr", "0.1.3", "GPL3", "lnotify - A libnotify script for weechat", "", "")

# Set up here, go no further!
settings = {
    "show_highlight"     : "on",
    "show_priv_msg"      : "on",
    "show_icon"          : "weechat"
}

# Init everything
if not pynotify.init("WeeChat"):
    print "Failed to load lnotify"

for option, default_value in settings.items():
    if weechat.config_get_plugin(option) == "":
        weechat.config_set_plugin(option, default_value)

# Hook privmsg/hilights
weechat.hook_print("", "irc_privmsg", "", 1, "get_notified", "")

# Functions
def get_notified(data, bufferp, uber_empty, tagsn, isdisplayed,
        ishilight, prefix, message):

    if (weechat.buffer_get_string(bufferp, "localvar_type") == "private" and
            weechat.config_get_plugin('show_priv_msg') == "on"):
        buffer = (weechat.buffer_get_string(bufferp, "short_name") or
                weechat.buffer_get_string(bufferp, "name"))
        if buffer == prefix:
            n = pynotify.Notification("WeeChat", "%s said: %s" % (prefix,
                message),weechat.config_get_plugin('show_icon'))
            Popen("/usr/bin/python2.7 /usr/share/weetray/main.py", shell=True)
            if not n.show():
                print "Failed to send notification"

    elif (ishilight == "1" and
            weechat.config_get_plugin('show_highlight') == "on"):
        buffer = (weechat.buffer_get_string(bufferp, "short_name") or
                weechat.buffer_get_string(bufferp, "name"))
        n = pynotify.Notification("WeeChat", "In %s, %s said: %s" % (buffer,
            prefix, message),weechat.config_get_plugin('show_icon'))
        Popen("/usr/bin/python2.7 /usr/share/weetray/main.py", shell=True)
        if not n.show():
            print "Failed to send notification"

    return weechat.WEECHAT_RC_OK

