"""Decode a client data file (e.g. items.bin) into its plain text, byte for byte.

Usage: python unpack_binary.py <path_to_file>   ->   <path_to_file without extension>.decoded
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
        encoded = f.read()
    try:
        plain = bincodec.decode(encoded)
    except ValueError as e:
        print(f"Failed to decode '{input_file}': {e}")
        return

    output_file = f"{os.path.splitext(input_file)[0]}.decoded"
    with open(output_file, "wb") as out:
        out.write(plain)
    print(f"Decrypted content saved to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python unpack_binary.py <path_to_file>")
    else:
        main(sys.argv[1])
