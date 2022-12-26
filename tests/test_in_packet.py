import time
import unittest

from wcps_core.constants import InternalKeys
from wcps_core.packets import InPacket

class TestInPacket(unittest.TestCase):
    def setUp(self):
        self.buffer = bytearray(b'\xf2\xf6\xf4\xf6\xf1\xf2\xf4\xf0\xe3\xf7\xf2\xf2\xf1\xe3\xc9')
        self.packet = InPacket(self.buffer, xor_key=0xC3)

    def test_xor_decrypt(self):
        # Test decryption with a different key
        self.assertEqual(self.packet.decoded_buffer, "15752173 4112 \n")

    def test_parse_packet_header(self):
        self.assertEqual((self.packet.ticks, self.packet.packet_id), (15752173, 4112))
        
if __name__ == '__main__':
    unittest.main()