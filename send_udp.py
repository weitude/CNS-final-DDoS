import socket

HOST, PORT = "10.0.0.20", 9999
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'Hello, world', (HOST, PORT))
s.close()
