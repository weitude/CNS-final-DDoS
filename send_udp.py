import socket
import random
from argparse import ArgumentParser, Namespace

def randbytes(n: int) -> bytes:
    random_bytes = bytes(
        [random.getrandbits(8) for _ in range(0, n)]
    )
    return random_bytes

def send_udp(host: str, port: int, length: int):
    print(f"Target: {host}:{port}\t Data Size: {length}")
    data = randbytes(length)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(data, (host, port))
    s.close()

    return

def main(args):
    send_udp(args.target, args.port, args.length)
    
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
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    main(args)
