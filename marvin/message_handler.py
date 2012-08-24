import constants
import random
import shlex
import glob
import re
import os


class MessageHandler(object):
    def __init__(self, conf, bot):
        self.conf = conf
        self.bot = bot
        self.handlers = [
                ('^{nick}: choose (.*)$'.format(nick=self.conf.nickname),
                self.handle_choose),
                ('^{nick}: yesno .*$'.format(nick=self.conf.nickname),
                self.handle_yesno),
                ('^.*{nick}.*\?$'.format(nick=self.conf.nickname),
                self.handle_question),
                ('^.*{nick}.*$'.format(nick=self.conf.nickname),
                self.handle_mention),
                ]
        self.load_all()

    def handle_msg(self, user, channel, msg):
        for pattern, handler in self.handlers:
            m = re.compile(pattern).match(msg)
            if m:
                handler(user, channel, msg, m)
                return

    def handle_question(self, user, channel, msg, m):
        n = random.randint(0, len(self.eightball) - 1)
        self.msg(channel, self.eightball[n])

    def handle_mention(self, user, channel, msg, m):
        n = random.randint(0, len(self.answers) - 1)
        self.msg(channel, self.answers[n])

    def handle_choose(self, user, channel, msg, m):
        if len(m.groups()):
            groups = shlex.split(m.group(1))
            self.msg(channel, groups[random.randint(0, len(groups) - 1)])
        else:
            self.msg(channel, "I can't really pick something from nothing, "
            "now can I?")

    def handle_yesno(self, user, channel, msg, m):
        self.msg(channel, random.choice(["Of course!", "Nah."]))

    def msg(self, channel, msg):
        self.bot.connection.privmsg(channel, msg)

    def load_all(self):
        self.bot.tui.msg(u'Reloading resources...')
        self.load_eightball()
        self.load_answers()
        self.load_sneer()
        self.bot.tui.msg(u'Done!')

    def load_eightball(self):
        self.eightball = open(os.path.join(constants.BASE,
            '../resources/eightball')).readlines()

    def load_answers(self):
        self.answers = open(os.path.join(constants.BASE,
            '../resources/answers')).readlines()

    def load_sneer(self):
        self.sneer = {}
        for f in glob.glob(os.path.abspath(os.path.join(constants.BASE,
            '../resources/sneer_*'))):
            data = open(f).readlines()
            self.sneer[os.path.basename(f)[6:]] = data
