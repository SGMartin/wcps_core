import unittest

from wcps_core.datafiles import bincodec


class TestBinCodec(unittest.TestCase):
    def test_roundtrip_keeps_cp949_bytes(self):
        # Plain text with CRLF, tabs and a CP949 name (not valid UTF-8).
        plain = b"<!--\r\n\t\tKOREAN\t=\tDF_\xbd\xba\xc4\xda\xc7\xc7\xbf\xc2\r\n//-->\r\n"
        encoded = bincodec.encode(plain)
        self.assertEqual(bincodec.decode(encoded), plain)

    def test_encoded_format(self):
        # 'A' (0x41) ^ 0xD7 = 0x96; uppercase hex, no separators.
        self.assertEqual(bincodec.encode(b"A\n"), b"96DD")

    def test_decode_reencode_is_identical(self):
        original = bincodec.encode(bytes(range(256)))
        self.assertEqual(bincodec.encode(bincodec.decode(original)), original)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            bincodec.decode(b"ABC")
        with self.assertRaises(ValueError):
            bincodec.decode(b"ZZ")


if __name__ == "__main__":
    unittest.main()
