#!/usr/bin/env python

"""
Simple dumbbell topology.
"""

import sys

from mininet.net import Mininet
from mininet.log import lg
from mininet.cli import CLI

from topology import DumbbellTopo

flush = sys.stdout.flush

def run(count):

    "Check bandwidth at various lengths along a switch chain."

    topo = DumbbellTopo(count)
    net = Mininet( topo=topo, waitConnected=True )
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    lg.setLogLevel( 'info' )
    size = 10
    run( size )