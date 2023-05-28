
"""
Utils functions.
"""

import argparse
from mininet.util import pmonitor

def measure_latency(net, ip: str = "127.0.0.1") -> dict:
    """
    Measure hosts latency to specified IP address.
    """
    pdata = {}
    popens = {}
    for host in net.hosts:
        popens[host] = host.popen(f"ping -c5 {ip}")
        pdata[host.name] = []
    for host, line in pmonitor(popens):
        if host:
            pdata[host.name].append(line)
    pdelay = {}
    for host, events in pdata.items():
        pdelay[host] = {}
        tmp = events[-1].split()
        for k, v in zip(tmp[1].split('/'), tmp[3].split('/')):
            pdelay[host][k] = v
    
    return pdelay

def restricted_float(x):
    """
    Reference:
        https://stackoverflow.com/questions/12116685/how-can-i-require-my-python-scripts-argument-to-be-a-float-in-a-range-using-arg
    """
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError("%r not a floating-point literal" % (x,))

    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x
