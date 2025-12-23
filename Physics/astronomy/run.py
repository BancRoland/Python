import numpy as np
from dataclasses import dataclass
import sys
import os
home_directory = os.path.expanduser("~")
sys.path.append(home_directory+"/Desktop/Python/math/matrices/Rodrigues_rot")

import banc_vectorManip as vMp
import matplotlib.pyplot as plt

@dataclass
class coordinates:
    azimuth_like: float = 0
    elevation_like: float = 0

    def azimuth_like_setter(self, azimuth_deg: float):
        if azimuth_deg > 360.0 or azimuth_deg < 0.0:
            raise ValueError ("invalid elevation value")
        self.azimuth_like = azimuth_deg

    def elevation_like_setter(self,elevation_deg: float):
        if elevation_deg > 90.0 or elevation_deg < -90.0:
            raise ValueError ("invalid elevation value")
        self.elevation_like = elevation_deg

    def print(self):
        print(f"{self.azimuth_like} , {self.elevation_like}")



@dataclass
class time_format:
    date: int = 0
    hour: int = 0
    min: int = 0
    sec: float = 0.0

    def get_secs_of_year(self):
        out = self.date*86400 + self.hour*3600 + self.min*60 + self.sec
        return out
    
    def process_of_year(self):
        return self.get_secs_of_year()/(365.25*86400)
    
    def print(self):
        print(f"{self.date:3.0f} d {self.hour:2.0f} h {self.min:2.0f} min {self.sec:2.3} sec")
    


@dataclass
class geological_pos:
    _coord = coordinates()
    latitude = _coord.azimuth_like
    longitude = _coord.elevation_like

    def latitude_setter(self, latitude_deg: float):
        self._coord.azimuth_like_setter(latitude_deg)
        self.latitude = self._coord.azimuth_like

    def longitude_setter(self, longitude_deg: float):
        self._coord.elevation_like_setter(longitude_deg)
        self.longitude = self._coord.elevation_like

def deg_2_time(angle_deg :float)->time_format:
    angle_in_hour  = angle_deg/360*24

    hour = int(angle_in_hour)
    min = int((angle_in_hour-hour)*60)
    sec = (angle_in_hour-hour-min/60)*60*60
    out = time_format(0,hour,min,sec)
    return out


class equatorial_coord:
    _coord = coordinates()
    rectascense_deg = _coord.azimuth_like
    rectascense_time : time_format = deg_2_time(rectascense_deg)

    declination_deg = _coord.elevation_like

    def rectascense_setter(self, rectascense_deg: float):
        self._coord.azimuth_like_setter(rectascense_deg)
        self.rectascense_deg = self._coord.azimuth_like
        self.rectascense_time = deg_2_time(self.rectascense_deg)

    def declination_setter(self, declination_deg: float):
        self._coord.elevation_like_setter(declination_deg)
        self.declination_deg = self._coord.elevation_like

    def __init__(self,rectascense_deg, declination_deg):
        self.rectascense_setter(rectascense_deg)
        self.declination_setter(declination_deg)

    def print(self):
        print(f"rectascence_deg: {self.rectascense_deg}, rectascence_time:")
        deg_2_time(self.rectascense_deg).print()
        print(f"declination: {self.declination_deg}\n")



@dataclass
class ecliptic_coord:
    _coord = coordinates()
    latitude = _coord.azimuth_like
    longitude = _coord.elevation_like


    def latitude_setter(self, latitude_deg: float):
        self._coord.azimuth_like_setter(latitude_deg)
        self.latitude = self._coord.azimuth_like

    def longitude_setter(self, longitude_deg: float):
        self._coord.elevation_like_setter(longitude_deg)
        self.longitude = self._coord.elevation_like

    def __init__(self,latitude_deg, longitude_deg):
        self.latitude_setter(latitude_deg)
        self.longitude_setter(longitude_deg)


@dataclass
class horizontal_coord:
    _coord = coordinates()
    azimuth = _coord.azimuth_like
    elevation = _coord.elevation_like

    def azimuth_setter(self, azimuth_deg: float):
        self._coord.azimuth_like_setter(azimuth_deg)
        self.azimuth = self._coord.azimuth_like

    def elevation_setter(self, elevation_deg: float):
        self._coord.elevation_like_setter(elevation_deg)
        self.elevation = self._coord.elevation_like
        




def get_sun_pos_in_ecliptic_coordinates(time: time_format)->ecliptic_coord:

    deg_from_time = 360*time.process_of_year()
    latitude = (deg_from_time)%360
    
    coord = ecliptic_coord(0,0)
    coord.longitude_setter(0)
    coord.latitude_setter(latitude)

    return coord

