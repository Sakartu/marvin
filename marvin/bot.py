from irc.bot import SingleServerIRCBot
from message_handler import MessageHandler
from github import IssuePoller
import threading
import irc.client
import util

irc.client.DEBUG = False


class Marvin(SingleServerIRCBot):
    def __init__(self, conf, tui, all_joined):
        SingleServerIRCBot.__init__(self, [(conf.server, conf.port)],
                conf.nickname, conf.realname)
        self.conf = conf
        self.tui = tui
        tui.bot = self
        self.handler = MessageHandler(conf, self)
        self.pollers = []
        self.all_joined = all_joined
        self.joined = []
        for (user, project) in self.conf.issues:
            p = IssuePoller(conf, self, user, project)
            self.pollers.append(p)
            print u'Poller built for ' + user + '/' + project

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + '_')

    def on_welcome(self, c, e):
        print u'Connected, joining channels...'
        for chan in self.conf.channels:
            c.join(chan)

        for p in self.pollers:
            p.start()

    def on_join(self, c, e):
        self.joined.append(e.target())
        print u'Joined ' + e.target() + '!'
        if util.are_equal_lower(self.joined, self.conf.channels):
            self.all_joined.set()

    def on_privmsg(self, c, e):
        self.handle_msg(c, e)

    def on_pubmsg(self, c, e):
        self.handle_msg(c, e)

    def handle_msg(self, c, e):
        user = irc.client.nm_to_n(e.source())
        channel = e.target()
        msg = e.arguments()[0]
        self.handler.handle_msg(user, channel, msg)

    def broadcast(self, msg):
        for c in self.conf.channels:
            self.connection.privmsg(c, msg)


class MarvinBot(threading.Thread):
    def __init__(self, conf, tui, joined):
        threading.Thread.__init__(self)
        self.daemon = True
        self.bot = Marvin(conf, tui, joined)

    def run(self):
        self.bot.start()
