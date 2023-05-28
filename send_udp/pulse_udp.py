import socket
import random
from time import time, sleep
from argparse import ArgumentParser, Namespace

def randbytes(n: int) -> bytes:
    random_bytes = bytes(
        [random.getrandbits(8) for _ in range(0, n)]
    )
    return random_bytes

def main(args):
    total = 0
    data = randbytes(args.length)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    duration = args.period / 2 - args.delay
    for _ in range(args.cycle):
        start = time()
        while time() - start < duration:
            # Total 50 thousands packet for all hosts
            s.sendto(data, (args.target, args.port))
            total += 1
            sleep(random.uniform(0.001, 0.003))
        sleep(args.period - time() + start)
    s.close()
    print(f"Sending {total} packets to {args.target}")
    
    return

def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-t", "--target",
        type=str,
        required=True,
        help="Destination host IP address"
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
