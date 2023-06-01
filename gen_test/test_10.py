#!/usr/bin/env python3

"""
Test Case 10 Script
"""

import os
import pickle
import random
import sys
import tempfile
from argparse import ArgumentParser, Namespace
from os import path
from time import time, sleep

from mininet.cli import CLI
from mininet.log import lg
from mininet.net import Mininet

from topology import DumbbellTopo

flush = sys.stdout.flush


def run(size, rounds, file):
    """
    Send UDP packets to random targets.
    """
    topo = DumbbellTopo(size)
    net = Mininet(topo=topo, waitConnected=True)
    net.start()
    # print("*** Measuring link latency ...")
    # pdelay = measure_latency(net)
    bots = net.hosts[:size]
    tars = [host.IP() for host in net.hosts[size:]]
    order = []

    for _ in range(rounds):
        random.shuffle(tars)
        order.append(tars.copy())

    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        print(f"*** file: {tmp.name}")
        pickle.dump(order, open(tmp.name, "wb"))
        res = input("*** Start sending UDP packets? [y/n]: ")
        if res.upper() == "Y":
            for round in range(5):
                start = time()
                random.shuffle(bots)
                print(f"### Round {round + 1}")
                for i, host in enumerate(bots[:7]):
                    print(host)
                    host.popen(f"python3 {file} -f {tmp.name} -s {i}")
                sleep(4 - time() + start)
    finally:
        tmp.close()
        CLI(net)
        os.unlink(tmp.name)

    net.stop()


def main(args):
    lg.setLogLevel("info")
    # Start sanity check
    if not path.isfile(args.file):
        print(f"Error: {args.file} is not a file")
        exit(1)
    extension = args.file.split(".")[-1]
    if extension != "py":
        print(f"Error: {args.file} is not a Python script")
        exit(1)
    # End sanity check
    run(args.size, args.rounds, args.file)

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
    parser.add_argument(
        "-r", "--rounds",
        type=int,
        default=5000,
        help="Number of attacking rounds"
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    main(args)
