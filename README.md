# CNS Final

## docker-mininet

### Docker Build Command

```bash
cd docker-mininet
docker build -t mininet .
```

### Docker Run Command

```bash
docker run -it --rm --privileged -e DISPLAY \
           -P -v /lib/modules:/lib/modules \
           mininet
```

## Generate UDP traffic

### Random Choose 3 Hosts

Randomly choose 3 hosts in the botnet to send UDP packets to benign hosts.

```bash
sudo python topo/simple_send.py -f send_udp/send_udp.py
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

Sample captured `pcapng` file is at `test_data`

### Case 1 & 4: Target Same Host

All botnet hosts send UDP packets to `10.0.0.11`.

#### Case 1

```bash
sudo python gen_test/test_1.py -f gen_test/utils/pulse_udp.py
```

#### Case 4

```bash
sudo python gen_test/test_4.py -f gen_test/utils/pulse_udp.py
```

### Test Case 7: Random Select Target

> This version generates UDP stream w/o background traffic.

All botnet hosts randomly select target host.

```bash
sudo python gen_test/test_7.py -f gen_test/utils/send_7.py
```

### Test Case 8: Random Select Target w/ Background Traffic

A fraction of hosts acting as a botnet randomly select targets and other hosts as benign hosts sending background traffic.

```bash
sudo python gen_test/test_8.py -m gen_test/utils/send_7.py \
  -b gen_test/utils/benign_udp.py
```

