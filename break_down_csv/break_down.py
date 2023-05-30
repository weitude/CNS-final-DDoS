import csv
import pandas as pd
import os

packet_set = []
which = "7"
filename = f"../test_data/csv/test_{which}.csv"
with open(filename) as csvfile:
    rows = csv.reader(csvfile)
    for i in rows:
        packet_set.append(i)

packet_set = packet_set[1:]
packet_set.sort(key=lambda packet_set:float(packet_set[1]))

os.system("mkdir break_down_data")

cur_time = 0
counter = 0
while True:
    cur_time += 0.1
    buf = []
    while True:
        if len(packet_set) != 0 and float(packet_set[0][1]) <= cur_time:
            buf.append(packet_set.pop(0)[1:])
        else:
            break

    df = pd.DataFrame(buf)
    df.to_csv(f"./break_down_data/break_down_{which}_{counter}.csv")
    counter += 1

    if len(packet_set) == 0:
        break
