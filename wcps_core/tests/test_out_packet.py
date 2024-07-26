import unittest
from wcps_core.packets import OutPacket

class TestOutPacket(unittest.TestCase):
    def setUp(self):
        self.packet = OutPacket(packet_id=123)
        self.transcoded_hello = "hello world".replace(" ", chr(0x1D))

    def test_value_to_block(self):
        # Test bool value
        self.assertEqual(self.packet.value_to_block(True), "1")
        self.assertEqual(self.packet.value_to_block(False), "0")

        # Test string value
        self.assertEqual(self.packet.value_to_block("hello world"), self.transcoded_hello)
        self.assertEqual(self.packet.value_to_block("hello world "), f"{self.transcoded_hello}{chr(0x1D)}")

        # Test int value
        self.assertEqual(self.packet.value_to_block(123), "123")

    def test_append(self):
        self.packet.append("hello world")
        self.assertEqual(self.packet.blocks[-1], self.transcoded_hello)

    def test_fill(self):
        self.packet.fill("hello world", 3)
        self.assertEqual(self.packet.blocks[-3:], [self.transcoded_hello] * 3)

    def test_xor_encrypt(self):
        encrypted = self.packet.xor_encrypt("hello world".encode("utf-8"))
        print(encrypted)
        self.assertEqual(encrypted, b'\xcb\xc6\xcf\xcf\xcc\x83\xd4\xcc\xd1\xcf\xc7')

    def test_build(self):
        self.packet = OutPacket(packet_id=123)
        ## Spoof time block for testing
        self.packet.blocks[0] = "111"
        results = f"111 123{chr(0x0A)}".encode("utf-8")
        encrypted_results = self.packet.xor_encrypt(packet=results)

        self.assertEqual(self.packet.build(encrypted=False), results)
        self.assertEqual(self.packet.build(), encrypted_results)  

if __name__ == '__main__':
    unittest.main()
