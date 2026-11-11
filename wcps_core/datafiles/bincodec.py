"""Byte-exact codec for the client's encoded data files (items.bin, branch.bin, weapondata.bin,
FileCodes.bin).

On disk each file is ASCII hex (uppercase, no separators) of the plain text XORed with 0xD7 (215).
The plain text is not UTF-8: names are CP949 (Korean) bytes, so everything here works on bytes and
never decodes text. decode() followed by encode() reproduces the original file exactly.
"""

XOR_KEY = 0xD7


def decode(encoded: bytes) -> bytes:
    """Encoded file contents (hex text) -> plain text bytes."""
    data = bytes(encoded).strip()
    if len(data) % 2:
        raise ValueError("encoded data has an odd number of hex digits")
    try:
        raw = bytes.fromhex(data.decode("ascii"))
    except (UnicodeDecodeError, ValueError) as e:
        raise ValueError(f"encoded data is not plain hex: {e}") from None
    return bytes(b ^ XOR_KEY for b in raw)


def encode(plain: bytes) -> bytes:
    """Plain text bytes -> encoded file contents (uppercase hex text)."""
    return bytes(b ^ XOR_KEY for b in plain).hex().upper().encode("ascii")
