from argument_parser import OUTPUT_VERBOSITY_LEVEL_DEBUG
from scapy.all import *
from scapy.layers.l2 import ARP
import tensorflow as tf
from sklearn.model_selection import train_test_split


def read_pcap(filepath):
    packets = PcapReader(filepath)
    arp_packets = [pkt for pkt in packets if pkt.haslayer(ARP)]
    return arp_packets


def process_arp_pcap(packets):
    data = []
    for pkt in packets:
        # Access ARP packet fields
        arp = pkt.getlayer(ARP)
        source_mac = arp.hwsrc
        source_ip = arp.psrc
        target_mac = arp.hwdst
        target_ip = arp.pdst
        data.append([source_ip, source_mac, target_ip, target_mac])
    return data


def parse_pcap(packets):
    def string_to_float(input_string):
        try:
            parsed_string = ''.join(char for char in input_string if char.isdigit())
            return float(parsed_string)
        except ValueError:
            print("[!] Error parsing data")

    parsed_data = []
    for pkt in packets:
        parsed_pkt = [string_to_float(field) for field in pkt]
        parsed_data.append(parsed_pkt)

    return parsed_data


def create_tensors(data, labels):
    # Convert data and labels to TensorFlow tensors
    features_tensor = tf.convert_to_tensor(data).numpy().astype(float)
    labels_tensor = tf.convert_to_tensor(labels).numpy().astype(float)

    if OUTPUT_VERBOSITY_LEVEL_DEBUG:
        print("\nFEATURES TENSOR PROPERTIES:")
        print(f"Size: {len(features_tensor)}")
        print(f"Shape: {features_tensor.shape}")

        print("\nLABELS TENSOR PROPERTIES:")
        print(f"Size: {len(labels_tensor)}")
        print(f"Shape: {labels_tensor.shape}")

    return features_tensor, labels_tensor


def split_dataset(features_tensor, labels_tensor):
    x_train, x_test, y_train, y_test = train_test_split(features_tensor, labels_tensor, test_size=0.2, random_state=42)
    return x_train, x_test, y_train, y_test
