import time 

from wcps_core.constants import InternalKeys

class InPacket:
    def __init__(self, buffer: bytearray, xor_key: int = InternalKeys.XOR_RECIEVE):
        self.decoded_buffer = self.xor_decrypt(packet_buffer=buffer, xor_key=xor_key)
        self.blocks = self.decoded_buffer.split(" ")
        self.ticks, self.packet_id = self.parse_packet_header(blocks=self.blocks)
        self.blocks = self.blocks[2:]

    def parse_packet_header(self, blocks: list) -> tuple:
        header = (blocks[0], blocks[1])
        try:
            return tuple(int(x) for x in header)
        except ValueError as e:
            print(f"Cannot parse packet header: {e}")
            return header

    def xor_decrypt(self, packet_buffer: bytearray, xor_key: int) -> str:
        # Decrypt the bytes with the xOrKey.
        this_buffer = bytearray(packet_buffer)
        for i in range(len(this_buffer)):
            this_buffer[i] = this_buffer[i] ^ xor_key

        # Return the decrypted packet
        decoded_buffer = this_buffer.decode("utf-8")
        return decoded_buffer


class OutPacket:
    def __init__(self, packet_id: int, xor_key: int = InternalKeys.XOR_SEND):
        self.packet_id = packet_id
        self.ticks = int(time.time())
        self.blocks = [str(self.ticks), str(self.packet_id)]
        self.xor_key = xor_key


    def value_to_block(self, value) -> str:
        if isinstance(value, bool):
            value_to_append = "1" if value else "0"
        elif isinstance(value, str):
            value_to_append = value.replace(" ", chr(0x1D))
        else:
            value_to_append = str(value)

        return value_to_append


    def append(self, value) -> None:
        transcoded = self.value_to_block(value)
        self.blocks.append(transcoded)


    def fill(self, value, times:int) -> None:
        transcoded = self.value_to_block(value)
        self.blocks.extend([transcoded] * times)


    def xor_encrypt(self, packet:str) -> bytearray:
        buffer = bytearray(packet)
        for i in range(len(buffer)):
            buffer[i] = buffer[i] ^ self.xor_key 
        
        return buffer


    def build(self, encrypted: bool = True) -> bytearray | bytes:
        full_packet = " ".join(self.blocks)
        # End of packet character
        full_packet += chr(0xA) 
        full_packet = full_packet.encode("utf-8")

        if encrypted:
            full_packet = self.xor_encrypt(packet=full_packet)

        return full_packet