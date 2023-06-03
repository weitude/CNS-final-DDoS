import socket
import random
from time import time, sleep
from argparse import ArgumentParser, Namespace

def randbytes(n: int) -> bytes:
    random_bytes = bytes(
        [random.getrandbits(8) for _ in range(0, n)]
    )
    return random_bytes

def run(dest, port, length, period):
    total = 0
    start = time()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time() - start < period:
        data = randbytes(int(length * random.random()))
        ip = random.choice(dest)
        s.sendto(data, (ip, port))
        total += 1
        sleep(random.uniform(0.002, 0.005))
    s.close()
    print(f"Sending {total} packets to destination [{' ,'.join(dest)}]")
    
    return

def main(args):
    dest = args.dest.split(',')
    run(dest, args.port, args.length, args.period)
    return

def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-d", "--dest",
        type=str,
        required=True,
        help="The destination host IP addresses"
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=28866,
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
        default=20,
        help="The length of time to send packets"
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    main(args)
