#!/usr/bin/env python3

"""
Define needed topologies.
"""

from mininet.topo import Topo
from mininet.util import irange

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
