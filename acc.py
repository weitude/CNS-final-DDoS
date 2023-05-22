import csv

INF = 1 << 64
filename = "./data/7.csv"


packet_set = []
with open(filename) as csvfile:
    rows = csv.reader(csvfile)
    for i in rows:
        packet_set.append(i)

packet_set.sort(key=lambda packet_set:packet_set[1])
packet_set = packet_set[:-1]

"""
cluster : [src_min, src_max, dst_min, dst_max]
"""
src_min_idx = 0
src_max_idx = 1
dst_min_idx = 2
dst_max_idx = 3

cluster_set = [["10.0.0.2", "10.0.0.2", "10.0.0.2", "10.0.0.2"],
           ["10.0.0.4", "10.0.0.4", "10.0.0.4", "10.0.0.4"],
           ["10.0.0.6", "10.0.0.6", "10.0.0.6", "10.0.0.6"],
           ["10.0.0.8", "10.0.0.8", "10.0.0.8", "10.0.0.8"]]

def ip_dis(a, b):
    a = a.split('.')
    b = b.split('.')

    return abs(int(a[3]) - int(b[3]))

def ip_compare(a, b):
    a = a.split('.')
    b = b.split('.')
    for i in range(4):
        if int(a[i]) > int(b[i]):
            return True

    return False


def compute_distance(packet, cluster):
    dis = 0
    for idx, feature in enumerate(packet):
        feature_dis = 0
        if idx == 2 or idx == 3: #source ip or destination ip
            if ip_compare(cluster[src_min_idx], feature):
                feature_dis = ip_dis(cluster[src_min_idx], feature)    
            if ip_compare(feature, cluster[src_max_idx]):
                feature_dis = ip_dis(feature, cluster[src_max_idx])

            dis += feature_dis
        else:
            """ seems no use """
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


for packet in packet_set:
    selected_cluster = -1
    dis_min = INF
    for idx, cluster in enumerate(cluster_set):
        dis = compute_distance(packet, cluster)
        if dis < dis_min:
            dis_min = dis
            selected_cluster = cluster
    if dis_min > 0:
        update_cluster(packet, selected_cluster)
    print(cluster_set)
