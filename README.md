# CNS fianl

## Generate UDP traffic

Randomly choose 3 hosts in the botnet to send UDP packets to benign hosts.

```bash
sudo python topo/simple_send.py -f send_udp.py
```

Start Wireshark to capture UDP packets:

```bash
sudo -E wireshark &
```

- Choose `s1-eth1` interface

```bash
# Type y/Y to start sending UDP packets
*** Start sending UDP packets? [y/n]: y
Host: 10.0.0.7 Target: 10.0.0.18
Host: 10.0.0.2 Target: 10.0.0.16
Host: 10.0.0.10 Target: 10.0.0.18
```

Sample captured `pcapng` file is at `test-data`

