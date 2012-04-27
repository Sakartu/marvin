import threading
import util
import cmd
import sys

class MarvinTUI(threading.Thread, cmd.Cmd):
    def __init__(self, conf):
        cmd.Cmd.__init__(self)

        self.conf = conf
        self.bot = None
        self.running = True
        self.prompt = u'marvin$ '
        self.intro = u'Welcome to marvin, the depressed IRC bot'
        self.doc_header = u'Commands (press help <command> to get help):'

    def cmdloop(self):
        while self.running:
            try:
                cmd.Cmd.cmdloop(self)
            except UserCancelled:
                self.intro = u''
                continue

    def preloop(self):
        self.do_help("")

    def postloop(self):
        print

    def precmd(self, line):
        if line == "EOF":
            raise UserCancelled
        else:
            return line

    def do_join(self, line=None):
        if not line:
            self.help_join()
            return
        for c in line.split():
            self.bot.connection.join(util.get_channel(c))

    def help_join(self):
        print u'Join one or more channels given as arguments.'
        print u'usage: join [channel]...'

    def do_say(self, line=None):
        if not line:
            self.help_say()
            return
        (target, msg) = tuple(line.split(None, 1))
        self.bot.connection.privmsg(target, msg)

    def help_say(self):
        print u'Say something to a target (channel or user)'
        print u'usage: say [target] <msg>'

    def do_broadcast(self, line=None):
        pass

    def help_broadcast(self, line=None):
        pass

    def do_quit(self, line=None):
        '''
        Quits the program
        '''
        print u'\nDisconnecting and exitting...'
        if self.bot:
            for p in self.bot.pollers:
                p.cancel()
            self.bot.die()
        sys.exit(0)

    def help_quit(self):
        print u'Quit the application'

    def help_help(self):
        print u'Get help about a topic'

class TUIException(Exception):
    '''
    A TUI exception
    '''
    pass

class UserCancelled(TUIException):
    '''
    This class is raised when the user presses ^D in the TUI
    '''
    pass
