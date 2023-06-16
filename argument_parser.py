import argparse


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--anomaly_pcap",
        type=str,
        default="",
        required=True
    )
    parser.add_argument(
        "-n",
        "--normal_pcap",
        type=str,
        default="",
        required=True
    )
    parser.add_argument(
        "-i",
        "--input_pcap",
        type=str,
        default="",
        required=True
    )

    return parser.parse_known_args()
