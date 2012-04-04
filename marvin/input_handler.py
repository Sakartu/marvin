import threading
import string

class InputHandler(threading.Thread):
    def __init__(self, conf, bot):
        threading.Thread.__init__(self)
        self.daemon = True
        self.conf = conf
        self.bot = bot

    def run(self):
        chan, text = self.parse_inp(raw_input())
        while True:
            if chan in self.conf.channels:
                self.bot.msg(chan, text)
                print u'Message sent to {chan}!'.format(chan=chan)
            else:
                print u'Not joined in {chan}!'.format(chan=chan)
            chan, text = self.parse_inp(raw_input())

    def parse_inp(self, inp):
        chan, text = string.split(inp, maxsplit=1)
        if not chan.startswith('#'):
            chan = '#' + chan
        return chan, text
