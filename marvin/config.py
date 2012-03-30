import pprint
import argparse
import constants
from ConfigParser import SafeConfigParser

def parse_options():
    parser = argparse.ArgumentParser(description=constants.DESCRIPTION)
    parser.add_argument('-c', '--chan', dest='channel', 
            help='Comma separated list of channels to join. Does not have to have a leading #.')
    parser.add_argument('-s', '--server', dest='server',
            help='The server to connect to.')
    parser.add_argument('-p', '--port', dest='port', default=6667, type=int,
            help='The port to connect to. Optional, default is 6667.')
    parser.add_argument('-n', '--nickname', dest='nickname', default='marvinbot',
            help='The nickname the bot should have. Default is "marvin"')
    parser.add_argument('--config', dest='configpath', default='marvin.conf',
            help='The location of the configuration file. Optional, default is marvin.conf')
    args = parser.parse_args()
    return args

def parse_config(args):
    confpath = args.configpath
    parser = SafeConfigParser()
    parser.read(confpath)

    conf = Config()

    def parse_value(conf, parser, args, section, value):
        result = None
        if value in dir(args) and getattr(args, value):
            result = getattr(args, value)
        else:
            result = parser.get(section, value)
        setattr(conf, value, result)
        return conf

    def parse_csvalue(conf, parser, args, section, value):
        result = []
        if value in dir(args) and getattr(args, value):
            result = map(lambda x : tuple(x.split('/')), 
                    getattr(args, value).split(','))
        else:
            result = map(lambda x : tuple(x.split('/')), 
                    parser.get(section, value).split(','))
        setattr(conf, value, result)
        return conf

    # Parse lists
    conf = parse_value(conf, parser, args, 'general', 'server')
    conf = parse_value(conf, parser, args, 'general', 'port')
    conf = parse_value(conf, parser, args, 'general', 'nickname')
    conf = parse_csvalue(conf, parser, args, 'general', 'channels')
    normalised = []
    for c in conf.channels:
        normalised.append('#' + c[0] if not c[0].startswith('#') else c)
    conf.channels = normalised

    conf = parse_value(conf, parser, args, 'github', 'polltime')
    conf = parse_csvalue(conf, parser, args, 'github', 'commits')
    conf = parse_csvalue(conf, parser, args, 'github', 'issues')
    return conf

class Config(object):
    def __init__(self):
        self.server = ''
        self.port = ''
        self.nickname = ''
        self.channels = []
        self.issues = []
        self.commits = []

    def __repr__(self):
        result = self.nickname + '@' + self.server + ':' + str(self.port) + '\n'
        result += 'Channels: ' + pprint.pformat(self.channels)
        result += '\nIssues: ' + pprint.pformat(self.issues)
        result += '\nCommits: ' + pprint.pformat(self.commits)
        return result
        

