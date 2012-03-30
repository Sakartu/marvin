#!/usr/bin/env python

from twisted.internet import reactor
import config
from bot import MarvinFactory

if __name__ == '__main__':
    args = config.parse_options()
    conf = config.parse_config(args)
    factory = MarvinFactory(conf)
    reactor.connectTCP(conf.server, conf.port, factory)
    reactor.run()
