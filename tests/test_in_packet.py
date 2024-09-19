import unittest
from wcps_core.packets import InPacket


class TestInPacket(unittest.TestCase):
    def setUp(self):
        self.receptor = object()  # Mock receptor object for testing

    def test_parse_packet_header(self):
        packet = bytearray(b'1726764939 4096 1 c2171580-a343-4604-8887-2daf834b59af\n')
        in_packet = InPacket(packet, self.receptor)

        self.assertEqual(in_packet.ticks, 1726764939)
        self.assertEqual(in_packet.packet_id, 4096)

    def test_parse_packet_header_with_invalid_data(self):
        in_packet = InPacket(bytearray(b'1203 4569\n'), self.receptor)
        self.assertEqual(in_packet.ticks, 1203)
        self.assertEqual(in_packet.packet_id, 4569)

    def test_block_parsing(self):
        buffer = bytearray(b'0 1 data1 data2 data3\n')
        in_packet = InPacket(buffer, self.receptor)

        self.assertEqual(len(in_packet.blocks), 3)  # Should be 3 blocks after header
        self.assertEqual(in_packet.blocks[0], "data1")
        self.assertEqual(in_packet.blocks[1], "data2")
        self.assertEqual(in_packet.blocks[2], "data3")


if __name__ == '__main__':
    unittest.main()
