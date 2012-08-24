import cmd
import sys
import curses
import signal
import curses.textpad
import datetime


class MarvinTUI(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.setup_screens()
        signal.signal(signal.SIGWINCH, self.setup_screens)
        self.reroute_stdio()
        self.running = True

    def cmdloop(self):
        while self.running:
            self.cmdwin.addstr('marvin$ ')
            text = self.cmdwin.getstr()
            self.msg('Command: ' + text)
            self.onecmd(text)

    def default(self, line):
        self.query('Unknown command: ' + str(line))

    def do_quit(self, line=None):
        '''
        Quits the program
        '''
        self.msg(u'\nDisconnecting and exitting...')
        curses.endwin()
        sys.exit(0)

    def help_quit(self):
        self.query(u'Quit the application')

    def help_help(self):
        self.query(u'Get help about a topic')

    def setup_screens(self, *args):
        if args:
            curses.endwin()
        self.screen = curses.initscr()
        self.screen.clear()
        self.maxy, self.maxx = self.screen.getmaxyx()

        # Left screen
        self.left = self.screen.subwin(self.maxy, self.maxx / 2, 0, 0)
        self.left.box()
        self.left.addstr(0, 3, 'Commands')
        innery, innerx = tuple(x + 1 for x in self.left.getbegyx())
        rows, cols = self.left.getmaxyx()
        innerrows = innery + rows - 3
        innercols = innerx + cols - 3
        self.cmdwin = self.left.subwin(innerrows, innercols, innery, innerx)
        self.cmdwin.leaveok(True)
        self.cmdwin.idlok(True)
        self.cmdwin.scrollok(True)

        # Right screen
        self.right = self.screen.subwin(self.maxy, self.maxx / 2, 0,
                self.maxx / 2)
        self.right.box()
        self.right.addstr(0, 3, 'Log')
        self.padmaxy, self.padmaxx = self.right.getmaxyx()
        self.rightpad = curses.newpad(1000, self.padmaxx)
        self.rightscroll = 0
        self.screen.refresh()
        self.msg((innery, innerx, rows, cols, innerrows, innercols))
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

if __name__ == '__main__':
    m = MarvinTUI()
    try:
        m.cmdloop()
    finally:
        curses.endwin()
        print u'Everything cleaned up!'
