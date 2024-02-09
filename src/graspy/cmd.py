# Run command line interface to execute batch process

import os
import sys
import argparse
import logging
import graspy


def main():
    parser = argparse.ArgumentParser(description="Graspy command line interface")
    parser.add_argument("tci", help="TICRA Command Interface file to use")
    parser.add_argument("tor", help="TOR object file to use")
    parser.add_argument("output", help="Output file to save results to")
    parser.add_argument("log", help="Log file to save logs to")
    args = parser.parse_args()

    # Generate gxp file
    logging.info("Generating gxp file")
    file_contents = [
        "[TOR file]",
        f"file = {args.tor}",
        "[TCI file]",
        f"file = {args.tci}",
    ]
    # Write to file
    with open("batch.gxp", "w") as f:
        f.write("\n".join(file_contents))

    cmd = f"ticra-tools batch.gxp {args.output}.out {args.log}.log"
    logging.info(f"Running command: {cmd}")
    os.system(cmd)
