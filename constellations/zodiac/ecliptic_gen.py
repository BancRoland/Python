import utils
import numpy as np

v_list=[]

equinox_point = utils.get_3d_vec_from_RaDec(ra=0, dec=0)


for i in np.arange(0,24,0.25):
    time_rot = utils.zrot(equinox_point,i/24*360)
    space_rot= utils.xrot(time_rot,-23.44)

    v_list.append(space_rot)

    radec_val = utils.get_RaDec_from_3dVector(space_rot)


print("Name,Right Ascension,Declination,Apparent Magnitude,Constellation")
for v in v_list:
    ra,dec = utils.get_RaDec_from_3dVector(v)
    ra_sex = utils.Sexagesimal.from_hourDeg_to_Sexagesimal(ra)
    dec_sex = utils.Sexagesimal.from_hourDeg_to_Sexagesimal(dec)
    hourMinSec = ra_sex.get_string__hour_sec_min()
    degMinSec = dec_sex.get_string__deg_min_sec()

    # # tavasz,00h 00m 00.00s,+00° 00′ 00″,0,Ecliptic, nyar,06h 00m 00.00s,+23° 30′ 00.0″,0,Ecliptic,-,grey,1,0.5
    print(f"point,{hourMinSec},{degMinSec},5,Ecliptic")


