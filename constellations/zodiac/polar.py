import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi
import utils
import argparse
import toml
import time
import csv_read_zodiac

PRINT_STARS = False
PRINT_LINES = False
PRINT_BORDERS = True



def print_pol(constellations_for_borders_list, 
              center_Dec_deg, 
              root, 
              center_ra_deg, 
              zrot_deg, 
              constellation_line_list,
              constellations_for_stars_list,
              hmg,
              hmg2,
              a,
              DPI,
              fov
              ):

    # x_realm = [-3.3, 4]
    # y_realm = [-1.8, 1.5]
    # x_span = abs(x_realm[0]-x_realm[1])
    # y_span = abs(y_realm[0]-y_realm[1])
    # x_y_scale=x_span/y_span
    # base_scale=5

    plt.figure(figsize=(10, 8)) 
    ax = plt.subplot(111, projection='polar')

    if PRINT_BORDERS:
        # print()
        # print(constellations_for_borders_list)
        used_borders_list = []
        for idx,constellation_for_borders in enumerate(constellations_for_borders_list):
            print(f"Borders\t{idx} len: {len(constellations_for_borders_list)}\t{constellation_for_borders}")
            data_file_path=f"{root}/constellations/prev/borders/{constellation_for_borders}.csv"

            borders = csv_read_zodiac.read_lines_csv(data_file_path)
            # print("B")
            
            # utils.plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, used_borders_list)
            utils.plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax)
            # print(used_borders_list)
            # print("A")


    if PRINT_LINES:
        for idx,constellation_for_line in enumerate(constellation_line_list):
            print(f"lines\t{idx} len: {len(constellation_line_list)}")
            data_file_path = f"{root}/constellations/prev/{constellation_for_line}.csv"

            lines = csv_read_zodiac.read_lines_csv(data_file_path)
            # utils.plot_lines_polar(lines,center_Dec_deg,center_ra_deg,zrot_deg, Break_line=0.1)
            utils.plot_lines_polar(lines, center_Dec_deg,center_ra_deg,zrot_deg, ax)


    if PRINT_STARS:
        DATA=[]
        for idx, constellation_for_stars in enumerate(constellations_for_stars_list):
            print(f"stars\t{idx} len: {len(constellations_for_stars_list)}")
            data_file_path=f"{root}/constellations/prev/{constellation_for_stars}.csv"

            data = csv_read_zodiac.read_csv(data_file_path)
            DATA.append(data)
        # utils.plot_stars_polar(DATA,center_Dec_deg,center_ra_deg,zrot_deg,hmg,hmg2,a)
        utils.plot_stars_polar(DATA,center_Dec_deg,center_ra_deg,zrot_deg,hmg,hmg2,a)





    # plt.xlim([0*np.pi,2.25*np.pi])

    # plt.ylim([-np.pi/2,np.pi/2])

    # for i in range(-6,6):
    #     plt.axvline(i/6*np.pi,linestyle="--",color="gray",linewidth=0.5)
    # for i in range(-3,3):
    #     plt.axhline(i/6*np.pi,linestyle="--",color="gray",linewidth=0.5)

    plt.gca().set_aspect('equal', adjustable='box')
 

    # ax.set_ylim(0, np.tan(fov/4/180*np.pi))
    # ax.set_yticklabels([])
    # # plt.tight_layout(pad=0)
    # plt.axis('off')
    # # plt.margins(0)


    ax.set_ylim(0, np.tan(fov/4/180*np.pi))
    ax.set_yticklabels([])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(False)
    
    # plt.savefig("cylindrical.pdf", dpi=DPI)
    # plt.savefig("polar_trying_best.pdf", dpi=DPI, bbox_inches='tight', pad_inches=0)
    plt.savefig("polar_trying_best.png", dpi=DPI, bbox_inches='tight', pad_inches=0)


    # plt.show()









# plt.figure(figsize=(10, 8)) 
#     ax = plt.subplot(111, projection='polar')

#     if 1:
#         utils.plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax)

#         utils.plot_lines_polar(lines,center_Dec_deg,center_ra_deg, zrot_deg, ax)
#         utils.plot_stars_polar(const, center_Dec_deg,center_ra_deg,zrot_deg, ax, hmg, hmg2, a)

#         ax.set_ylim(0, np.tan(fov/4/180*np.pi))
#         ax.set_yticklabels([])
#         plt.gca().set_aspect('equal', adjustable='box')
#         plt.grid(False)

#         plt.savefig("all.pdf", dpi=DPI)




#     plt.figure(figsize=(10, 8)) 
#     ax = plt.subplot(111, projection='polar')

#     if 0:
#         utils.plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax)

#         # utils.plot_lines_polar(lines,center_Dec_deg,center_ra_deg, zrot_deg, ax)
#         utils.plot_stars_polar(const, center_Dec_deg,center_ra_deg,zrot_deg, ax, hmg, hmg2, a)

#         ax.set_ylim(0, np.tan(fov/4/180*np.pi))
#         ax.set_yticklabels([])
#         plt.gca().set_aspect('equal', adjustable='box')
#         plt.grid(False)

#     plt.savefig("borders_&_stars.pdf", dpi=DPI)
    

#     plt.figure(figsize=(10, 8)) 
#     ax = plt.subplot(111, projection='polar')
#     if 0:
#         # utils.plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax)

#         utils.plot_lines_polar(lines,center_Dec_deg,center_ra_deg, zrot_deg, ax)
#         utils.plot_stars_polar(const, center_Dec_deg,center_ra_deg,zrot_deg, ax, hmg, hmg2, a)

#         ax.set_ylim(0, np.tan(fov/4/180*np.pi))
#         ax.set_yticklabels([])
#         plt.gca().set_aspect('equal', adjustable='box')
#         plt.grid(False)

#     plt.savefig("stars_&_lines.pdf", dpi=DPI)


#     plt.figure(figsize=(10, 8)) 
#     ax = plt.subplot(111, projection='polar')
#     if 0:
#         utils.plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax)

#         # utils.plot_lines_polar(lines,center_Dec_deg,center_ra_deg, zrot_deg, ax)
#         # utils.plot_stars_polar(const, center_Dec_deg,center_ra_deg,zrot_deg, ax, hmg, hmg2, a)

#         ax.set_ylim(0, np.tan(fov/4/180*np.pi))
#         ax.set_yticklabels([])
#         plt.gca().set_aspect('equal', adjustable='box')
#         plt.grid(False)

#     plt.savefig("borders.pdf", dpi=DPI)


#     plt.figure(figsize=(10, 8)) 
#     ax = plt.subplot(111, projection='polar')
#     if 0:
#         # utils.plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax)

#         # utils.plot_lines_polar(lines,center_Dec_deg,center_ra_deg, zrot_deg, ax)
#         utils.plot_stars_polar(const, center_Dec_deg,center_ra_deg,zrot_deg, ax, hmg, hmg2, a)

#         ax.set_ylim(0, np.tan(fov/4/180*np.pi))
#         ax.set_yticklabels([])
#         plt.gca().set_aspect('equal', adjustable='box')
#         plt.grid(False)

#     plt.savefig("stars.pdf", dpi=DPI)