#!/usr/bin/env python

from bot import Marvin
from tui import MarvinTUI

import readline
import config
import util

# see http://www.devshed.com/c/a/Python/IRC-on-a-Higher-Level/1/

if __name__ == '__main__':
    args = config.parse_options()
    conf = config.parse_config(args)
    print u'Connecting to server...'
    tui = MarvinTUI(conf)
    completer = readline.get_completer()
    bot = Marvin(conf, tui)
    util.setup_signal_handlers(bot, completer)
    bot.start()
