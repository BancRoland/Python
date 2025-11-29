import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi
import utils
import argparse
import toml
import time
import csv_read_zodiac

def read_from_file(root: str):
    items = []
    
    with open(f"{root}") as f:
        for line in f:
            line = line.strip()
            if len(line)>=2:
                first_char = line[0]
                if (first_char  != "#") and (first_char != ")") and (line[-2:] != "=("):
                    items.append(line)

    return items

# scenario = "orion"
# scenario = "north_puzzle_inside"
scenario = 'cylindrical_puzzle'
# scenario = 'centaur'

# scenario = 'orion'


root = "/home/roland/Desktop/Python/constellations/zodiac"
scenario_folder=f"{root}/scenarios/{scenario}"
constellation_line_list = read_from_file(f"{scenario_folder}/list_lines.sh")
constellations_for_borders_list = read_from_file(f"{scenario_folder}/list_borders.sh")
constellations_for_stars_list = read_from_file(f"{scenario_folder}/list.sh")


# for constellation_for_line in constellation_line_list:
#     line_data_file_path=f"{root}/constellations/prev/{constellation_for_line}.csv"

#     data = csv_read_zodiac.read_lines_csv(line_data_file_path)


# for constellation_for_borders in constellations_for_borders_list:
#     line_data_file_path=f"{root}/constellations/prev/borders/{constellation_for_borders}.csv"

#     data = csv_read_zodiac.read_lines_csv(line_data_file_path)

# for constellation_for_stars in constellations_for_stars_list:
#     line_data_file_path=f"{root}/constellations/prev/{constellation_for_stars}.csv"

#     data = csv_read_zodiac.read_csv(line_data_file_path)


print("zodiac_plotter.py started")

STR_GRPH_PROJ   =   False
CYLINDRICAL     =   True
POLAR           =   False
POLAR_LINES     =   False
SPHERRICAL      =   False

DPI=500
# DPI=50

# Path to the TOML file
toml_file = f"{scenario_folder}/variables.toml"

# Load the TOML file
with open(toml_file, "r") as f:
    data = toml.load(f)

# Accessing values
time_values = data.get("time", {})
coordinates_values = data.get("coordinates", {})
z_rotation_values = data.get("z_rotation", {})

# Extracting specific values
center_ra_hour = time_values.get("Ra_hour")
center_ra_min = time_values.get("Ra_min")
center_ra_sec = time_values.get("Ra_sec")

center_Dec_deg0 = coordinates_values.get("Dec_deg")
center_Dec_degmin = coordinates_values.get("Dec_min")
center_Dec_degsec = coordinates_values.get("Dec_sec")

zrot_deg = z_rotation_values.get("zrot")
fov = z_rotation_values.get("fov")
if fov == "None":
    fov=180

parser = argparse.ArgumentParser(description="calculate the area of circle with radius r")

# parser.add_argument("-Ra","--rightascension", help="Rectascension value of center", nargs='?', type=float, const=1, default=0)
parser.add_argument("-dec_deg0","--declination_deg0", help="declination value of center", type=float, default=90)
parser.add_argument("-dec_degmin","--declination_degmin", help="declination value of center", type=float, default=0)
parser.add_argument("-dec_degsec","--declination_degsec", help="declination value of center", type=float, default=0)

parser.add_argument("-RA_hour","--rectascension_hour", help="rectascension hour value of center", type=float, default=0)
parser.add_argument("-RA_min","--rectascension_min", help="rectascension minute value of center", type=float, default=0)
parser.add_argument("-RA_sec","--rectascension_sec", help="rectascension second value of center", type=float, default=0)
parser.add_argument("-zrot","--zrot", help="declination second value of center", type=float, default=0)
parser.add_argument("-a","--a", help="declination second value of center", type=float, default=1.5)
parser.add_argument("-hmg","--hmg", help="declination second value of center", type=float, default=4)
parser.add_argument("-hmg2","--hmg2", help="declination second value of center", type=float, default=2)


args=parser.parse_args()


center_ra_deg=((center_ra_hour+center_ra_min/60+center_ra_sec/60/60)/24)*360
center_Dec_deg=center_Dec_deg0+center_Dec_degmin/60+center_Dec_degsec/60/60


a       = args.a
hmg     = args.hmg
hmg2    = args.hmg2

