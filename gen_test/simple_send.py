#!/usr/bin/env python

"""
Toy example.
"""

import sys
import random

from mininet.net import Mininet
from mininet.log import lg
from mininet.cli import CLI

from os import path
from topology import DumbbellTopo
from argparse import ArgumentParser, Namespace

flush = sys.stdout.flush

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
