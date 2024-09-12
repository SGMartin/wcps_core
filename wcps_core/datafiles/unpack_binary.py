import sys
import os


class BinHandler:
    def __init__(self):
        self.ht_decrypt_buffer = {}
        self.lstb_output_buffer = []
        self.initialize_hex_table()

    def initialize_hex_table(self):
        for i in range(256):
            hex_key = f"{i:02X}"
            self.ht_decrypt_buffer[hex_key] = i ^ 215

    def decrypt_content(self, hex_string):
        byte_array = bytearray(
            self.ht_decrypt_buffer[hex_string[i:i+2]] for i in range(0, len(hex_string), 2)
        )
        try:
            return byte_array.decode('utf-8')
        except UnicodeDecodeError:
            print("Warning: Decryption output cannot be decoded with UTF-8.")
            return byte_array.decode('latin1')  # Handle non-UTF-8 characters


def main(input_file):
    # Check if the input file exists
    if not os.path.isfile(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return

    # Read encrypted file
    try:
        with open(input_file, mode="r") as encrypted:
            encrypted_file = encrypted.read()
    except Exception as e:
        print(f"Failed to read the file. Error: {e}")
        return

    # Initialize BinHandler
    handler = BinHandler()

    # Decrypt content
    try:
        decrypted_content = handler.decrypt_content(encrypted_file)
        output_file = f"{os.path.splitext(input_file)[0]}.decoded"
        with open(output_file, "w") as out:
            out.write(decrypted_content)
        print(f"Decrypted content saved to: {output_file}")

    except Exception as e:
        print(f"Failed to decrypt or write the file. Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_file>")
    else:
        main(sys.argv[1])
