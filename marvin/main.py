#!/usr/bin/env python

from twisted.internet import reactor
import config
from bot import MarvinFactory

if __name__ == '__main__':
    args = config.parse_options()
    reactor.connectTCP(args.server, args.port, 
            MarvinFactory(args.channel, args.nick))
    reactor.run()
