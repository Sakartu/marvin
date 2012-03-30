import simplejson
import urllib2
import urllib
import constants
from infinite_timer import InfiniteTimer
from operator import attrgetter
import tempfile
import time


class IssuePoller():
    def __init__(self, conf, bot, username, project):
        self.conf = conf
        self.bot = bot
        self.username = username
        self.project = project
        self.timer = InfiniteTimer(int(self.conf.polltime), self.poll, immediate=True)
        self.old = tempfile.NamedTemporaryFile(delete=True)
        self.new = tempfile.NamedTemporaryFile(delete=True)
        self.poll(broadcast=False)

    def start(self):
        self.timer.start()

    def poll(self, broadcast=True):
        '''
        This method will check to see if there are new events for all the issues
        for the given project and notify users if there are
        '''
        url = constants.URL_ISSUE_EVENTS.format(
                user=self.username,
                project=self.project)
        try:
            resp = urllib2.urlopen(url)
            newevents = simplejson.loads(resp.read())
            olddata = self.old.read()
            oldevents = simplejson.load(olddata) if olddata else []
            oldids = map(attrgetter('id'), oldevents) if oldevents else []
            results = []
            for e in newevents:
                if e['id'] not in oldids and e['event'] == 'closed':
                    result = '{name} closed {proj} issue {num} ({url}) "{title}"!'.format(
                    proj=self.project,
                    name=e['actor']['login'], 
                    num=e['issue']['number'], 
                    url=self.shorten(e['issue']['html_url']), 
                    title=e['issue']['title'])
                    results.append(result)

            simplejson.dump(newevents, self.old)
            if not broadcast:
                return
            print 'Broadcasting...'
            for r in results: 
                self.bot.broadcast(r)
                # take 1 second sleep, to make sure we don't overflow the server
                time.sleep(1)
        except:
            print u'Could not retrieve issues!'

    def cancel(self):
        self.timer.cancel()
        self.old.close()
        self.new.close()

    def shorten(self, url):
        try:
            req = urllib2.Request(constants.URL_SHORTEN,
                    urllib.urlencode({'url' : url}))
            return urllib2.urlopen(req).headers.get('Location')
        except:
            return url


