import readline
import signal
import sys

def get_channel(line):
    if line.startswith('#'):
        return line
    else:
        return '#' + line

def setup_signal_handlers(bot, completer):
    def interrupt_handler(signum, frame):
        print u'Disconnecting and exitting...'
        for p in bot.pollers:
            p.cancel()
        bot.die()
        readline.set_completer(completer)
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt_handler)	
    signal.signal(signal.SIGTERM, interrupt_handler)	
