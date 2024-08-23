import json
import csv
import argparse
import os


def generate_items_table(json_data, output_csv_file):
    with open(output_csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["code", "english", "active", "source"])

        for key in ["RESOURCE", "CHARACTER", "ETC", "WEAPON", "E_WEAPON"]:
            if key in json_data:
                for item in json_data[key]:
                    basic_info = item.get("BASIC_INFO", {})
                    code = basic_info.get("CODE", "")
                    english = basic_info.get("ENGLISH", "")
                    active = basic_info.get("ACTIVE", "")
                    writer.writerow([code, english, active, key])


def generate_item_shop_table(json_data, output_csv_file):
    with open(output_csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "code", "is_buyable",
            "buy_type", "buy_option",
            "cost", "required_bp",
            "required_level",
            "required_premium"
            ]
            )

        for key in ["RESOURCE", "CHARACTER", "ETC", "WEAPON", "E_WEAPON"]:
            if key in json_data:
                for item in json_data[key]:
                    basic_info = item.get("BASIC_INFO", {})
                    buy_info = item.get("BUY_INFO", {})
                    buy2_info = item.get("USE_INFO", {})
                    code = basic_info.get("CODE", "")
                    is_buyable = buy_info.get("BUYABLE", "")
                    buy_type = buy_info.get("BUYTYPE", "")
                    buy_option = buy_info.get("BUYOPTION", "")
                    cost = buy_info.get("COST", "")
                    required_bp = buy_info.get("REQ_BP", "")
                    required_level = buy_info.get("REQ_LVL", "")
                    required_premium = buy2_info.get("APPLY_TARGET", "")
                    writer.writerow([
                        code, is_buyable,
                        buy_type, buy_option,
                        cost, required_bp,
                        required_level,
                        required_premium]
                        )


def generate_weapon_damage_table(json_data, output_csv_file):
    with open(output_csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["code", "power", "personal", "surface", "air", "ship"])

        if "WEAPON" in json_data:
            for weapon in json_data["WEAPON"]:
                basic_info = weapon.get("BASIC_INFO", {})
                code = basic_info.get("CODE", "")

                ability_info = weapon.get("ABILITY_INFO", {})
                power = ability_info.get("POWER", "")

                target_info = weapon.get("TARGET_INFO", {})
                personal = target_info.get("PERSONAL", "")
                surface = target_info.get("SURFACE", "")
                air = target_info.get("AIR", "")
                ship = target_info.get("SHIP", "")

                writer.writerow([code, power, personal, surface, air, ship])


def generate_vehicle_weapon_damage_table(json_data, output_csv_file):
    with open(output_csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "code", "power", "personal", "surface", "air", "ship"])

        if "E_WEAPON" in json_data:
            for weapon in json_data["E_WEAPON"]:
                basic_info = weapon.get("BASIC_INFO", {})
                name = basic_info.get("ENGLISH", "")
                code = basic_info.get("CODE", "")

                ability_info = weapon.get("ABILITY_INFO", {})
                power = ability_info.get("POWER", "")

                target_info = weapon.get("TARGET_INFO", {})
                personal = target_info.get("PERSONAL", "")
                surface = target_info.get("SURFACE", "")
                air = target_info.get("AIR", "")
                ship = target_info.get("SHIP", "")

                writer.writerow([name, code, power, personal, surface, air, ship])


def generate_vehicle_table(json_data, output_csv_file):
    with open(output_csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "name",
            "code",
            "health",
            "seat_id",
            "weapon_code",
            "weapon_ammo",
            "weapon_magazine",
            "armor_type"
            ]
            )

        if "EQUIPMENT" in json_data:
            for vehicle in json_data["EQUIPMENT"]:
                basic_info = vehicle.get("BASIC_INFO", {})
                name = basic_info.get("ENGLISH", "")
                code = basic_info.get("CODE", "")

                ability_info = vehicle.get("ABILITY_INFO", {})
                vehicle_health = ability_info.get("DEFENCE", 0)

                seats = vehicle.get("RIDING_INFO", {})

                for seat in seats.values():
                    print(seat)
                    seat_id = seat.get("SEAT_NUMBER", "")
                    weapon_code = seat.get("CODE", "")
                    weapon_ammo = seat.get("AMMONNUM", 0)
                    weapon_magazine = seat.get("MAGAZINENUM", 0)
                    armor_type = seat.get("ARMOR_TYPE", 0)

                    writer.writerow([
                        name,
                        code,
                        vehicle_health,
                        seat_id,
                        weapon_code,
                        weapon_ammo,
                        weapon_magazine,
                        armor_type]
                    )


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate CSV files from JSON data.")
    parser.add_argument("json_file", type=str, help="Path to the input JSON file")
    args = parser.parse_args()

    json_file_path = args.json_file
    if not os.path.isfile(json_file_path):
        print(f"Error: The file {json_file_path} does not exist.")
        return

    # Determine output file paths
    base_dir = os.path.dirname(json_file_path)
    items_table_path = os.path.join(base_dir, "items.csv")
    item_shop_table_path = os.path.join(base_dir, "item_shop.csv")
    weapon_damage_table_path = os.path.join(base_dir, "weapon_damage.csv")
    e_weapons_table_path = os.path.join(base_dir, "vehicle_weapon_damage.csv")
    vehicle_table_path = os.path.join(base_dir, "vehicles.csv")

    # Load JSON data
    with open(json_file_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # Generate the CSV tables
    generate_items_table(json_data, items_table_path)
    generate_item_shop_table(json_data, item_shop_table_path)
    generate_weapon_damage_table(json_data, weapon_damage_table_path)
    generate_vehicle_weapon_damage_table(json_data, e_weapons_table_path)
    generate_vehicle_table(json_data, vehicle_table_path)

    print("CSV files generated:")
    print(f"- {items_table_path}")
    print(f"- {item_shop_table_path}")
    print(f"- {weapon_damage_table_path}")
    print(f"- {vehicle_table_path}")


if __name__ == "__main__":
    main()
