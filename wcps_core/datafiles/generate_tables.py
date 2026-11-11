"""Generate the game server's item tables from the client's items.bin in one step.

Usage: python generate_tables.py <items file> <output dir>

<items file> can be the encoded items.bin or its decoded text (e.g. tools/legacy/data/items.txt).
Writes items.csv, item_shop.csv, weapon_damage.csv, vehicle_weapon_damage.csv and vehicles.csv
into <output dir> (e.g. wcps_game/wcps_game/client).
"""
import os
import sys
import tempfile

try:
    from wcps_core.datafiles import bincodec
    from wcps_core.datafiles.bin_to_json import parse_item_data
    from wcps_core.datafiles.json_to_csv import generate_all
except ImportError:  # run as a loose script from this folder
    import bincodec
    from bin_to_json import parse_item_data
    from json_to_csv import generate_all


def load_items(path):
    """Parsed item data from an encoded items.bin or its decoded text."""
    with open(path, "rb") as f:
        raw = f.read()
    try:
        plain = bincodec.decode(raw)
    except ValueError:
        plain = raw  # already decoded text
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        tmp.write(plain)
    try:
        return parse_item_data(tmp.name)
    finally:
        os.unlink(tmp.name)


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    items_path, out_dir = argv
    os.makedirs(out_dir, exist_ok=True)
    generate_all(load_items(items_path), out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
