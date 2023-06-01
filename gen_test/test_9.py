#!/usr/bin/env python3

"""
Test Case 9 Script.
 - consider background traffic
 - default behavior
    - h<1..7>  -> h<rand(11..20)>   pulse-wave traffic
    - h<8..10> -> h<rand(11..20)>   benign traffic
"""

import os
import sys
import random
import pickle
import tempfile

from mininet.net import Mininet
from mininet.log import lg

from os import path
from argparse import ArgumentParser, Namespace

from topology import DumbbellTopo
from utils.utils import restricted_float

flush = sys.stdout.flush


def run(size, botnet_size, rounds, mscript, bscript):
    """
    Send UDP packets to random targets.
    """
    topo = DumbbellTopo(size)
    net = Mininet( topo=topo, waitConnected=True )
    net.start()
    # bots = net.hosts[:botnet_size]
    bots = random.sample(net.hosts[:size], botnet_size)
    # nors = net.hosts[botnet_size:size]
    nors = [x for x in net.hosts[:size] if x not in bots]
    tars = [host.IP() for host in net.hosts[size:]]
    order = []

    print(f"botnet hosts: [{', '.join([x.IP() for x in bots])}]")
    print(f"benign hosts: [{', '.join([x.IP() for x in nors])}]")

    for _ in range(rounds):
        order.append(random.sample(tars, botnet_size))

    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        pickle.dump(order, open(tmp.name, "wb"))
        res = input("*** Start sending UDP packets? [y/n]: ")
        if res.upper() == "Y":
            dest = ",".join(tars)
            for host in nors:
                host.popen(f"python3 {bscript} -d {dest}")
            for i, host in enumerate(bots):
                host.popen(f"python3 {mscript} -f {tmp.name} -s {i}")
    finally:
        tmp.close()
        input("*** Press enter after capturing traffic [Enter]: ")
        os.unlink(tmp.name)

    net.stop()

def main(args):
    lg.setLogLevel("info")
    botnet_size = int(args.size * args.botnet_frac)
    run(args.size, botnet_size, args.rounds,
        args.malicious_script, args.benign_scirpt)

    return

def sanity_check(args):
    for file in [args.malicious_script, args.benign_scirpt]:
        if not path.isfile(file):
            print(f"Error: {file} is not a file")
            exit(1)
        extension = file.split(".")[-1]
        if extension != "py":
            print(f"Error: {file} is not a Python script")
            exit(1)

    return

def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-m", "--malicious_script",
        type=str,
        required=True,
        help="Python script executed by hosts in botnet"
    )
    parser.add_argument(
        "-b", "--benign_scirpt",
        type=str,
        required=True,
        help="Python script executed by benign hosts"
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
    parser.add_argument(
        "--botnet_frac",
        type=restricted_float,
        default=0.7,
        help="Number of botnet hosts in net"
    )
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_args()
    sanity_check(args)
    main(args)
