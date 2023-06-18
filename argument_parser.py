import argparse

OUTPUT_VERBOSITY_LEVEL_DEBUG = False


def argument_parser():
    global OUTPUT_VERBOSITY_LEVEL_DEBUG
    parser = argparse.ArgumentParser()
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
    parser.add_argument(
        "-a",
        "--anomaly_pcap",
        type=str,
        default="",
        required=True
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=str,
        default='0',
        required=False,
        choices=['0', '1']
    )

    return parser.parse_known_args()


args = argument_parser()[0]
if args.verbosity:
    OUTPUT_VERBOSITY_LEVEL_DEBUG = True