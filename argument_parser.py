import argparse

OUTPUT_VERBOSITY_LEVEL = False


def argument_parser():
    global OUTPUT_VERBOSITY_LEVEL
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--files",
        type=str,
        default="",
        nargs='+',
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
        "-v",
        "--verbose",
        action="store_true",
        required=False,
        help="Enable verbose output"
    )

    return parser.parse_known_args()


args = argument_parser()[0]
if args.verbose:
    OUTPUT_VERBOSITY_LEVEL = True