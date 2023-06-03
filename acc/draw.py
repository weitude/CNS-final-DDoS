import csv
import pandas as pd
import os
import matplotlib.pyplot as plt

attack = [4,1,6,9,3,2,10]
benign = [5,7,8]
#filename = f"../break_down_csv/9-1/after_acc_9-1.csv"
filename = f"./after_acc_9-1.csv"

packet_set = []
with open(filename) as csvfile:
    rows = csv.reader(csvfile)
    for i in rows:
        packet_set.append(i)

attack_packet = []
benign_packet = []
for packet in packet_set[1:]:
    srcIP = int(packet[2].split('.')[3])
    if srcIP in attack:
        attack_packet.append(packet)
    elif srcIP in benign:
        benign_packet.append(packet)

interval = 0.5
attack_timestamp = [0]
attack_number = [0]
current_time = interval
counter = 0
for i in attack_packet:
    if float(i[1]) <= current_time:
        counter += 1
    else:
        attack_number.append(counter)
        attack_timestamp.append(current_time)
        counter = 0
        current_time += interval

benign_timestamp = [0]
benign_number = [0]
current_time = interval
counter = 0
for i in benign_packet:
    if float(i[1]) <= current_time:
        counter += 1
    else:
        benign_number.append(counter)
        benign_timestamp.append(current_time)
        counter = 0
        current_time += interval

total_timestamp = [0]
total_number = [0]
current_time = interval
counter = 0
for i in packet_set:
    if float(i[1]) <= current_time:
        counter += 1
    else:
        total_number.append(counter)
        total_timestamp.append(current_time)
        counter = 0
        current_time += interval

plt.plot(attack_timestamp, attack_number, color='orange', label="attack")
plt.plot(benign_timestamp, benign_number, color='green', label="benign")
plt.plot(total_timestamp, total_number, color='blue', label="total")
plt.xlabel('time', fontsize="10")
plt.ylabel('# of packets', fontsize="10")
plt.title('title', fontsize="18")
plt.savefig(f"after_test_9-1.jpg")