@dataclass
class descates_vector():
    V = np.array([0,0,0])

    x: float = 0
    y: float = 0
    z: float = 0

    def setter(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.V = np.array([x,y,z])

    def print(self):
        print(f"{self.x}, {self.y}, {self.z}")

def cosd(alpha_deg):
    alpha_rad=alpha_deg/180*np.pi
    return(np.cos(alpha_rad))

def sind(alpha_deg):
    alpha_rad=alpha_deg/180*np.pi
    return(np.sin(alpha_rad))

AXIAL_TILT = 23.5
def get_vector_form_ecliptic_coordinates(coord: ecliptic_coord)->descates_vector:
    # tavaszpont: [1,0,0]
    # ekliptikus észak: [0,0,1]
    V = descates_vector()


    
    # print("attrib val:")
    # print(coord._coord.print())
    # print("azmt-like, eleV_like")
    # print(coord._coord.azimuth_like)
    # print(coord._coord.elevation_like)
    # print("lat-lon")
    # print(coord.latitude)
    # print(coord.longitude)
    # print("cosd")
    # print(cosd(coord.longitude))
    
    x = cosd(coord.longitude)*cosd(coord.latitude)
    # print(f"x = {x}")
    y = cosd(coord.longitude)*sind(coord.latitude)
    # print(f"y = {y}")
    z = sind(coord.longitude)
    # print(f"z = {z}")

    V.setter(x,y,z)

    # print("x,y,z:")
    # V.print()

    return V

def get_equatorial_from_vector(vector: descates_vector)->equatorial_coord:
    rectascension = np.arctan2(vector.y,vector.x)/np.pi*180
    rectascension = (rectascension+360)%360

    declination = np.arcsin(vector.z)/np.pi*180
    # declination = (declination+360)%360

    equatorial_coord0 = equatorial_coord(rectascense_deg=rectascension, declination_deg=declination)
    return equatorial_coord0

def rotate_vector(vector: descates_vector, axis: descates_vector, alpha_deg: float):
    vector  = np.array([vector.x,vector.y,vector.z])
    axis    = np.array([axis.x,axis.y,axis.z])

    rotated_vector = vMp.ROT(vector, axis, alpha_deg/180*np.pi)
    out = descates_vector(rotated_vector[0], rotated_vector[1], rotated_vector[2])
    return out

def get_sun_pos_in_equatorial_coordinates(time: time_format)->equatorial_coord:
    sun_ecliptic_coord = get_sun_pos_in_ecliptic_coordinates(time= time)   
    sun_vector_ecliptic = get_vector_form_ecliptic_coordinates(sun_ecliptic_coord)

    equinox_ecliptic_coord = ecliptic_coord(0,0)
    equinox_vector_ecliptic = get_vector_form_ecliptic_coordinates(equinox_ecliptic_coord)
    
    sun_vector_equatorial = rotate_vector(sun_vector_ecliptic, equinox_vector_ecliptic, AXIAL_TILT)
    sun_equatorial = get_equatorial_from_vector(sun_vector_equatorial)
    return sun_equatorial



    rectascension = np.arctan2(vector.y,vector.x)/np.pi*180
    rectascension = (rectascension+360)%360

    declination = np.arcsin(vector.z)/np.pi*180
    # declination = (declination+360)%360

    equatorial_coord0 = equatorial_coord(rectascense_deg=rectascension, declination_deg=declination)
    return equatorial_coord0

def get_vector_form_equatorial(equatorial_coordinates: equatorial_coord):
    V = descates_vector()
    V.z=sind(equatorial_coordinates.declination_deg)
    shadow=cosd(equatorial_coordinates.declination_deg)
    V.x = shadow*cosd(equatorial_coordinates.rectascense_deg)
    V.y = shadow*sind(equatorial_coordinates.rectascense_deg)
    return V

def equat_2_horiz(equatorial_coordinates: equatorial_coord, time: time_format)->horizontal_coord:
    V = get_vector_form_equatorial(equatorial_coordinates)

    out = horizontal_coord
    out.elevation_setter(equatorial_coordinates.declination_deg)
    out.azimut_setter(0)

    V.declination

# def equat_2_horiz(V: equatorial_coord, geological_pos: geological_pos, time: time_format):
#     equat_2_horiz_on_north_pole(V,time)

# def get_sun_pos_in_horizontal_coordinates(time_sec: float, geological_pos: geological_pos)->horizontal_coord:
#     V = get_sun_pos_in_equatorial_coordinates(time_sec)
#     out = equat_2_horiz(V, geological_pos)
#     return out

if __name__:
    
    for d in range(0,360,30):
        time = time_format(date=d)
        print(f"\n\ndate = {d}")
        A= get_sun_pos_in_equatorial_coordinates(time)
        A.print()
        plt.scatter(A.rectascense_deg, A.declination_deg)

# plt.show()



