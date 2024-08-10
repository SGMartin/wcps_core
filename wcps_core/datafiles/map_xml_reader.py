import json
import os
import re
import sys
import xml.etree.ElementTree as ET


def parse_map_list(xml_string):
    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Initialize an empty list to hold the map data
    maps = []

    # Iterate through each map in the XML
    for map_element in root.findall("Map"):
        map_name = map_element.get("Name")
        maps.append({
            "name": map_name,
            "active": True
        })

    # Check for the inactive maps and update the "active" field
    for map_element in root.findall("_Map"):
        map_name = map_element.get("Name")
        maps.append({
            "name": map_name,
            "active": False
        })

    # Convert the list to a JSON formatted string
    return json.dumps(maps, indent=4)


def parse_map_info(xml_string):
    # Remove the unclosed <Audio> tag
    xml_string = re.sub(r'<Audio\b[^>]*>', '', xml_string)

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
            "Large": channel_element.get("Large")
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


def main(input_directory):
    with open(file=os.path.join(input_directory, "MapList.xml"), mode="r") as map_file:
        maps_xml_list = map_file.read()

    map_list_json = parse_map_list(maps_xml_list)

    # Get all of the map folders
    map_folders = [
        name for name
        in os.listdir(input_directory)
        if os.path.isdir(os.path.join(input_directory, name))
        ]

    map_dict = {map_folder.lower(): map_folder for map_folder in map_folders}

    all_map_settings = []
    for listed_map in json.loads(map_list_json):
        this_map = listed_map["name"]

        if this_map.lower() in map_dict.keys():
            with open(
                file=os.path.join(input_directory, map_dict[this_map.lower()], "MapInfo.xml"),
                mode="r"
            ) as map_data:
                map_data_file = map_data.read()
                map_data_json = parse_map_info(map_data_file)

                all_map_settings.append(json.loads(map_data_json))

    map_settings_file = "output/json/map_settings.json"
    map_list_file = "output/json/map_list.json"

    # Save the JSON data to a file
    with open(map_settings_file, "w") as outfile:
        json.dump(all_map_settings, outfile, indent=4)

        # Save the JSON data to a file
    with open(map_list_file, "w") as outfile:
        json.dump(json.loads(map_list_json), outfile, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_file>")
    else:
        main(sys.argv[1])
