import os
import struct
import tempfile
import unittest

from wcps_core.datafiles import fcl


def build_fcl(entries, field=0x3F8CCCCD):
    """Synthetic Global.FCL with the PF23 header layout (non-zero field, count at 8)."""
    data = bytearray(b"FCLD" + struct.pack("<ii", field, len(entries)))
    for name, content in entries:
        raw = name.encode("latin-1")
        data += struct.pack("<I", len(raw)) + raw
        data += b"\x00" + struct.pack("<Q", 0x01C9551FD3A62D00)  # 0x00 + FILETIME
        data += struct.pack("<II", len(content), fcl.file_checksum(content))
    return bytes(data)


class TestChecksum(unittest.TestCase):
    def test_xor_of_words(self):
        self.assertEqual(fcl.file_checksum(b"\x01\x00\x00\x00\x02\x00\x00\x00"), 3)

    def test_zero_padding(self):
        self.assertEqual(fcl.file_checksum(b"\xff"), 0xFF)
        self.assertEqual(fcl.file_checksum(b""), 0)

    def test_entry_name(self):
        self.assertEqual(fcl.entry_name("Data/items.bin"), "\\DATA\\ITEMS.BIN")
        self.assertEqual(fcl.entry_name("\\DATA\\ITEMS.BIN"), "\\DATA\\ITEMS.BIN")


class TestFileCodeList(unittest.TestCase):
    def setUp(self):
        self.files = [("\\DATA\\ITEMS.BIN", b"items v1"), ("\\TEXTURE\\A.DDS", b"texture")]
        self.raw = build_fcl(self.files)

    def test_parse(self):
        doc = fcl.FileCodeList(self.raw)
        self.assertEqual(len(doc.entries), 2)
        e = doc.get("Data/items.bin")
        self.assertEqual((e.size, e.checksum), (8, fcl.file_checksum(b"items v1")))
        self.assertTrue(doc.matches("Texture/a.dds", b"texture"))

    def test_update_in_place_touches_only_size_and_checksum(self):
        doc = fcl.FileCodeList(self.raw)
        self.assertTrue(doc.update("Data/items.bin", b"items v2 longer"))
        self.assertEqual(len(doc.data), len(self.raw))
        changed = [i for i, (a, b) in enumerate(zip(self.raw, doc.data)) if a != b]
        e = doc.get("Data/items.bin")
        self.assertTrue(all(e.size_offset <= i < e.size_offset + 8 for i in changed))
        self.assertEqual(doc.data[:12], self.raw[:12])  # header untouched
        self.assertEqual(fcl.FileCodeList(bytes(doc.data)).get("Data/items.bin").size, 15)

    def test_update_unchanged(self):
        doc = fcl.FileCodeList(self.raw)
        self.assertFalse(doc.update("Data/items.bin", b"items v1"))
        self.assertEqual(bytes(doc.data), self.raw)

    def test_zero_field_layout(self):
        raw = b"FCLD" + struct.pack("<iii", 0, 7, 1) + build_fcl(self.files[:1])[12:]
        doc = fcl.FileCodeList(raw)
        self.assertEqual(doc.entries[0].name, "\\DATA\\ITEMS.BIN")

    def test_rejects_other_files(self):
        with self.assertRaises(ValueError):
            fcl.FileCodeList(b"NOPE" + b"\0" * 12)

    def test_cli_update_and_check(self):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "Data"))
            os.makedirs(os.path.join(root, "Texture"))
            with open(os.path.join(root, "Data", "Global.FCL"), "wb") as f:
                f.write(self.raw)
            with open(os.path.join(root, "Data", "items.bin"), "wb") as f:
                f.write(b"items v2")
            with open(os.path.join(root, "Texture", "a.dds"), "wb") as f:
                f.write(b"texture")
            self.assertEqual(fcl.main(["check", root]), 1)
            self.assertEqual(fcl.main(["update", root, "Data/items.bin"]), 0)
            self.assertEqual(fcl.main(["check", root]), 0)


if __name__ == "__main__":
    unittest.main()
