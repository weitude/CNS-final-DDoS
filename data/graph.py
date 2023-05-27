import csv
import matplotlib.pyplot as plt

filename = "./7.csv"

packet_set = []
with open(filename) as csvfile:
    rows = csv.reader(csvfile)
    for i in rows:
        packet_set.append(i)

packet_set = packet_set[1:]
packet_set.sort(key=lambda packet_set:float(packet_set[1]))

interval = 0.1
timestamp = [0]
number = [0]
current_time = interval
counter = 0
for i in packet_set:
    if float(i[1]) <= current_time:
        counter += 1
    else:
        number.append(counter)
        timestamp.append(current_time)
        counter = 0
        current_time += interval

plt.plot(timestamp, number)
plt.savefig("7.jpg")
