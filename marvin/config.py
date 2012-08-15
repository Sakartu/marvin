import pprint
import argparse
import constants
from ConfigParser import SafeConfigParser


def parse_options():
    parser = argparse.ArgumentParser(description=constants.DESCRIPTION)
    parser.add_argument('-c', '--chan', dest='channel',
            help='Comma separated list of channels to join. Does not have to '
            'have a leading #.')
    parser.add_argument('-s', '--server', dest='server',
            help='The server to connect to.')
    parser.add_argument('-p', '--port', dest='port', default=6667, type=int,
            help='The port to connect to. Optional, default is 6667.')
    parser.add_argument('-n', '--nickname', dest='nickname',
            default='marvinbot', help='The nickname the bot should have. '
            'Default is "marvin"')
    parser.add_argument('--config', dest='configpath', default='marvin.conf',
            help='The location of the configuration file. Optional, default '
            'is marvin.conf')
    args = parser.parse_args()
    return args


def parse_config(args):
    confpath = args.configpath
    parser = SafeConfigParser()
    parser.read(confpath)

    conf = Config()

    def parse_value(conf, parser, args, section, key):
        '''
        Parse a value from the config file
        '''
        result = None
        if key in dir(args) and getattr(args, key):
            result = getattr(args, key)
        elif parser.has_option(section, key):
            result = parser.get(section, key)
        else:
            result = ''
        setattr(conf, key, result)
        return conf

    def parse_csvalue(conf, parser, args, section, key):
        '''
        Parse a comma separated value
        '''
        conf = parse_value(conf, parser, args, section, key)
        setattr(conf, key, tuple(getattr(conf, key).split(',')))
        return conf

    def parse_csssvalue(conf, parser, args, section, key):
        '''
        Parse a comma, then slash separated value
        '''
        conf = parse_csvalue(conf, parser, args, section, key)
        vs = getattr(conf, key)
        setattr(conf, key, tuple(tuple(x.split('/')) for x in vs))
        return conf

    # Parse configuration options
    for k in ('server', 'port', 'nickname', 'realname'):
        conf = parse_value(conf, parser, args, 'general', k)

    for k in ('channels',):
        conf = parse_csvalue(conf, parser, args, 'general', k)

    for k in ('polltime',):
        conf = parse_value(conf, parser, args, 'github', k)

    for k in ('commits', 'issues'):
        conf = parse_csssvalue(conf, parser, args, 'github', k)

    normalised = []
    for c in conf.channels:
        normalised.append('#' + c[0] if not c[0].startswith('#') else c)
    conf.channels = normalised

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
        result = (self.nickname + '@' + self.server + ':' + str(self.port)
                + '\n')
        result += 'Channels: ' + pprint.pformat(self.channels)
        result += '\nIssues: ' + pprint.pformat(self.issues)
        result += '\nCommits: ' + pprint.pformat(self.commits)
        return result

    def __str__(self):
        return repr(self)
