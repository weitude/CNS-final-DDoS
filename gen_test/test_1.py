#!/usr/bin/env python3

"""
Test Case 1 Script.
"""

import sys
import random

from mininet.net import Mininet
from mininet.log import lg
# from mininet.cli import CLI

from os import path
from argparse import ArgumentParser, Namespace

from topology import DumbbellTopo
# from utils.utils import measure_latency

flush = sys.stdout.flush

def run(size, file):
    """
    Send UDP packets to random targets.
    """
    topo = DumbbellTopo(size)
    net = Mininet( topo=topo, waitConnected=True )
    net.start()
    # print("*** Measuring link latency ...")
    # pdelay = measure_latency(net)
    bots = net.hosts[:size]
    tar = net.hosts[size]
    res = input("*** Start sending UDP packets? [y/n]: ")

    if res.upper() == "Y":
        random.shuffle(bots)
        print("[", end="")
        for host in bots:
            print(f"{host.IP()},", end="")
            # host.popen(f"python3 {file} -t {tar.IP()} -d {pdelay[host.name]['avg']}")
            host.popen(f"python3 {file} -t {tar.IP()}")
        print("]")

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
    run(args.size, args.file)

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
