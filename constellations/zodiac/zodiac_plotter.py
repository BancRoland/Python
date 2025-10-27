import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi
import utils
import argparse
import toml

print("zodiac_plotter.py started")


CONNECT=0

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
lines=np.load("lines_data.npy", allow_pickle=True)

if 0:
    plt.figure(figsize=(10, 8)) 
    x=[]
    y=[]
    for star in const:
        ra  = star['Right Ascension (deg)']/180*pi
        dec = star['Declination (deg)']/180*np.pi
        v = utils.get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
        w = utils.upproject(v)
        S,marker,alpha = utils.condition_magnitudes(star,hmg,hmg2)
        plt.scatter(w[1], w[0], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha)
        x.append(w[1])
        y.append(w[0])
    if 1:
        # plt.plot(x, y, color="black")
        for line in lines:
                    ra1  = line['Right Ascension (deg)1']/180*pi
                    dec1 = line['Declination (deg)1']/180*np.pi
                    ra2  = line['Right Ascension (deg)2']/180*pi
                    dec2 = line['Declination (deg)2']/180*np.pi
                    linestyle = line['linestyle']
                    color = line['color']
                    width = line['width']
                    alpha = line['alpha']

                    v1 = utils.get_transformed_vector(ra1,dec1,center_Dec_deg, center_ra_deg, zrot_deg)
                    w1 = utils.upproject(v1)
                    v2 = utils.get_transformed_vector(ra2,dec2,center_Dec_deg, center_ra_deg, zrot_deg)
                    w2 = utils.upproject(v2)
                    S,marker,alpha = utils.condition_magnitudes(star,hmg,hmg2)
                    # plt.scatter(w[1], w[0], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha)
                    plt.plot([w1[1],w2[1]],[w1[0],w2[0]],linewidth=width,linestyle=linestyle,alpha=alpha,color=color)

    # plt.grid()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig("toprint.png", dpi=500)
    # plt.show()

if 0:
    plt.figure(figsize=(15, 9)) 
    x=[]
    y=[]
    for star in const:
        ra  = star['Right Ascension (deg)']/180*pi
        dec = star['Declination (deg)']/180*np.pi
        v = utils.get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
        w = utils.cylinder_project(v)
        S,marker,alpha = utils.condition_magnitudes(star,hmg,hmg2)
        plt.scatter(w[0], w[1], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha)
        y.append(w[1])
        x.append(w[0])
    if CONNECT:
        # plt.plot(y, x, color="black")
        for i in range(len(x)-1):
            dx = x[i+1] - x[i]
            dy = y[i+1] - y[i]
            plt.arrow(x[i], y[i], dx*1 , dy*1, 
            head_width=0.05, head_length=0.1, fc='red', ec='red', length_includes_head=True)

    plt.xlim([-np.pi,np.pi])
    plt.ylim([-np.pi/2,np.pi/2])
    plt.gca().set_aspect('equal', adjustable='box')
    for i in range(-6,6):
        plt.axvline(i/6*np.pi,linestyle="--",color="gray",linewidth=0.5)
    for i in range(-3,3):
        plt.axhline(i/6*np.pi,linestyle="--",color="gray",linewidth=0.5)

    plt.savefig("toprint2.png", dpi=500)
    # plt.show()

print("toprint2 DONE")


if 0:
    plt.figure(figsize=(15, 9)) 
    x=[]
    y=[]
    for star in const:
        ra  = star['Right Ascension (deg)']
        dec = star['Declination (deg)']
        S,marker,alpha = utils.condition_magnitudes(star,hmg,hmg2)
        plt.scatter(ra, dec, color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha)
        y.append(ra)
        x.append(dec)
    if CONNECT:
        for i in range(len(x)-1):
            dx = x[i+1] - x[i]
            dy = y[i+1] - y[i]
            plt.arrow(y[i], x[i], dy*1 , dx*1, 
            head_width=0.05, head_length=0.1, fc='red', ec='red', length_includes_head=True)

    plt.xlim([-10,370])
    plt.ylim([-180,180])
    # plt.gca().set_aspect('equal', adjustable='box')
    for i in range(0,13):
        plt.axvline(i/6*180,linestyle="--",color="gray",linewidth=0.5)
    for i in range(-6,6):
        plt.axhline(i/6*180,linestyle="--",color="gray",linewidth=0.5)

    plt.savefig("toprint3.png", dpi=500)
    # plt.show()
