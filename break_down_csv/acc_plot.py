import csv
import pandas as pd
import os
import matplotlib.pyplot as plt

INF = 1 << 64

testcase = "9-1"
os.system(f"mkdir {testcase}")
result = []
for part in range(4):
    print(part)
    filename = f"./break_down_data/break_down_{testcase}_{part}.csv"

    packet_set = []
    with open(filename) as csvfile:
        rows = csv.reader(csvfile)
        for i in rows:
            if len(i) == 1:
                continue
            packet_set.append(i)

    if len(packet_set) == 0:
        continue

    packet_set = packet_set[1:]
    packet_set.sort(key=lambda packet_set:float(packet_set[1]))
    #rate = float(packet_set[-1][1]) / len(packet_set)
    rate = 4 / len(packet_set)

    """
    cluster : [src_min, src_max, dst_min, dst_max]
    """
    src_min_idx = 0
    src_max_idx = 1
    dst_min_idx = 2
    dst_max_idx = 3

    cluster_set = [["10.0.0.3", "10.0.0.3", "10.0.0.13", "10.0.0.13"],
                   ["10.0.0.3", "10.0.0.3", "10.0.0.17", "10.0.0.17"],
                   ["10.0.0.7", "10.0.0.7", "10.0.0.13", "10.0.0.13"],
                   ["10.0.0.7", "10.0.0.7", "10.0.0.17", "10.0.0.17"]]

    def ip_dis(a, b):
        a = a.split('.')
        b = b.split('.')

        return abs(int(a[3]) - int(b[3]))

    def ip_compare(a, b):
        a = a.split('.')
        b = b.split('.')
        if int(a[3]) >= int(b[3]):
            return True

        return False


    def compute_distance(packet, cluster):
        dis = 0
        for idx, feature in enumerate(packet):
            feature_dis = 0
            if idx == 2 : #source ip or destination ip
                if ip_compare(cluster[src_min_idx], feature):
                    feature_dis += ip_dis(cluster[src_min_idx], feature)    
                if ip_compare(feature, cluster[src_max_idx]):
                    feature_dis += ip_dis(feature, cluster[src_max_idx])
            elif idx == 3:
                if ip_compare(cluster[dst_min_idx], feature):
                    feature_dis += ip_dis(cluster[dst_min_idx], feature)    
                if ip_compare(feature, cluster[dst_max_idx]):
                    feature_dis += ip_dis(feature, cluster[dst_max_idx])
            else:
                """ seems no use """
            dis += feature_dis
        return dis

    def update_cluster(packet, cluster):
        for idx, feature in enumerate(packet):
            if idx == 2: #source ip
                if ip_compare(cluster[src_min_idx], feature):
                    cluster[src_min_idx] = feature
                if ip_compare(feature, cluster[src_max_idx]):
                    cluster[src_max_idx] = feature
            elif idx == 3: #destination ip
                if ip_compare(cluster[dst_min_idx], feature):
                    cluster[dst_min_idx] = feature
                if ip_compare(feature, cluster[dst_max_idx]):
                    cluster[dst_max_idx] = feature
            else:
                """ seems no use """


    packet_queue_set = [[] for i in range(4)]
    for packet in packet_set:
        if packet[4] != "UDP":
            continue
        selected_cluster = -1
        which = -1
        dis_min = INF
        #print(packet)
        for idx, cluster in enumerate(cluster_set):
            dis = compute_distance(packet, cluster)
            #print('idx, dis ',idx, dis)
            #print(cluster)
            if dis < dis_min:
                dis_min = dis
                selected_cluster = cluster
                which = idx
        #print('dis_min',dis_min)
        if dis_min > 0:
            update_cluster(packet, selected_cluster)
        #print(cluster_set)
        
        packet_queue_set[which].append(packet)

    """ draw cluster graph """
    #print(packet_queue_set[2])
    """
    for i in range(4):
        df = pd.DataFrame(packet_queue_set[i])
        df.to_csv(f"cluster{i}.csv")
    """

    cnt = dict()
    for i in range(1,11):
        for j in range(11,21):
            cnt[(i,j)] = [0,-1]

    for i in range(4):
        for one_packet in packet_queue_set[i]:
            s = int(one_packet[2].split('.')[3])
            d = int(one_packet[3].split('.')[3])
            cnt[(s,d)][0] += 1
            #if cnt[(s,d)][1]==-1:
            cnt[(s,d)][1] = i
        #print(cnt)

    src = []
    des = []
    cnt_packet = []
    color_list = ['red', 'yellow', 'green', 'blue']
    colors = []
    for i in range(1,11):
        for j in range(11,21):
            if cnt[(i,j)][0]>0:
                src.append(i)
                des.append(j)
                cnt_packet.append(cnt[(i,j)][0])
                colors.append(color_list[cnt[(i,j)][1]])

    for i in range(len(cnt_packet)):
        cnt_packet[i] *= 20

    plt.figure(figsize=(10, 15), dpi=100)
    plt.scatter(src, des, c=colors, s=cnt_packet, label='packet')
    plt.xticks(range(1, 11, 1))
    plt.yticks(range(11, 21, 1))
    plt.xlabel("source ip", fontdict={'size': 16})
    plt.ylabel("destination ip", fontdict={'size': 16})
    plt.title("Clusters", fontdict={'size': 20})
    plt.savefig(f'./{testcase}/plot_{part}.png')
    plt.cla()
    plt.close()

    """ draw cluster graph """

    
    length = []
    #print("length of each cluster")
    for i in range(4):
        length.append(len(packet_queue_set[i]))
        print(f"{i}:", length[i])

    current_time = part * 4
    print("rate:", rate)
    while True:
        empty = 0
        current_time += rate
        for i in range(4):
            if length[i] > 0:
                out = packet_queue_set[i].pop(0)
                out[1] = str(round(current_time, 6))
                result.append(out[1:])
                length[i] -= 1
            else:
                empty += 1

        if empty == 4:
            break

df = pd.DataFrame(result)
df.to_csv(f"./{testcase}/after_acc_{testcase}.csv")