const=np.load("stars_test.npy", allow_pickle=True)
lines=np.load("lines_data.npy", allow_pickle=True)
borders=np.load("borders_data.npy", allow_pickle=True)


# if True:
#     ax=plt.figure(figsize=(10, 8)) 
#     utils.read_borders__gen_graph(borders)
# plt.show()


if STR_GRPH_PROJ:
    ax=plt.figure(figsize=(10, 10)) 
    x=[]
    y=[]
    for star in const:
        ra  = star['Right Ascension (deg)']/180*pi
        dec = star['Declination (deg)']/180*np.pi
        v = utils.get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
        x_y_z = utils.upproject(v)
        S,marker,alpha = utils.condition_magnitudes(star,hmg,hmg2)
        plt.scatter(x_y_z[1], x_y_z[0], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha, zorder=3)
        x.append(x_y_z[1])
        y.append(x_y_z[0])
        
    utils.plot_borders_str_grph(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax)
    utils.plot_lines_str_grph(lines,center_Dec_deg,center_ra_deg, zrot_deg, ax)

    # plt.grid()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim([-1,1])
    plt.ylim([-1,1])
    plt.tight_layout(pad=0)
    plt.axis('off')
    plt.margins(0)
    plt.savefig("str_grph_proj.pdf", dpi=DPI, pad_inches=0)
    # plt.savefig("str_grph_proj.png", dpi=DPI, pad_inches=0)
    # plt.show()

if CYLINDRICAL:

    x_realm = [-3.3, 4]
    y_realm = [-1.8, 1.5]
    x_span = abs(x_realm[0]-x_realm[1])
    y_span = abs(y_realm[0]-y_realm[1])
    x_y_scale=x_span/y_span
    base_scale=5

    plt.figure(figsize=(x_y_scale*base_scale, base_scale))

    if 1:
        # print()
        # print(constellations_for_borders_list)
        used_borders_list = []
        for idx,constellation_for_borders in enumerate(constellations_for_borders_list):
            print(f"Borders\t{idx} len: {len(constellations_for_borders_list)}\t{constellation_for_borders}")
            data_file_path=f"{root}/constellations/prev/borders/{constellation_for_borders}.csv"

            borders = csv_read_zodiac.read_lines_csv(data_file_path)
            # print("B")
            
            utils.plot_cylindrical_borders(borders, center_Dec_deg,center_ra_deg,zrot_deg, used_borders_list)
            # print(used_borders_list)
            # print("A")


    if 1:
        # print()
        # print(constellation_line_list)
        for idx,constellation_for_line in enumerate(constellation_line_list):
            print(f"lines\t{idx} len: {len(constellation_line_list)}")
            data_file_path = f"{root}/constellations/prev/{constellation_for_line}.csv"

            data = csv_read_zodiac.read_lines_csv(data_file_path)
            utils.plot_cylindrical_lines(data,center_Dec_deg,center_ra_deg,zrot_deg, Break_line=0.1)

        print()
        print(constellations_for_stars_list)

    if 1:
        DATA=[]
        for idx, constellation_for_stars in enumerate(constellations_for_stars_list):
            print(f"stars\t{idx} len: {len(constellations_for_stars_list)}")
            data_file_path=f"{root}/constellations/prev/{constellation_for_stars}.csv"

            data = csv_read_zodiac.read_csv(data_file_path)
            DATA.append(data)
        utils.plot_cylindrical_stars(DATA,center_Dec_deg,center_ra_deg,zrot_deg,hmg,hmg2,a)


    # plt.xlim([0*np.pi,2.25*np.pi])

    # plt.ylim([-np.pi/2,np.pi/2])

    # for i in range(-6,6):
    #     plt.axvline(i/6*np.pi,linestyle="--",color="gray",linewidth=0.5)
    # for i in range(-3,3):
    #     plt.axhline(i/6*np.pi,linestyle="--",color="gray",linewidth=0.5)

    plt.gca().set_aspect('equal', adjustable='box')
 
    plt.xlim(x_realm)
    plt.ylim(y_realm)
    plt.tight_layout(pad=0)
    plt.axis('off')
    plt.margins(0)
    
    plt.savefig("cylindrical.pdf", dpi=DPI)
    # plt.show()

print("cylindrical DONE")



