"""Encode a plain text data file back into the client format, byte for byte.

Usage: python pack_binary.py <path_to_file>   ->   <path_to_file without extension>.encoded
"""
import os
import sys

try:
    from wcps_core.datafiles import bincodec
except ImportError:  # run as a loose script from this folder
    import bincodec


def main(input_file):
    if not os.path.isfile(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return

    with open(input_file, "rb") as f:
        plain = f.read()

    output_file = f"{os.path.splitext(input_file)[0]}.encoded"
    with open(output_file, "wb") as out:
        out.write(bincodec.encode(plain))
    print(f"Encrypted content saved to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pack_binary.py <path_to_file>")
    else:
        main(sys.argv[1])
