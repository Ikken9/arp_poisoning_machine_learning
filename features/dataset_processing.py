from scapy.all import *
from scapy.layers.l2 import ARP
import tensorflow as tf
from sklearn.model_selection import train_test_split


def read_pcap(filepath):
    data = []
    packets = PcapReader(filepath)
    arp_packets = [pkt for pkt in packets if pkt.haslayer(ARP)]

    for pkt in arp_packets:
        # Access ARP packet fields
        arp = pkt.getlayer(ARP)
        source_mac = arp.hwsrc
        source_ip = arp.psrc
        target_mac = arp.hwdst
        target_ip = arp.pdst

        print(f"Source MAC: {source_mac}\t Source IP: {source_ip}\t Target MAC: {target_mac}\t Target IP: {target_ip}")
        data.append([source_ip, source_mac, target_ip, target_mac])

    return data


def create_tensors(data, labels):
    # Convert data and labels to TensorFlow tensors
    features_tensor = tf.convert_to_tensor(data)
    labels_tensor = tf.convert_to_tensor(labels)

    return features_tensor, labels_tensor


def split_dataset(features_tensor, labels_tensor):
    x_train, y_train, x_test, y_test = train_test_split(features_tensor, labels_tensor, test_size=0.2, random_state=42)
    return x_train, y_train, x_test, y_test