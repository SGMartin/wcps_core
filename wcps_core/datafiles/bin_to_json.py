import re
import json


def parse_section(content, start_tag, end_tag):
    pattern = re.compile(rf"{start_tag}(.*?){end_tag}", re.DOTALL)
    matches = pattern.findall(content)
    return matches


def parse_block(block):
    result = {}
    block = re.sub(r"<!--|//-->", "", block).strip()
    sections = re.findall(r"<(.*?)>(.*?)</\1>", block, re.DOTALL)
    for section, content in sections:
        # Check if section is RIDING_INFO to handle nested blocks differently
        if section == "RIDING_INFO":
            seats = re.findall(r"<(.*?)>(.*?)</\1>", content, re.DOTALL)
            result["SEATS"] = []
            for seat_name, seat_content in seats:
                items = re.findall(r"(\w+)\s+=\s+(.*)", seat_content.strip())
                seat_data = {key: value.strip() for key, value in items}
                seat_data["TYPE"] = seat_name
                result["SEATS"].append(seat_data)
        else:
            items = re.findall(r"(\w+)\s+=\s+(.*)", content.strip())
            result[section] = {key: value.strip() for key, value in items}
    return result


def parse_item_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    item_data = {
        "RESOURCE": [],
        "CHARACTER": [],
        "ETC": [],
        "WEAPON": [],
        "EQUIPMENT": [],
        "E_WEAPON": []
    }

    # Process general item types
    for item_type in item_data.keys():
        start_tag = rf"\[{item_type}\]"
        end_tag = rf"\[/{item_type}\]"
        sections = parse_section(content, start_tag, end_tag)

        for section in sections:
            blocks = re.findall(r"<!--(.*?)//-->", section, re.DOTALL)
            for block in blocks:
                parsed_block = parse_block(block)
                item_data[item_type].append(parsed_block)

    return item_data


def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Example usage
file_path = "output/decoded/items.bin.decoded"
parsed_data = parse_item_data(file_path)
save_json(parsed_data, "item_data.json")