print("toprint3 DONE")

if 1:
    plt.figure(figsize=(10, 8)) 
    ax = plt.subplot(111, projection='polar')
    x=[]
    y=[]
    for idx,star in enumerate(const):
        print(f"stars:\t{idx/len(const)*100:.2f}%")
        ra  = star['Right Ascension (deg)']/180*pi
        dec = star['Declination (deg)']/180*np.pi
        v = utils.get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
        theta_R = utils.polar_upproject(v)
        S,marker,alpha = utils.condition_magnitudes(star,hmg,hmg2)
        ax.scatter(theta_R[0], theta_R[1], c="black", marker=marker, s=a*(1+hmg-S), alpha=alpha)
        x.append(theta_R[1])
        y.append(theta_R[0])
    if CONNECT:
        plt.plot(y, x, color="black")
    # plt.grid()
    ax.set_ylim(0, np.tan(fov/4/180*np.pi))
    ax.set_yticklabels([])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(False)
    # plt.grid(True)

    plt.savefig("toprint_polar.png", dpi=500)
    # plt.show()

if 1:

    for idx,line in enumerate(lines):
                print(f"lines:\t{idx/len(lines)*100:.2f}%")
                ra1  = line['Right Ascension (deg)1']/180*pi
                dec1 = line['Declination (deg)1']/180*np.pi
                ra2  = line['Right Ascension (deg)2']/180*pi
                dec2 = line['Declination (deg)2']/180*np.pi
                linestyle = line['linestyle']
                color = line['color']
                width = line['width']
                alpha = line['alpha']

                if linestyle==":":
                    ra_diff = (ra2-ra1)
                    if abs(ra_diff)>pi:
                        if ra1<ra2:
                            ra1=ra1+2*pi
                        else:
                            ra1=ra1-2*pi  
                        ra_diff = (ra2-ra1)

                    dec_diff = (dec2-dec1)
                    if abs(dec_diff)>pi:
                        if dec1<dec2:
                            dec1=dec1+2*pi
                        else:
                            dec1=dec1-2*pi   
                        dec_diff = (dec2-dec1)
                    iteration_num = max((np.floor(abs(ra_diff)/(2*np.pi)*360))+1 , (np.floor(abs(dec_diff)/(2*np.pi)*360))+1)

                    ra_step = ra_diff/iteration_num
                    dec_step = dec_diff/iteration_num
                    ra_now = ra1
                    dec_now = dec1


                    for i in range(int(iteration_num)):
                        ra_next = ra_now + ra_step
                        dec_next = dec_now + dec_step

                        v1 = utils.get_transformed_vector(ra_now,dec_now,center_Dec_deg, center_ra_deg, zrot_deg)
                        theta_R1 = utils.polar_upproject(v1)

                        v2 = utils.get_transformed_vector(ra_next,dec_next,center_Dec_deg, center_ra_deg, zrot_deg)
                        theta_R2 = utils.polar_upproject(v2)

                        theta1=theta_R1[0]
                        theta2=theta_R2[0]
                        R1=theta_R1[1]
                        R2=theta_R2[1]
                        ax.plot([theta1,theta2],[R1,R2],linewidth=0.5,linestyle="-",alpha=1,color=color)

                        ra_now = ra_next
                        dec_now = dec_next

                else:
                    v1 = utils.get_transformed_vector(ra1,dec1,center_Dec_deg, center_ra_deg, zrot_deg)
                    theta_R1 = utils.polar_upproject(v1)

                    v2 = utils.get_transformed_vector(ra2,dec2,center_Dec_deg, center_ra_deg, zrot_deg)
                    theta_R2 = utils.polar_upproject(v2)

                    theta1=theta_R1[0]
                    theta2=theta_R2[0]
                    R1=theta_R1[1]
                    R2=theta_R2[1]
                    ax.plot([theta1,theta2],[R1,R2],linewidth=width,linestyle=linestyle,alpha=1,color=color)
                                 

    plt.savefig("toprint_polar_lines.png", dpi=500)



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


