import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi
import utils
import argparse
import toml

# Path to the TOML file
toml_file = "variables.toml"

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

# center_Dec_deg0  = args.declination_deg0
# center_Dec_degmin  = args.declination_degmin
# center_Dec_degsec  = args.declination_degsec
# center_ra_hour  = args.rectascension_hour
# center_ra_min   = args.rectascension_min
# center_ra_sec   = args.rectascension_sec

center_ra_deg=((center_ra_hour+center_ra_min/60+center_ra_sec/60/60)/24)*360
center_Dec_deg=center_Dec_deg0+center_Dec_degmin/60+center_Dec_degsec/60/60

# zrot_deg = args.zrot

a       = args.a
hmg     = args.hmg
hmg2    = args.hmg2

const=np.load("stars_test.npy", allow_pickle=True)

if 1:
    plt.figure(figsize=(10, 8)) 
    for star in const:
        ra  = star['Right Ascension (deg)']/180*pi
        dec = star['Declination (deg)']/180*np.pi
        v = utils.get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
        w = utils.upproject(v)
        S,marker,alpha = utils.condition_magnitudes(star,hmg,hmg2)
        plt.scatter(w[1], w[0], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha)
    # plt.grid()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig("toprint.png", dpi=500)
    # plt.show()

if 1:
    plt.figure(figsize=(15, 9)) 
    for star in const:
        ra  = star['Right Ascension (deg)']/180*pi
        dec = star['Declination (deg)']/180*np.pi
        v = utils.get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
        w = utils.cylinder_project(v)
        S,marker,alpha = utils.condition_magnitudes(star,hmg,hmg2)
        plt.scatter(w[0], w[1], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha)
    plt.xlim([-np.pi,np.pi])
    plt.ylim([-np.pi/2,np.pi/2])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig("toprint2.png", dpi=500)
    # plt.show()


plt.figure(figsize=(10, 8)) 
ax = plt.subplot(111, projection='polar')
for star in const:
    ra  = star['Right Ascension (deg)']/180*pi
    dec = star['Declination (deg)']/180*np.pi
    v = utils.get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
    theta_R = utils.polar_upproject(v)
    S,marker,alpha = utils.condition_magnitudes(star,hmg,hmg2)
    # plt.scatter(w[1], w[0], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha)
    ax.scatter(theta_R[0], theta_R[1], c="black", marker=marker, s=a*(1+hmg-S), alpha=alpha)
# plt.grid()
ax.set_ylim(0, np.tan(fov/4/180*np.pi))
ax.set_yticklabels([])
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(False)
plt.savefig("toprint_polar.png", dpi=500)
# plt.show()


# plt.figure(figsize=(10, 8)) 
# ax = plt.subplot(111, projection='polar')
# for star in const:
#     ra  = star['Right Ascension (deg)']/180*pi
#     dec = star['Declination (deg)']/180*np.pi
#     v = utils.get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
#     ra2,dec2 = utils.vector2ra_dec(v)
#     S,marker,alpha = utils.condition_magnitudes(star,hmg,hmg2)
#     ax.scatter(ra2, np.pi/2-dec2, c="black", marker=marker, s=a*(1+hmg-S), alpha=alpha)
# # plt.grid()
# ax.set_ylim(0, np.pi/2)
# ax.set_yticklabels([])
# plt.gca().set_aspect('equal', adjustable='box')
# plt.grid(False)
# ax.set_theta_direction(-1)
# ax.set_theta_zero_location('N')
# plt.savefig("toprint_polar2.png", dpi=500)
# plt.show()