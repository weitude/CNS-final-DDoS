#!/usr/bin/env python

"""
Simple dumbbell topology.
"""

import sys
import random

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import lg
from mininet.util import irange
from mininet.cli import CLI

from os import path
from argparse import ArgumentParser, Namespace

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


def run(size, num, file):
    """
    Send UDP packets to random targets.
    """
    topo = DumbbellTopo(size)
    net = Mininet( topo=topo, waitConnected=True )
    net.start()
    bots = net.hosts[:size]
    tars = net.hosts[size:]
    res = input("*** Start sending UDP packets? [y/n]: ")

    if res.upper() == "Y":
        for host in random.sample(bots, num):
            tar = random.choice(tars)
            print(f"Host: {host.IP()} Target: {tar.IP()}")
            host.popen(f"python {file} -t {tar.IP()}")

    CLI(net)
    net.stop()

def main(args):
    lg.setLogLevel("info")
    # Start sanity check
    if not path.isfile(args.file):
        print(f"Error: {args.file} is not a Python script")
    extension = args.file.split(".")[-1]
    if extension != "py":
        print(f"Error: {args.file} is not a Python script")
    # End sanity check
    run(args.size, args.num, args.file)

    return


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--file",
        type=str,
        required=True,
        help="Python script executed by hosts in botnet"
    )
    parser.add_argument(
        "-n", "--num",
        type=int,
        default=3,
        help="Number of attacking hosts"
    )
    parser.add_argument(
        "-s", "--size",
        type=int,
        default=10,
        help="Size of network topology"
    )
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_args()
    main(args)
