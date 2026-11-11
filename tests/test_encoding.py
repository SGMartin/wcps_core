import unittest

from wcps_core.packets import InPacket, OutPacket


class TestPacketEncoding(unittest.TestCase):
    """El texto del cliente va en la página de códigos de Windows: los bytes >= 0x80 no se pierden."""

    def setUp(self):
        self.receptor = object()

    def test_chat_with_spanish_chars(self):
        # Paquete de chat real del cliente PF23 (Windows-1252): "ESPAÑA" y "Qué".
        buffer = bytearray(b"17366609 29696 3 0 NULL Santiago\x1d\x1d\x1d>>\x1dESPA\xd1A\x1dQu\xe9 \n")
        in_packet = InPacket(buffer, self.receptor)
        self.assertEqual(in_packet.packet_id, 29696)
        self.assertEqual(in_packet.blocks[3], "Santiago\x1d\x1d\x1d>>\x1dESPAÑA\x1dQué")

    def test_roundtrip_is_byte_exact(self):
        # Lo que entra sale igual, incluidos bytes CP949 (coreano) y cp1252.
        text_bytes = b"\xb0\xa1\xb3\xaa\x1d\xf1\xe9\xbf\xa1"
        in_packet = InPacket(bytearray(b"1 2 " + text_bytes + b"\n"), self.receptor)
        out = OutPacket(packet_id=2)
        out.blocks = [str(1), str(2)]
        out.append(in_packet.blocks[0])
        self.assertEqual(out.build(encrypted=False), b"1 2 " + text_bytes + b"\n")

    def test_ascii_unchanged(self):
        out = OutPacket(packet_id=4096)
        out.append("hello world")
        out.append(42)
        built = out.build(encrypted=False)
        self.assertTrue(built.endswith(b" 4096 hello\x1dworld 42\n"))

    def test_out_unicode_beyond_latin1_does_not_raise(self):
        out = OutPacket(packet_id=1)
        out.append("가나")  # fuera de latin-1
        self.assertTrue(out.build(encrypted=False).endswith(b" ??\n"))


if __name__ == "__main__":
    unittest.main()
