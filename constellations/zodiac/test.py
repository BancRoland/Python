import csv_read_zodiac

def read_from_file(root: str):
    items = []
    inside_array = False
    
    with open(f"{root}") as f:
        for line in f:
            line = line.strip()
            if len(line)>=2:
                first_char = line[0]
                if (first_char  != "#") and (first_char != ")") and (line[-2:] != "=("):
                    items.append(line)

    return items

scenario = "north_puzzle_inside"

root = "/home/roland/Desktop/Python/constellations/zodiac"
scenario_folder=f"{root}/scenarios/{scenario}"
constellation_line_list = read_from_file(f"{scenario_folder}/list_lines.sh")
constellations_for_borders_list = read_from_file(f"{scenario_folder}/list_borders.sh")
constellations_for_stars_list = read_from_file(f"{scenario_folder}/list.sh")


for constellation_for_line in constellation_line_list:
    line_data_file_path=f"{root}/constellations/prev/{constellation_for_line}.csv"

    data = csv_read_zodiac.read_lines_csv(line_data_file_path)


for constellation_for_borders in constellations_for_borders_list:
    print(constellation_for_borders)
    line_data_file_path=f"{root}/constellations/prev/borders/{constellation_for_borders}.csv"
    data = csv_read_zodiac.read_lines_csv(line_data_file_path)
    for data_elem in data:


for constellation_for_stars in constellations_for_stars_list:
    line_data_file_path=f"{root}/constellations/prev/{constellation_for_stars}.csv"

    data = csv_read_zodiac.read_csv(line_data_file_path)
