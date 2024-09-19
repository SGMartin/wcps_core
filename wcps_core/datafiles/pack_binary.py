import sys
import os


class BinHandler:
    def __init__(self):
        self.ht_encrypt_buffer = {}
        self.initialize_hex_table()

    def initialize_hex_table(self):
        # Create a reverse map for encoding: value -> key (reversing the decryption map)
        self.ht_encrypt_buffer = {i ^ 215: f"{i:02X}" for i in range(256)}

    def encrypt_content(self, text):
        # Convert each character to its corresponding hex string using XOR encryption
        byte_array = text.encode('utf-8')
        encrypted_string = ''.join(self.ht_encrypt_buffer[b] for b in byte_array)
        return encrypted_string


def main(input_file):
    # Check if the input file exists
    if not os.path.isfile(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return

    # Read the plain text file
    try:
        with open(input_file, mode="r", encoding="utf-8") as plain_file:
            plain_text = plain_file.read()
    except Exception as e:
        print(f"Failed to read the file. Error: {e}")
        return

    # Initialize BinHandler
    handler = BinHandler()

    # Encrypt content
    try:
        encrypted_content = handler.encrypt_content(plain_text)
        output_file = f"{os.path.splitext(input_file)[0]}.encoded"
        with open(output_file, "w") as out:
            out.write(encrypted_content)
        print(f"Encrypted content saved to: {output_file}")

    except Exception as e:
        print(f"Failed to encrypt or write the file. Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python encode_script.py <path_to_file>")
    else:
        main(sys.argv[1])
