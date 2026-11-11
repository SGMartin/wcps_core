"""Generate the game server's map tables from the client's Maps folder.

Usage: python map_xml_reader.py <client Maps folder> <output dir>

Reads MapList.xml and, for every listed map, its MapInfo.xml, ControlPointTemplate.dat and
ObjectSpawnTemplate.dat. Writes maps.csv and map_vehicles.csv into <output dir>
(e.g. wcps_game/wcps_game/client).
"""
import csv
import json
import os
import re
import sys
import xml.etree.ElementTree as ET


def client_bool(value, default=False):
    """Read a boolean the way the client does (FUN_00716060 in PF23).

    A non-zero number, or text starting with T/t/Y/y, or "ON" is true; text starting with
    0/F/f/N/n, or "OFF" is false; anything else gives the default. So the client reads the
    "Ture" typo in some MapInfo.xml (e.g. Paroho) as true.
    """
    text = (value or "").strip()
    try:
        if int(text) != 0:
            return True
    except ValueError:
        pass
    if text[:1] in ("T", "t", "Y", "y") or text.upper().startswith("ON"):
        return True
    if text[:1] in ("0", "F", "f", "N", "n") or text.upper().startswith("OFF"):
        return False
    return default


def parse_map_list(xml_string):
    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Initialize an empty list to hold the map data
    maps = []

    # Iterate through each map in the XML
    for map_element in root.findall("Map"):
        map_name = map_element.get("Name")
        maps.append({"name": map_name, "active": True})

    # Check for the inactive maps and update the "active" field
    for map_element in root.findall("_Map"):
        map_name = map_element.get("Name")
        maps.append({"name": map_name, "active": False})

    # Convert the list to a JSON formatted string
    return json.dumps(maps, indent=4)


def parse_map_info(xml_string):
    # Remove the unclosed <Audio> tag
    xml_string = re.sub(r"<Audio\b[^>]*>", "", xml_string)

    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Initialize the dictionary to hold the parsed data
    map_info = {}

    # Parse Identity ID
    identity_element = root.find("Identity")
    if identity_element is not None:
        map_info["Identity"] = identity_element.get("ID")

    # Parse Display information (ThumbIndex)
    display_element = root.find("Display")
    if display_element is not None:
        map_info["ThumbIndex"] = display_element.get("ThumbIndex")

    # Parse Channel information
    channel_element = root.find("Channel")
    if channel_element is not None:
        map_info["Channel"] = {
            "Mission": channel_element.get("Mission"),
            "Medium": channel_element.get("Medium"),
            "Large": channel_element.get("Large"),
        }

    # Parse GameMode information
    game_mode_element = root.find("GameMode")
    if game_mode_element is not None:
        game_mode_data = {}
        for mode in game_mode_element:
            mode_name = mode.tag
            if mode.get("Support") is not None:
                game_mode_data[mode_name] = mode.get("Support")
            if mode.get("Scale") is not None:
                game_mode_data[mode_name] = mode.get("Scale")
        map_info["GameMode"] = game_mode_data

    # Parse Restriction information
    restriction_element = root.find("Restriction")
    if restriction_element is not None:
        map_info["Restriction"] = restriction_element.get("PayType")

    # Convert the dictionary to a JSON formatted string
    return json.dumps(map_info, indent=4)


def parse_control_points(control_point_file_stream):
    entities = control_point_file_stream.strip().split("\n\n")
    team_dict = {
        0: [],
        1: [],
    }  # Initialize the dictionary for team 0 (DERB) and team 1 (NIU)
    entity_count = len(entities)  # Count the number of entities

    for idx, entity in enumerate(entities):
        lines = entity.splitlines()
        team = None
        for line in lines:
            if line.startswith("ControlPoint.Team"):
                team = int(line.split()[-1])
                break

        # If team is not -1, add the entity ID to the dictionary
        if team in team_dict:
            team_dict[team].append(idx)

    return entity_count, team_dict


def parse_vehicles(vehicle_data_stream):
    entities = vehicle_data_stream.strip().split("\n\n")
    vehicles = {}

    for idx, entity in enumerate(entities):
        lines = entity.splitlines()
        for line in lines:
            if line.startswith("ObjectSpawn.Code"):
                vehicle_code = line.split()[-1]
            elif line.startswith("ObjectSpawn.SpawnInterval"):
                spawn_interval = int(line.split()[-1])
            elif line.startswith("ObjectSpawn.Position"):
                raw_coords = line.split()[-1]
                full_coords = [float(coord) for coord in raw_coords.split("/")]

        # If team is not -1, add the entity ID to the dictionary
        if vehicle_code is not None:
            vehicles[idx] = {
                "code": vehicle_code,
                "coords": full_coords,
                "spawn_interval": spawn_interval,
            }

    return vehicles


