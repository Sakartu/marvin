from ircbot import SingleServerIRCBot
from message_handler import MessageHandler
from github import IssuePoller
import irclib

irclib.DEBUG = False

class Marvin(SingleServerIRCBot):
    def __init__(self, conf, tui):
        SingleServerIRCBot.__init__(self, [(conf.server, conf.port)], 
                conf.nickname, conf.nickname)
        self.conf = conf
        self.tui = tui
        tui.bot = self
        self.handler = MessageHandler(conf, self)
        self.pollers = []
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
        if self.joined == self.conf.channels:
            self.tui.start()

    def on_privmsg(self, c, e):
        self.handle_msg(c, e)

    def on_pubmsg(self, c, e):
        self.handle_msg(c, e)

    def handle_msg(self, c, e):
        user = irclib.nm_to_n(e.source())
        channel = e.target()
        msg = e.arguments()[0]
        self.handler.handle_msg(user, channel, msg)

    def broadcast(self, msg):
        for c in self.conf.channels:
           self.connection.privmsg(c, msg)
