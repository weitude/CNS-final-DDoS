#!/usr/bin/env python

"""
Test Case 8 Script.
"""

import sys
import random

from mininet.net import Mininet
from mininet.log import lg

from os import path
from argparse import ArgumentParser, Namespace

from topology import DumbbellTopo
from utils.utils import measure_latency

flush = sys.stdout.flush

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
    tar1 = net.hosts[size].IP()
    tar2 = net.hosts[-1].IP()
    res = input("*** Start sending UDP packets? [y/n]: ")

    if res.upper() == "Y":
        random.shuffle(bots)
        for host in bots:
            if int(host.IP().split(".")[-1]) <= 5:
                tar = tar1
            else:
                tar = tar2
            print(f"host: {host.IP()} target: {tar}")
            host.popen(f"python {file} -t {tar} -d {pdelay[host.name]['avg']}")

    input("*** Press enter after capturing traffic [Enter]: ")
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