def parse_map_settings_to_csv(input_json, mapper, csv_file_path):
    # Load JSON data from the string (or from a file if needed)
    data = json.loads(input_json)

    # Define the CSV columns
    csv_columns = [
        "map_id",
        "map_name",
        "cqc",
        "uo",
        "bg",
        "explosive",
        "deathmatch",
        "conquest",
        "ffa",
        "premium",
        "active",
        "flags",
        "spawn_flags",
    ]

    # Prepare the data for CSV writing
    csv_data = []
    for item in data:
        spawn_flags = ",".join(
            [str(value[0]) for value in item["spawn_flags"].values()]
        )
        row = {
            "map_id": item["Identity"],
            "map_name": mapper.get(item["Identity"], "unknown"),
            "cqc": client_bool(item["Channel"]["Mission"]),
            "uo": client_bool(item["Channel"]["Medium"]),
            "bg": client_bool(item["Channel"]["Large"]),
            "explosive": client_bool(item["GameMode"]["Explosive"]),
            "deathmatch": client_bool(item["GameMode"]["DeathMatch"]),
            "conquest": client_bool(item["GameMode"]["Conquest"]),
            "ffa": item["GameMode"]["FFA"],
            "premium": item["Restriction"],
            "active": True,
            "flags": item["flags"],
            "spawn_flags": spawn_flags,
        }
        csv_data.append(row)

    # Write the data to the CSV file
    with open(csv_file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"Map settings saved to CSV: {csv_file_path}")


def parse_vehicles_to_csv(data, filename):
    """
    Writes the nested dictionary to a CSV file.

    Parameters:
    - data (dict): The nested dictionary containing the data.
    - filename (str): The name of the CSV file to write to.
    """
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["map_id", "vehicle_id", "vehicle_code", "coords", "spawn_interval"])

        # Iterate over the top-level dictionary
        for map_id, nested_dict in data.items():
            # Iterate over the nested dictionary
            for vehicle_id, entry in nested_dict.items():
                vehicle_code = entry.get("code", "")
                coords = entry.get("coords", "")
                coords = "/".join([str(coord) for coord in coords])
                spawn_interval = entry.get("spawn_interval", "")

                # Write the row to the CSV file
                writer.writerow([map_id, vehicle_id, vehicle_code, coords, spawn_interval])

    print("Exported vehicles to map vehicle table")


def main(input_directory, output_directory):
    with open(file=os.path.join(input_directory, "MapList.xml"), mode="r") as map_file:
        maps_xml_list = map_file.read()

    map_list_json = parse_map_list(maps_xml_list)

    # Get all of the map folders
    map_folders = [
        name
        for name in os.listdir(input_directory)
        if os.path.isdir(os.path.join(input_directory, name))
    ]

    map_dict = {map_folder.lower(): map_folder for map_folder in map_folders}

    all_map_settings = []
    id_name_mapper = {}
    all_vehicles = {}

    for listed_map in json.loads(map_list_json):
        this_map = listed_map["name"]
        vehicle_file = os.path.join(
            input_directory,
            map_dict[this_map.lower()],
            "ObjectSpawnTemplate.dat"
            )
        has_vehicles = os.path.isfile(vehicle_file)

        if this_map.lower() in map_dict.keys():
            with open(
                file=os.path.join(
                    input_directory, map_dict[this_map.lower()], "MapInfo.xml"
                ),
                mode="r",
            ) as map_data, open(
                file=os.path.join(
                    input_directory,
                    map_dict[this_map.lower()],
                    "ControlPointTemplate.dat",
                ),
                mode="r",
            ) as spawn_points:
                map_data_file = map_data.read()
                # Load main xml settings
                map_data_json = parse_map_info(map_data_file)
                map_data_json = json.loads(map_data_json)
                # Load spawn settings
                map_spawn_points = parse_control_points(spawn_points.read())
                # Append them to map data
                map_data_json["flags"] = map_spawn_points[0]
                map_data_json["spawn_flags"] = map_spawn_points[1]

                # Parse vehicles if needed
                if has_vehicles:
                    with open(vehicle_file, "r") as vehicle_stream:
                        raw_vehicles = vehicle_stream.read()
                        vehicles = parse_vehicles(raw_vehicles)
                        all_vehicles[int(map_data_json["Identity"])] = vehicles

                # Append to map settings
                # Seasonal maps share the ID of their base map (e.g. XMarien and Marien are both 12):
                # name the ID after the first map listed, the base one.
                map_id = map_data_json["Identity"]
                id_name_mapper.setdefault(map_id, this_map.lower())
                all_map_settings.append(map_data_json)

    os.makedirs(output_directory, exist_ok=True)

    # Export to csv
    parse_map_settings_to_csv(
        json.dumps(all_map_settings, indent=4),
        id_name_mapper,
        os.path.join(output_directory, "maps.csv"),
    )

    # Generate vehicle table
    parse_vehicles_to_csv(all_vehicles, filename=os.path.join(output_directory, "map_vehicles.csv"))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
