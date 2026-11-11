import csv
import os
import tempfile
import unittest

from wcps_core.datafiles import bincodec, generate_tables

ITEMS = (
    "<!--\n[ITEM_DATA]\n\t[WEAPON]\n\t\t<!--\n\t\t<BASIC_INFO>\n"
    "\t\t\tKOREAN                      =\tDE_\xb1\xb8\n"
    "\t\t\tENGLISH                     =\tDE_G36\n"
    "\t\t\tCODE                        =\tDE01\n"
    "\t\t\tACTIVE                      =\tTRUE\n"
    "\t\t\tLABEL                       =\t2\n"
    "\t\t</BASIC_INFO>\n\t\t<BUY_INFO>\n"
    "\t\t\tBUYABLE                     =\tTRUE\n"
    "\t\t\tBUYTYPE                     =\t1\n"
    "\t\t\tBUYOPTION                   =\t5\n"
    "\t\t\tCOST                        =\t-1,-1,-1,13000,-1\n"
    "\t\t\tREQ_BP                      =\t0\n"
    "\t\t\tREQ_LVL                     =\t1\n"
    "\t\t</BUY_INFO>\n\t\t<USE_INFO>\n"
    "\t\t\tAPPLY_TARGET                =\t-1\n"
    "\t\t</USE_INFO>\n\t\t//-->\n\t[/WEAPON]\n[/ITEM_DATA]\n//-->\n"
).encode("latin-1")


class TestGenerateTables(unittest.TestCase):
    def check_shop(self, items_path):
        with tempfile.TemporaryDirectory() as out:
            self.assertEqual(generate_tables.main([items_path, out]), 0)
            with open(os.path.join(out, "item_shop.csv"), encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[0]["code"], "DE01")
            self.assertEqual(rows[0]["required_premium"], "-1")
            self.assertEqual(rows[0]["cost"], "-1,-1,-1,13000,-1")
            for name in ("items", "weapon_damage", "vehicle_weapon_damage", "vehicles"):
                self.assertTrue(os.path.exists(os.path.join(out, f"{name}.csv")))

    def test_from_decoded_text(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(ITEMS)
        try:
            self.check_shop(f.name)
        finally:
            os.unlink(f.name)

    def test_from_encoded_bin(self):
        with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as f:
            f.write(bincodec.encode(ITEMS))
        try:
            self.check_shop(f.name)
        finally:
            os.unlink(f.name)


if __name__ == "__main__":
    unittest.main()
