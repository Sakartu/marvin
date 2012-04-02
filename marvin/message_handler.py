import re
import random
import constants
import shlex

class MessageHandler(object):
    def __init__(self, conf, bot):
        self.conf = conf
        self.bot = bot
        self.handlers = [
                ('^{nick}.*\?$'.format(nick=self.bot.nickname),
                self.handle_question),
                ('^.*{nick}.*$'.format(nick=self.bot.nickname),
                self.handle_mention),
                ('^.*{nick}: choose (.*)$'.format(nick=self.bot.nickname),
                self.handle_choose),
                ]

    def handle(self, user, channel, msg):
        for pattern, handler in self.handlers:
            m = re.compile(pattern).match(msg)
            if m:
                handler(user, channel, msg, m)
                return

    def handle_question(self, user, channel, msg, m):
        n = random.randint(0, len(constants.EIGHTBALL) - 1) 
        self.bot.msg(channel, constants.EIGHTBALL[n])

    def handle_mention(self, user, channel, msg, m):
        n = random.randint(0, len(constants.ANSWERS) - 1) 
        self.bot.msg(channel, constants.ANSWERS[n])

    def handle_choose(self, user, channel, msg, m):
        if len(m.groups):
            groups = shlex.split(m.group(1))
            self.bot.msg(groups[random.randint(0, len(groups) - 1)])
        else:
            self.bot.msg("I can't really pick something from nothing, now can I?")

    def handle_yesno(self, user, channel, msg, m):
        self.bot.msg(random.choose(["Of course!", "Nah."]))
