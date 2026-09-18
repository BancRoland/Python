import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi
import utils
import argparse
import toml
import time
import csv_read_zodiac



def print_cyl(constellations_for_borders_list, 
              center_Dec_deg, 
              root, 
              center_ra_deg, 
              zrot_deg, 
              constellation_line_list,
              constellations_for_stars_list,
              hmg,
              hmg2,
              a,
              DPI):

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
        for idx,constellation_for_line in enumerate(constellation_line_list):
            print(f"lines\t{idx} len: {len(constellation_line_list)}")
            data_file_path = f"{root}/constellations/prev/{constellation_for_line}.csv"

            data = csv_read_zodiac.read_lines_csv(data_file_path)
            utils.plot_cylindrical_lines(data,center_Dec_deg,center_ra_deg,zrot_deg, Break_line=0.1)


    if 1:
        DATA=[]
        for idx, constellation_for_stars in enumerate(constellations_for_stars_list):
            print(f"stars\t{idx} len: {len(constellations_for_stars_list)}")
            data_file_path=f"{root}/constellations/prev/{constellation_for_stars}.csv"

            data = csv_read_zodiac.read_stars_csv(data_file_path)
            DATA.append(data)
        utils.plot_cylindrical_stars(DATA,center_Dec_deg,center_ra_deg,zrot_deg,hmg,hmg2,a)


    if 1:
        DATA=[]

        data_file_path=f"{root}/constellations/prev/ecliptic.csv"
        data = csv_read_zodiac.read_stars_csv(data_file_path)
        DATA.append(data)
        utils.plot_cylindrical_ecliptic(DATA,center_Dec_deg,center_ra_deg,zrot_deg,hmg,hmg2,a)

        DATA=[]

        data_file_path=f"{root}/constellations/prev/eqinox.csv"
        data = csv_read_zodiac.read_stars_csv(data_file_path)
        DATA.append(data)
        utils.plot_cylindrical_equinox(DATA,center_Dec_deg,center_ra_deg,zrot_deg,hmg,hmg2,a)


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
    
    # plt.savefig("cylindrical.pdf", dpi=DPI)
    plt.savefig("cylindrical.pdf", dpi=DPI, bbox_inches='tight', pad_inches=0)

    # plt.show()



