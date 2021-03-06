import simplejson
import urllib2
import urllib
import constants
import random
from infinite_timer import InfiniteTimer
from operator import itemgetter
import time


class IssuePoller():
    def __init__(self, conf, bot, username, project):
        self.conf = conf
        self.bot = bot
        self.username = username
        self.project = project
        self.timer = InfiniteTimer(int(self.conf.polltime), self.poll,
                immediate=True)
        self.oldevents = []
        self.newevents = []
        self.poll(broadcast=False)

    def start(self):
        self.timer.start()

    def poll(self, broadcast=True):
        '''
        This method will check to see if there are new events for all the
        issues for the given project and notify users if there are
        '''
        url = constants.URL_ISSUE_EVENTS.format(
                user=self.username,
                project=self.project)
        try:
            resp = urllib2.urlopen(url)
            self.newevents = simplejson.loads(resp.read())
            if self.oldevents:
                oldids = map(itemgetter('id'), self.oldevents)
            else:
                oldids = []
            results = []
            for e in self.newevents:
                if 'id' in e and e['id'] not in oldids:
                    if e['type'] != 'IssuesEvent':
                        continue
                    action = e['payload']['action']
                    if action in ['closed', 'opened', 'reopened']:
                        result = ('{name} {action} {proj} issue {num} ({url}) '
                        '"{title}"!').format(
                        proj=self.project,
                        name=e['actor']['login'],
                        action=e['payload']['action'],
                        num=e['payload']['issue']['number'],
                        url=self.shorten(e['payload']['issue']['html_url']),
                        title=e['payload']['issue']['title'])
                        results.append(result)
                    # Make him answer to his own events
                    if action in self.bot.handler.sneer:
                        remark = self.bot.handler.sneer[action][random.randint(
                            1, len(self.bot.handler.sneer[action]) - 1)]
                        results.append(remark)
            self.oldevents = self.newevents
            if not broadcast or not results:
                return
            self.bot.tui.msg('\nBroadcasting...')
            self.bot.tui.msg(self.bot.tui.prompt)
            for r in results:
                self.bot.broadcast(r)
                # take 1 second sleep, to make sure we don't overflow the
                # server
                time.sleep(1)
        except Exception, e:
            self.bot.tui.msg(u'Could not retrieve issues: ')
            self.bot.tui.msg(e)
            self.bot.tui.msg(self.bot.tui.prompt)

    def cancel(self):
        self.timer.cancel()

    def shorten(self, url):
        try:
            req = urllib2.Request(constants.URL_SHORTEN,
                    urllib.urlencode({'url': url}))
            return urllib2.urlopen(req).headers.get('Location')
        except:
            return url
