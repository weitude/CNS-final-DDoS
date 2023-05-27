#!/usr/bin/env python

"""
Simple dumbbell topology.
"""

import sys
import random

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import lg
from mininet.util import irange, pmonitor
from mininet.cli import CLI

from os import path
from argparse import ArgumentParser, Namespace

flush = sys.stdout.flush


class DumbbellTopo( Topo ):

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

def measure_latency(net) -> dict:
    popens = {}
    pdata = {}
    for host in net.hosts:
        popens[host] = host.popen( "ping -c5 %s" % "127.0.0.1" )
        pdata[host.name] = []
    for host, line in pmonitor( popens ):
        if host:
            pdata[host.name].append(line)
    pdelay = {}
    for k, v in pdata.items():
        pdelay[k] = {}
        tmp = v[-1].split()
        for kk, vv in zip(tmp[1].split('/'), tmp[3].split('/')):
            pdelay[k][kk] = vv
    
    return pdelay

def run(size, num, file):
    """
    Send UDP packets to random targets.
    """
    topo = DumbbellTopo(size)
    net = Mininet( topo=topo, waitConnected=True )
    net.start()
    print("*** Measuring link latency ...")
    pdelay = measure_latency(net)
    bots = net.hosts[:size]
    tar = net.hosts[size]
    res = input("*** Start sending UDP packets? [y/n]: ")

    if res.upper() == "Y":
        for host in bots:
            host.popen(f"python {file} -t {tar.IP()} -d {pdelay[host.name]['avg']}")

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
