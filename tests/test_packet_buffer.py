import unittest
from wcps_core.constants import InternalKeys
from wcps_core.packets import PacketBuffer, InPacket


class TestPacketBuffer(unittest.TestCase):
    def setUp(self):
        self.receptor = object()  # Mock receptor object for testing

    def test_xor_decrypt(self):
        packet_buffer = bytearray([1, 2, 3, 4, 5])
        xor_key = InternalKeys.XOR_AUTH_SEND  # Replace with an actual value for testing
        decrypted_buffer = PacketBuffer.xor_decrypt(self, packet_buffer, xor_key)

        # Assert that decrypted buffer has the expected values (this will depend on your xor_key)
        expected_decrypted = bytearray(
            [1 ^ xor_key, 2 ^ xor_key, 3 ^ xor_key, 4 ^ xor_key, 5 ^ xor_key]
        )
        self.assertEqual(decrypted_buffer, expected_decrypted)

    def test_find_packets(self):
        buffer = bytearray(b"packet1\npacket2\npacket3\n")
        packet_buffer = PacketBuffer(buffer, self.receptor)

        packets = packet_buffer.find_packets(buffer)

        self.assertEqual(len(packets), 3)
        self.assertEqual(packets[0], b"packet1\n")
        self.assertEqual(packets[1], b"packet2\n")
        self.assertEqual(packets[2], b"packet3\n")

    def test_packet_creation(self):

        buffer = bytearray(b'\xcb\xc6\xcf\xcf\xcc\x83\xd4\xcc\xd1\xcf\xc7\xa9')  # Example packet
        packet_buffer = PacketBuffer(buffer, self.receptor, xor_key=InternalKeys.XOR_GAME_SEND)
        self.assertEqual(len(packet_buffer.packet_stack), 1)
        self.assertIsInstance(packet_buffer.packet_stack[0], InPacket)

    def test_invalid_buffer_handling(self):
        invalid_buffer = bytearray(b"")
        packet_buffer = PacketBuffer(invalid_buffer, self.receptor)
        self.assertEqual(len(packet_buffer.packet_stack), 0)


if __name__ == "__main__":
    unittest.main()
