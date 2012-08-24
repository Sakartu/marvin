import util
import cmd
import sys
import curses
import curses.textpad
import datetime


class MarvinTUI(cmd.Cmd):
    def __init__(self, conf):
        cmd.Cmd.__init__(self)

        self.setup_screens()
        self.reroute_stdio()

        self.conf = conf
        self.bot = None
        self.running = True
        self.prompt = u'marvin$ '
        self.intro = u'Welcome to marvin, the depressed IRC bot'
        self.doc_header = u'Commands (press help <command> to get help):'
        self.msg(u'Connecting to server...')

    def cmdloop(self):
        while self.running:
            self.cmdwin.addstr(self.prompt)
            text = self.cmdwin.getstr()
            self.onecmd(text)

    def do_join(self, line=None):
        if not line:
            self.help_join()
            return
        for c in line.split():
            self.bot.connection.join(util.get_channel(c))

    def help_join(self):
        self.query(u'Join one or more channels given as arguments.')
        self.query(u'usage: join [channel]...')

    def do_reload(self, line=None):
        self.bot.handler.load_all()

    def help_reload(self):
        self.query(u'Reload all the resources (quotes and stuff)')

    def do_say(self, line=None):
        if not line:
            self.help_say()
            return
        (target, msg) = tuple(line.split(None, 1))
        self.bot.connection.privmsg(target, msg)

    def help_say(self):
        self.query(u'Say something to a target (channel or user)')
        self.query(u'usage: say [target] <msg>')

    def do_broadcast(self, line=None):
        pass

    def help_broadcast(self, line=None):
        pass

    def do_status(self, line=None):
        self.query(u'The bot is known as {nick}({real})'.format(
                nick=self.conf.nickname, real=self.conf.realname))
        self.query(u'{nick} is joined in:'.format(nick=self.conf.nickname))
        for i in self.conf.channels:
            self.query(i)

    def help_status(self, line=None):
        self.query(u'Print some status information about the bot, including '
                'which channels it\'s joined in')

    def do_quit(self, line=None):
        '''
        Quits the program
        '''
        self.query(u'\nDisconnecting and exitting...')
        if self.bot:
            for p in self.bot.pollers:
                p.cancel()
            self.bot.die()
        curses.endwin()
        sys.exit(0)

    def help_quit(self):
        self.query(u'Quit the application')

    def help_help(self):
        self.query(u'Get help about a topic')

    def setup_screens(self):
        self.screen = curses.initscr()
        self.maxy, self.maxx = self.screen.getmaxyx()

        # Left screen
        self.left = self.screen.subwin(self.maxy, self.maxx / 2, 0, 0)
        self.left.box()
        self.left.addstr(0, 3, 'Commands')
        self.left.leaveok(True)
        self.left.idlok(True)
        self.left.scrollok(True)
        innery, innerx = tuple(x + 1 for x in self.left.getbegyx())
        rows, cols = self.left.getmaxyx()
        innerrows = innery + rows - 3
        innercols = innerx + cols - 3
        self.cmdwin = self.left.subwin(innerrows, innercols, innery, innerx)

        # Right screen
        self.right = self.screen.subwin(self.maxy, self.maxx / 2, 0,
                self.maxx / 2)
        self.right.box()
        self.right.addstr(0, 3, 'Log')
        self.padmaxy, self.padmaxx = self.right.getmaxyx()
        self.rightpad = curses.newpad(1000, self.padmaxx)
        self.rightscroll = 0
        self.screen.refresh()
        self.msg('Setup done!')

    def reroute_stdio(self):
        query = self.query

        class NewOut(object):
            def write(self, m):
                query(m)

        self.stdout = NewOut()

    def query(self, m):
        self.cmdwin.addstr(m if m.endswith('\n') else m + '\n')

    def msg(self, m):
        m = datetime.datetime.now().strftime('[%x %X]: ') + unicode(m)
        self.rightpad.addstr(m if m.endswith('\n') else m + '\n')
        self.rightscroll += 1
        offset = self.rightscroll - self.padmaxy + 2
        self.rightpad.refresh(offset, 0, 1, self.padmaxx + 1,
                self.padmaxy - 2, self.maxx - 2)

    def write(self, m):
        self.msg(m)