if POLAR:
    plt.figure(figsize=(10, 8)) 
    ax = plt.subplot(111, projection='polar')

    if 1:
        utils.plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax)

        utils.plot_lines_polar(lines,center_Dec_deg,center_ra_deg, zrot_deg, ax)
        utils.plot_stars_polar(const, center_Dec_deg,center_ra_deg,zrot_deg, ax, hmg, hmg2, a)

        ax.set_ylim(0, np.tan(fov/4/180*np.pi))
        ax.set_yticklabels([])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(False)

        plt.savefig("all.pdf", dpi=DPI)




    plt.figure(figsize=(10, 8)) 
    ax = plt.subplot(111, projection='polar')

    if 0:
        utils.plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax)

        # utils.plot_lines_polar(lines,center_Dec_deg,center_ra_deg, zrot_deg, ax)
        utils.plot_stars_polar(const, center_Dec_deg,center_ra_deg,zrot_deg, ax, hmg, hmg2, a)

        ax.set_ylim(0, np.tan(fov/4/180*np.pi))
        ax.set_yticklabels([])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(False)

    plt.savefig("borders_&_stars.pdf", dpi=DPI)
    

    plt.figure(figsize=(10, 8)) 
    ax = plt.subplot(111, projection='polar')
    if 0:
        # utils.plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax)

        utils.plot_lines_polar(lines,center_Dec_deg,center_ra_deg, zrot_deg, ax)
        utils.plot_stars_polar(const, center_Dec_deg,center_ra_deg,zrot_deg, ax, hmg, hmg2, a)

        ax.set_ylim(0, np.tan(fov/4/180*np.pi))
        ax.set_yticklabels([])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(False)

    plt.savefig("stars_&_lines.pdf", dpi=DPI)


    plt.figure(figsize=(10, 8)) 
    ax = plt.subplot(111, projection='polar')
    if 0:
        utils.plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax)

        # utils.plot_lines_polar(lines,center_Dec_deg,center_ra_deg, zrot_deg, ax)
        # utils.plot_stars_polar(const, center_Dec_deg,center_ra_deg,zrot_deg, ax, hmg, hmg2, a)

        ax.set_ylim(0, np.tan(fov/4/180*np.pi))
        ax.set_yticklabels([])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(False)

    plt.savefig("borders.pdf", dpi=DPI)


    plt.figure(figsize=(10, 8)) 
    ax = plt.subplot(111, projection='polar')
    if 0:
        # utils.plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax)

        # utils.plot_lines_polar(lines,center_Dec_deg,center_ra_deg, zrot_deg, ax)
        utils.plot_stars_polar(const, center_Dec_deg,center_ra_deg,zrot_deg, ax, hmg, hmg2, a)

        ax.set_ylim(0, np.tan(fov/4/180*np.pi))
        ax.set_yticklabels([])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(False)

    plt.savefig("stars.pdf", dpi=DPI)



if SPHERRICAL:
    plt.figure(figsize=(10, 8)) 
    ax = plt.subplot(111, projection='polar')
    for star in const:
        ra  = star['Right Ascension (deg)']/180*pi
        dec = star['Declination (deg)']/180*np.pi
        v = utils.get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
        ra2,dec2 = utils.vector2ra_dec(v)
        S,marker,alpha = utils.condition_magnitudes(star,hmg,hmg2)
        ax.scatter(ra2, np.pi/2-dec2, c="black", marker=marker, s=a*(1+hmg-S), alpha=alpha)
    # plt.grid()
    ax.set_ylim(0, np.pi/2)
    ax.set_yticklabels([])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(False)
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    plt.savefig("sphereical.pdf", dpi=DPI)
    # plt.show()


import shutil
import os

dest = os.path.join("scenarios", scenario)

# Ensure destination directory exists
os.makedirs(dest, exist_ok=True)

files = [
    "cylindrical.pdf",
    "polar_lines.pdf",
    "polar.pdf",
    "sphereical.pdf",
    "str_grph_proj.pdf",
    "all.pdf",
    "stars_&_lines.pdf",
    "borders_&_stars.pdf",
    "borders.pdf",
    "stars.pdf",
]

for f in files:
    target = os.path.join(dest, f)

    try:
        # If file exists at destination, remove it so move can overwrite
        if os.path.exists(target):
            os.remove(target)

        shutil.move(f, target)
        print(f"Moved {f} → {target}")

    except FileNotFoundError:
        print(f"Skipped (missing): {f}")