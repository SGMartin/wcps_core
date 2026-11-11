"""Global.FCL ("file code list"): the client's list of files with size and checksum.

Format (Chapter 1; layout as in the WarField WRDevTool, checked against PF23):
    header   "FCLD" + int32 field + [int32] + int32 file count
             If the int32 after "FCLD" is non-zero (PF23: 0x3F8CCCCD) the count follows it at offset 8
             and entries start at 12; if it is zero, the count is at 12 and entries start at 16.
    entry    uint32 name length, name (upper case, e.g. "\\DATA\\ITEMS.BIN"), 9 stamp bytes
             (0x00 + FILETIME, little-endian), uint32 size, uint32 checksum   -> 21 + name length bytes
    checksum XOR of the file read as little-endian uint32 words, zero-padded to a multiple of 4.

update() rewrites size and checksum of existing entries in place; the header and every other byte
stay untouched (rebuilding the whole file with WRDevTool broke the header).

Usage:
    python fcl.py show   <Global.FCL> [name ...]
    python fcl.py check  <client_root> [relative path ...]   (all listed files if none given)
    python fcl.py update <client_root> <relative path> ...   (e.g. Data/items.bin)
"""
import os
import struct
import sys
from dataclasses import dataclass

MAGIC = b"FCLD"
STAMP_LEN = 9


def file_checksum(data: bytes) -> int:
    data = bytes(data) + b"\0" * (-len(data) % 4)
    checksum = 0
    for (word,) in struct.iter_unpack("<I", data):
        checksum ^= word
    return checksum


def entry_name(relative_path: str) -> str:
    """'Data/items.bin' -> '\\DATA\\ITEMS.BIN' (the key used in Global.FCL)."""
    name = relative_path.replace("/", "\\").upper()
    return name if name.startswith("\\") else "\\" + name


@dataclass
class Entry:
    name: str
    stamp: bytes
    size: int
    checksum: int
    offset: int  # offset of the uint32 name length

    @property
    def size_offset(self) -> int:
        return self.offset + 4 + len(self.name) + STAMP_LEN


class FileCodeList:
    def __init__(self, data: bytes):
        self.data = bytearray(data)
        if self.data[:4] != MAGIC:
            raise ValueError("not a Global.FCL file (missing FCLD magic)")
        if struct.unpack_from("<i", self.data, 4)[0] != 0:
            count_offset, first = 8, 12
        else:
            count_offset, first = 12, 16
        count = struct.unpack_from("<i", self.data, count_offset)[0]
        self.entries = []
        self.by_name = {}
        offset = first
        for _ in range(count):
            (name_len,) = struct.unpack_from("<I", self.data, offset)
            name = self.data[offset + 4:offset + 4 + name_len].decode("latin-1")
            pos = offset + 4 + name_len
            stamp = bytes(self.data[pos:pos + STAMP_LEN])
            size, checksum = struct.unpack_from("<II", self.data, pos + STAMP_LEN)
            entry = Entry(name, stamp, size, checksum, offset)
            self.entries.append(entry)
            self.by_name[name.upper()] = entry
            offset = pos + STAMP_LEN + 8
        if offset != len(self.data):
            raise ValueError(f"parsed {offset} of {len(self.data)} bytes: unexpected layout")

    @classmethod
    def load(cls, path: str) -> "FileCodeList":
        with open(path, "rb") as f:
            return cls(f.read())

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            f.write(self.data)

    def get(self, name: str) -> Entry:
        return self.by_name[entry_name(name)]

    def matches(self, name: str, content: bytes) -> bool:
        entry = self.get(name)
        return entry.size == len(content) and entry.checksum == file_checksum(content)

    def update(self, name: str, content: bytes) -> bool:
        """Set size and checksum of an existing entry. Returns True if anything changed."""
        entry = self.get(name)
        size, checksum = len(content), file_checksum(content)
        if (entry.size, entry.checksum) == (size, checksum):
            return False
        struct.pack_into("<II", self.data, entry.size_offset, size, checksum)
        entry.size, entry.checksum = size, checksum
        return True


def _client_file(root: str, entry_or_path: str) -> str:
    rel = entry_or_path.lstrip("\\/").replace("\\", "/")
    path = os.path.join(root, rel)
    if os.path.exists(path):
        return path
    # The FCL is upper case and the client tree is not: resolve case-insensitively.
    current = root
    for part in rel.split("/"):
        names = {n.lower(): n for n in os.listdir(current)} if os.path.isdir(current) else {}
        if part.lower() not in names:
            return path
        current = os.path.join(current, names[part.lower()])
    return current


def main(argv):
    if len(argv) < 2 or argv[0] not in ("show", "check", "update"):
        print(__doc__)
        return 2
    cmd = argv[0]
    if cmd == "show":
        fcl = FileCodeList.load(argv[1])
        print(f"{len(fcl.entries)} entries")
        for name in argv[2:]:
            e = fcl.get(name)
            print(f"{e.name}  size={e.size}  checksum={e.checksum:08x}  stamp={e.stamp.hex()}")
        return 0

    root = argv[1]
    fcl_path = _client_file(root, "Data/Global.FCL")
    fcl = FileCodeList.load(fcl_path)
    names = [entry_name(p) for p in argv[2:]] or [e.name for e in fcl.entries]

    if cmd == "check":
        bad = 0
        for name in names:
            path = _client_file(root, name)
            if not os.path.exists(path):
                print(f"missing   {name}")
                bad += 1
                continue
            with open(path, "rb") as f:
                if not fcl.matches(name, f.read()):
                    print(f"mismatch  {name}")
                    bad += 1
        print(f"checked {len(names)}, {bad} problem(s)")
        return 1 if bad else 0

    changed = 0
    for name in names:
        with open(_client_file(root, name), "rb") as f:
            if fcl.update(name, f.read()):
                print(f"updated   {name}")
                changed += 1
            else:
                print(f"unchanged {name}")
    if changed:
        fcl.save(fcl_path)
    print(f"{changed} entr{'y' if changed == 1 else 'ies'} updated in {fcl_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
