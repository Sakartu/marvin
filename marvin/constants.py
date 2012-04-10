import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))

DESCRIPTION = u'''A depressed IRC bot.'''

EIGHTBALL = open(os.path.join(BASE, '../resources/eightball')).readlines()

ANSWERS = open(os.path.join(BASE, '../resources/answers')).readlines()

SNEER = {}
for f in glob.glob(os.path.abspath(os.path.join(BASE, '../resources/sneer_*'))):
    data = open(f).readlines()
    SNEER[os.path.basename(f)[6:]] = data

URL_ISSUE_EVENTS = 'https://api.github.com/repos/{user}/{project}/events'
URL_SHORTEN = 'http://git.io'
