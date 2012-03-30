import argparse
import constants

def parse_options():
    parser = argparse.ArgumentParser(description=constants.DESCRIPTION)
    parser.add_argument('-c', '--chan', dest='channel', required=True,
            help='The channel to join. Does not have to have a leading #.')
    parser.add_argument('-s', '--server', dest='server', required=True,
            help='The server to connect to.')
    parser.add_argument('-p', '--port', dest='port', default=6667, type=int,
            help='The port to connect to. Optional, default is 6667.')
    parser.add_argument('-n', '--nick', dest='nick', default='marvinbot',
            help='The nickname the bot should have. Default is "marvin"')
    args = parser.parse_args()
    return args
