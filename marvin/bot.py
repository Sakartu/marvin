from twisted.words.protocols import irc
from twisted.internet import protocol
from message_handler import MessageHandler
from github import IssuePoller

class Marvin(irc.IRCClient):

    def _get_nickname(self):
        return self.factory.conf.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        for chan in self.factory.conf.channels:
            self.join(chan)
        print "Signed on as %s." % (self.nickname,)
        print "Starting github pollers"
        for p in self.factory.pollers:
            p.start()

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        if not user:
            return
        else:
            self.handler.handle(user, channel, msg)

    def broadcast(self, msg):
        for chan in self.factory.conf.channels:
            print chan, '->', msg
            self.msg(chan, msg)

class MarvinFactory(protocol.ClientFactory):
    protocol = Marvin

    def __init__(self, conf):
        self.conf = conf

    def buildProtocol(self, addr):
        bot = Marvin()
        bot.factory = self
        bot.handler = MessageHandler(self.conf, bot)
        self.pollers = []
        for (user, project) in self.conf.issues:
            p = IssuePoller(self.conf, bot, user, project, project == 'marvin')
            print 'Built poller for {user}/{project}'.format(user=user, 
                    project=project)
            self.pollers.append(p)
        return bot

    def clientConnectionLost(self, connector, reason):
        print "Lost connection!"
        for p in self.pollers:
            p.cancel()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

