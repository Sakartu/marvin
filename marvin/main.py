#!/usr/bin/env python

from bot import MarvinBot
from tui import MarvinTUI

import threading
import config

# see http://www.devshed.com/c/a/Python/IRC-on-a-Higher-Level/1/

if __name__ == '__main__':
    args = config.parse_options()
    conf = config.parse_config(args)
    all_joined = threading.Event()
    tui = MarvinTUI(conf)
    bot = MarvinBot(conf, tui, all_joined)
    bot.start()
    all_joined.wait()
    try:
        tui.cmdloop()
    except KeyboardInterrupt:
        tui.do_quit()
