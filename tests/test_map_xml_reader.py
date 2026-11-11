import csv
import os
import tempfile
import unittest

from wcps_core.datafiles import map_xml_reader
from wcps_core.datafiles.map_xml_reader import client_bool

MAP_INFO = """<MapInfo Version="1.0">
\t<Identity ID="{id}"/>
\t<Display DisplayName="{name}" ThumbIndex="0"/>
\t<Channel Mission="False" Medium="{medium}" Large="False"/>
\t<GameMode>
\t\t<Explosive\tSupport="False"/>
\t\t<DeathMatch\tSupport="{dm}"/>
\t\t<Conquest\tSupport="False"/>
\t\t<FFA\t\tScale="0"/>
\t\t<Tutorial\tSupport="False"/>
\t</GameMode>
\t<Restriction PayType="Free"/>
\t<Audio BGM="Theme.mp3" Ambient="None">
</MapInfo>
"""

CONTROL_POINTS = "ControlPoint.Name A\nControlPoint.Team 0\n\nControlPoint.Name B\nControlPoint.Team 1\n"

MAP_LIST = """<MapList Version="1.0">
\t<Map Name="Base"/>
\t<Map Name="Typo"/>
\t<_Map Name="XBase"/>
</MapList>
"""


class TestClientBool(unittest.TestCase):
    def test_like_the_client(self):
        for text in ("True", "Ture", "true", "Yes", "1", "-3", "ON", "on"):
            self.assertTrue(client_bool(text), text)
        for text in ("False", "false", "No", "0", "OFF", "off"):
            self.assertFalse(client_bool(text), text)
        self.assertFalse(client_bool("whatever"))
        self.assertTrue(client_bool("whatever", default=True))


class TestMapTables(unittest.TestCase):
    def test_generate(self):
        with tempfile.TemporaryDirectory() as maps, tempfile.TemporaryDirectory() as out:
            with open(os.path.join(maps, "MapList.xml"), "w") as f:
                f.write(MAP_LIST)
            # XBase is a seasonal version of Base: same ID, listed after it and commented out
            for folder, map_id, medium, dm in (
                ("Base", 1, "True", "True"),
                ("XBase", 1, "True", "True"),
                ("Typo", 2, "Ture", "Ture"),
            ):
                os.makedirs(os.path.join(maps, folder))
                with open(os.path.join(maps, folder, "MapInfo.xml"), "w") as f:
                    f.write(MAP_INFO.format(id=map_id, name=folder, medium=medium, dm=dm))
                with open(os.path.join(maps, folder, "ControlPointTemplate.dat"), "w") as f:
                    f.write(CONTROL_POINTS)

            map_xml_reader.main(maps, out)

            with open(os.path.join(out, "maps.csv"), encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            self.assertTrue(os.path.exists(os.path.join(out, "map_vehicles.csv")))

        by_id = {}
        for row in rows:
            by_id.setdefault(row["map_id"], []).append(row)
        # every row of an ID is named after the base map
        self.assertEqual({row["map_name"] for row in by_id["1"]}, {"base"})
        typo = by_id["2"][0]
        self.assertEqual((typo["uo"], typo["deathmatch"]), ("True", "True"))
        self.assertEqual((typo["flags"], typo["spawn_flags"]), ("2", "0,1"))


if __name__ == "__main__":
    unittest.main()
