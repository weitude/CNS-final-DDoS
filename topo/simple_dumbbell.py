#!/usr/bin/env python

"""
Simple dumbell topology.
"""

import sys

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import lg
from mininet.util import irange
from mininet.cli import CLI

flush = sys.stdout.flush


class DumbbellTopo( Topo ):
    """
    Topology for a string of 2N hosts and 2 switches.

      h1               h4
         \           /
      h2 - s1 --- s2 - h5
         /           \ 
      h3               h6

    """

    def build( self, N, **params ):
        # Create switches and hosts
        hosts = [ self.addHost( "h%s" % h ) for h in irange( 1, 2*N ) ]
        switches = [ self.addSwitch( "s%s" % s ) 
                     for s in irange( 1, 2 ) ]

        # Wire up switches
        self.addLink(switches[0], switches[1])

        # Wire up hosts
        for i, switch in enumerate(switches):
            for j in range(N):
                self.addLink(hosts[i*N+j], switch)


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