import re
import random
import constants

class MessageHandler(object):
    def __init__(self, bot):
        self.bot = bot
        self.handlers = {
                '^{nick}.*?$'.format(nick=self.bot.nickname) 
                : self.handle_question,
                '^.*{nick}.*$'.format(nick=self.bot.nickname) 
                : self.handle_mention,
                }

    def handle(self, user, channel, msg):
        for pattern, handler in self.handlers.items():
            if re.compile(pattern).match(msg):
                handler(user, channel, msg)

    def handle_question(self, user, channel, msg):
        n = random.randint(0, len(constants.EIGHTBALL) - 1) 
        self.bot.msg(channel, constants.EIGHTBALL[n])

    def handle_mention(self, user, channel, msg):
        n = random.randint(0, len(constants.ANSWERS) - 1) 
        self.bot.msg(channel, constants.ANSWERS[n])
