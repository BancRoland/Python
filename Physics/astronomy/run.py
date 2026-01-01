import numpy as np
from dataclasses import dataclass, field
import sys
import os
home_directory = os.path.expanduser("~")
sys.path.append(home_directory+"/Desktop/Python/math/matrices/Rodrigues_rot")

import banc_vectorManip as vMp
import matplotlib.pyplot as plt
import csv_read




@dataclass
class AngleDegree:
    positive_sign: bool = True
    degree: int = 0
    minute: int = 0
    second: float = 0.0

    def as_float(self) -> float:
        out = self.degree + self.minute/60 + self.second/60/60
        if self.positive_sign == False:
            out=-1*out
        return out
    
    def as_radian(self) -> float:
        deg = self.as_float()
        rad=deg/180*np.pi
        return rad
    

    @classmethod
    def from_float(cls, angle_deg: float) -> "AngleDegree":
        positive_sign = False if angle_deg < 0 else True
        angle_deg = abs(angle_deg)

        degree = int(angle_deg)
        remaining_minutes = (angle_deg - degree) * 60
        minute = int(remaining_minutes)
        second = (remaining_minutes - minute) * 60

        return cls(positive_sign, degree, minute, second)


    def __add__(self, other) -> "AngleDegree":
        if isinstance(other, AngleDegree):
            return AngleDegree.from_float(self.as_float() + other.as_float())
        elif isinstance(other, (int, float)):
            return AngleDegree.from_float(self.as_float() + other)
        return NotImplemented



@dataclass
class coordinates:
    _azimuth_like: AngleDegree = field(default_factory=AngleDegree)
    _elevation_like: AngleDegree = field(default_factory=AngleDegree)

    @property
    def azimuth_like(self) -> AngleDegree:
        return self._azimuth_like

    @azimuth_like.setter
    def azimuth_like(self, value: AngleDegree):
        azimuth_deg = value.as_float()
        if azimuth_deg >= 0.0 and azimuth_deg <= 360.0:
            self._azimuth_like = value
        else:
            raise ValueError("invalid azimuth")
        
    @property
    def elevation_like(self)->AngleDegree:
        return self._elevation_like
    
    @elevation_like.setter
    def elevation_like(self, value : AngleDegree):
        elevation_deg = value.as_float()
        if elevation_deg >=-90 and elevation_deg <= 90:
            self._elevation_like = value
        else:
            raise ValueError("invalid elevation")

    def __str__(self):
        return(f"_azimuth like: {self.azimuth_like}\nelevation_like: {self.elevation_like}")




@dataclass
class time_format:
    date: int = 0
    hour: int = 0
    min: int = 0
    sec: float = 0.0


    def get_sec_from_date(self):
        out = self.date*86400 + self.hour*3600 + self.min*60 + self.sec
        return out
    
    def process_of_year(self):
        return self.get_sec_from_date()/(365.25*86400)
    
    def get_date_from_sec(sec:float):
        out = time_format()

        out.date = int(sec/60/60/24)
        remain_sec = sec-out.date*60*60*24

        out.hour = int(remain_sec/60/60)
        remain_sec = remain_sec - out.hour*60*60

        out.min = int(remain_sec/60)
        remain_sec = remain_sec - out.min*60

        out.sec = remain_sec

        return out

    def get_day_from_time(self):
        return time_format(date=0, hour=self.hour, min=self.min, sec=self.sec)
    
    def __str__(self):
        return(f"{self.date:3} d {self.hour:2} h {self.min:2} min {self.sec:2.3f} sec")
    
    def __add__(self, other: "time_format")->"time_format":
        return_time = time_format.get_date_from_sec(self.get_sec_from_date() + other.get_sec_from_date())
        return return_time

    


@dataclass
class geological_pos:
    _coord: coordinates = field(default_factory=coordinates)

    @property
    def latitude(self) -> AngleDegree:
        return self._coord.elevation_like
    
    @property
    def longitude(self) -> AngleDegree:
        return self._coord.azimuth_like
    
    @latitude.setter
    def latitude(self, value: AngleDegree):
        self._coord.elevation_like = value

    @longitude.setter
    def longitude(self, value: AngleDegree):
        self._coord.azimuth_like = value



def deg_2_time(angle :AngleDegree)->time_format:
    angle_deg = angle.as_float()
    angle_in_hour  = angle_deg/360*24

    hour = int(angle_in_hour)
    min = int((angle_in_hour-hour)*60)
    sec = (angle_in_hour-hour-min/60)*60*60
    out = time_format(0,hour,min,sec)
    return out


class equatorial_coord:

    def __init__(self,rectascense_deg: AngleDegree = AngleDegree(), declination_deg: AngleDegree = AngleDegree()):
        self._coord = coordinates()
        self.rectascense = rectascense_deg
        self.declination = declination_deg


    @property
    def rectascense(self) -> AngleDegree:
        return self._coord.azimuth_like

    @rectascense.setter
    def rectascense(self, value: AngleDegree):
        self._coord.azimuth_like = value

    @property
    def rectascense_time(self) -> time_format:
        return deg_2_time(self.rectascense)

    @property
    def declination(self) -> AngleDegree:
        return self._coord.elevation_like

    @declination.setter
    def declination(self, value: AngleDegree):
        self._coord.elevation_like = value


    def __str__(self):
        return(f"\nEQ rectascence_deg: {self.rectascense}\nEQ declination: {self.declination}\n")



class EclipticCoord:
    def __init__(self, latitude: AngleDegree, longitude: AngleDegree):
        # Create the underlying coordinates object
        self._coord = coordinates()
        
        # Use property setters to initialize values (ensures validation)
        self.latitude = latitude
        self.longitude = longitude

    # ---------- Latitude property ----------
    @property
    def latitude(self) -> AngleDegree:
        return self._coord.elevation_like

    @latitude.setter
    def latitude(self, value: AngleDegree):
        # Use the Coordinates class setter (or property)
        self._coord.elevation_like = value

    # ---------- Longitude property ----------
    @property
    def longitude(self) -> AngleDegree:
        return self._coord.azimuth_like

    @longitude.setter
    def longitude(self, value: AngleDegree):
        # Use the Coordinates class setter (or property)
        self._coord.azimuth_like = value

    def __str__(self)->str:
        return f"\nEC latitude = {self.latitude}\nEC longitude = {self.longitude}\n"





@dataclass
class horizontal_coord:
    _coord: coordinates = field(default_factory=coordinates)

    @property
    def azimuth(self) -> AngleDegree:
        return self._coord.azimuth_like
    
    @property
    def elevation(self) -> AngleDegree:
        return self._coord.elevation_like

    @azimuth.setter
    def azimuth(self, value: AngleDegree):
        self._coord.azimuth_like = value

    @elevation.setter
    def elevation(self, value: AngleDegree):
        self._coord.elevation_like = value
        

    def __str__(self):
        return (f"azmt:\t{self.azimuth},\telev:\t{self.elevation}")

def get_eot_from_date(date: time_format)->time_format:
    EOT_TABLE0=csv_read.getEOT_csv()
    EOT_TABLE=np.concatenate((EOT_TABLE0[80::],EOT_TABLE0[:80:]))

    idx=int(date.date)%365
    out = time_format.get_date_from_sec(EOT_TABLE[idx])
    return out


def get_sun_pos_in_ecliptic_coordinates(time: time_format, 
                                        sun_ecliptic_longitude_time_diff_for_eot:time_format=time_format())->EclipticCoord:

    time = time + sun_ecliptic_longitude_time_diff_for_eot

    deg_from_time = 360*time.process_of_year()
    longitude_deg = (deg_from_time)%360

    longitude = AngleDegree.from_float(longitude_deg)
    
    coord = EclipticCoord(AngleDegree(0),AngleDegree(0))
    coord.longitude = longitude
    coord.latitude = AngleDegree(0)

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


    def __str__(self):
        return (f"{self.x}, {self.y}, {self.z}")

def cosd(alpha: AngleDegree):
    alpha_rad=alpha.as_radian()
    return(np.cos(alpha_rad))

def sind(alpha: AngleDegree):
    alpha_rad=alpha.as_radian()
    return(np.sin(alpha_rad))

def arcsind(a):
    if a > 1 or a <-1:
        raise ValueError("trigonometrical error")
    out_rad = np.arcsin(a)
    out_deg = out_rad/np.pi*180
    return(out_deg)

def arccosd(a):
    if a > 1 or a <-1:
        raise ValueError("trigonometrical error")
    out_rad = np.arccos(a)
    out_deg = out_rad/np.pi*180
    return(out_deg)

AXIAL_TILT = 23.5
def get_vector_form_ecliptic_coordinates(coord: EclipticCoord)->descates_vector:
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
    
    x = cosd(coord.latitude)*cosd(coord.longitude)
    # print(f"x = {x}")
    y = cosd(coord.latitude)*sind(coord.longitude)
    # print(f"y = {y}")
    z = sind(coord.latitude)
    # print(f"z = {z}")

    V.setter(x,y,z)

    # print("x,y,z:")
    # V.print()

    return V

def get_equatorial_from_vector(vector: descates_vector)->equatorial_coord:
    rectascension = np.arctan2(vector.y,vector.x)/np.pi*180
    rectascension = (rectascension+360)%360
    rectascension_angle = AngleDegree().from_float(rectascension)

    declination = np.arcsin(vector.z)/np.pi*180
    declination_angle = AngleDegree().from_float(declination)

    equatorial_coord0 = equatorial_coord()
    equatorial_coord0.declination = declination_angle
    equatorial_coord0.rectascense = rectascension_angle

    return equatorial_coord0


def rotate_vector(vector: descates_vector, axis: descates_vector, alpha_deg: float):
    vector  = np.array([vector.x,vector.y,vector.z])
    axis    = np.array([axis.x,axis.y,axis.z])

    rotated_vector = vMp.ROT(vector, axis, alpha_deg/180*np.pi)
    out = descates_vector(rotated_vector[0], rotated_vector[1], rotated_vector[2])
    return out

def get_sun_pos_in_equatorial_coordinates(time: time_format, 
                                          sun_ecliptic_longitude_time_diff_for_eot:time_format=time_format()
                                          )->equatorial_coord:
    sun_ecliptic_coord = get_sun_pos_in_ecliptic_coordinates(time= time, 
                                                             sun_ecliptic_longitude_time_diff_for_eot = sun_ecliptic_longitude_time_diff_for_eot)   
    sun_vector_ecliptic = get_vector_form_ecliptic_coordinates(sun_ecliptic_coord)

    equinox_ecliptic_coord = EclipticCoord(AngleDegree(), AngleDegree())
    equinox_vector_ecliptic = get_vector_form_ecliptic_coordinates(equinox_ecliptic_coord)
    
    sun_vector_equatorial = rotate_vector(sun_vector_ecliptic, equinox_vector_ecliptic, AXIAL_TILT)
    sun_equatorial = get_equatorial_from_vector(sun_vector_equatorial)
    return sun_equatorial




def get_vector_form_equatorial(equatorial_coordinates: equatorial_coord):
    V = descates_vector()
    V.z=sind(equatorial_coordinates.declination)
    shadow=cosd(equatorial_coordinates.declination)
    V.x = shadow*cosd(equatorial_coordinates.rectascense)
    V.y = shadow*sind(equatorial_coordinates.rectascense)
    return V

def get_horizontal_from_vector(V:descates_vector):
    out = horizontal_coord()
    out.elevation = AngleDegree(degree=arcsind(V.z))
    out.azimuth = AngleDegree(degree=((np.arctan2(-V.y,V.x)/np.pi*180)+360)%360)
    return out

def equat_2_horiz(equatorial_coordinates: equatorial_coord, time: time_format, utc_plus:time_format, geo_pos: geological_pos)->horizontal_coord:
    rotational_axis     = descates_vector(0,0,1)
    solar_day           = time_format(0,hour = 24)
    siderical_year      = time_format(date=365,hour=6,min=9,sec=10)

    def replus(a,b):
        return((a*b)/(a+b))
    
    siderical_day:time_format = time_format.get_date_from_sec(replus(solar_day.get_sec_from_date(),siderical_year.get_sec_from_date()))

    rotations_by_date = time.get_sec_from_date()/siderical_day.get_sec_from_date()
    longitude_deg = geo_pos.longitude.as_float()

    utc_plus_sec = utc_plus.get_sec_from_date()
    utc_plus_sec_deg = utc_plus_sec/siderical_day.get_sec_from_date()*360.0

    rotations_deg = rotations_by_date*360 - longitude_deg + utc_plus_sec_deg

    V = get_vector_form_equatorial(equatorial_coordinates)

    W = rotate_vector(V,rotational_axis,-rotations_deg)

    latitude_axis = descates_vector(0,1,0)
    latitude_deg = geo_pos.latitude.as_float()

    WW = rotate_vector(W,latitude_axis,90-latitude_deg)

    out = get_horizontal_from_vector(WW)

    return out

def find_sun_set_time(date: time_format, 
                      utc_plus: time_format, 
                      pos: geological_pos, 
                      time_resolution: float=60, 
                      sunset: bool = True)->time_format:
    time_step = time_format(0,12,0,0)
    test_time = date + time_step
    if not is_the_sun_up(test_time,utc_plus,pos):
        raise Exception(f"sun is not over the horizont at {test_time}")
    
    if sunset:
        set_or_rise_multiplier = 1
    else:
        set_or_rise_multiplier = -1

        
    while time_step.get_sec_from_date() >= time_resolution:

        if (is_the_sun_up(test_time,utc_plus,pos)):
            horizont_multiplier = 1
        else:
            horizont_multiplier = -1

        time_step = time_format.get_date_from_sec(time_step.get_sec_from_date()/2)

        new_time_sec = test_time.get_sec_from_date() + set_or_rise_multiplier*horizont_multiplier*time_step.get_sec_from_date()
        test_time = time_format.get_date_from_sec(new_time_sec)

    return(test_time)


def find_sun_noon_time(date: time_format, 
                       utc_plus:time_format, 
                       pos: geological_pos, 
                       time_resolution: float=60,
                       sun_ecliptic_longitude_time_diff_for_eot:time_format=time_format()
                       )->time_format:
    time_step:time_format = time_format(0,12,0,0)
    test_time = date + time_step
    if not is_the_sun_up(test_time,utc_plus,pos, sun_ecliptic_longitude_time_diff_for_eot):
        raise Exception(f"sun is not over the horizont at {test_time}, utc plu: {utc_plus}, sun cliptical lon diff: {sun_ecliptic_longitude_time_diff_for_eot}")
    
        
    while time_step.get_sec_from_date() >= time_resolution:

        if (is_the_sun_east(test_time,utc_plus,pos,sun_ecliptic_longitude_time_diff_for_eot)):
            horizont_multiplier = 1
        else:
            horizont_multiplier = -1

        time_step = time_format.get_date_from_sec(time_step.get_sec_from_date()/2)

        new_time_sec = test_time.get_sec_from_date() + horizont_multiplier*time_step.get_sec_from_date()
        test_time = time_format.get_date_from_sec(new_time_sec)

    return(test_time)

# def equat_2_horiz(V: equatorial_coord, geological_pos: geological_pos, time: time_format):
#     equat_2_horiz_on_north_pole(V,time)

# def get_sun_pos_in_horizontal_coordinates(time_sec: float, geological_pos: geological_pos)->horizontal_coord:
#     V = get_sun_pos_in_equatorial_coordinates(time_sec)
#     out = equat_2_horiz(V, geological_pos)
#     return out

@dataclass
class EclipticCorrectorTime:
    time_of_year: time_format
    time_difference: time_format

    def __str__(self):
        print(f"\n\ntime_of_year =\t{self.time_of_year}\ntime_difference =\t{self.time_difference}")

def calculate_ecliptic_longitude_from_eot_table(day_step=10, time_accuracy: time_format = time_format(0,0,0,10.0), verbose = False):
    diff_from_noon_list = []
    expected_diff_list = []
    diff_from_calculated_and_exoected_list = []
    test_time_diff_list = []
    out = []

    time_samples = range(0,365,day_step)
    for d in time_samples:
        date = time_format(d)
        time_step:time_format = time_format(date=2)
        test_time_diff = time_format()

        while time_step.get_sec_from_date() >= time_accuracy.get_sec_from_date():
            sun_culmination_time_in_sec = find_sun_noon_time(date,
                                                            utc_plus = utc_plus, 
                                                            pos = greenwich_pos,
                                                            time_resolution = 1,
                                                            sun_ecliptic_longitude_time_diff_for_eot = test_time_diff).get_day_from_time().get_sec_from_date()
            noon_time_in_sec = time_format(date=0,hour=12).get_sec_from_date()

            diff_from_noon = sun_culmination_time_in_sec - noon_time_in_sec

            expected_diff = get_eot_from_date(date).get_sec_from_date()

            diff_from_calculated_and_exoected = diff_from_noon - expected_diff

            if diff_from_calculated_and_exoected > 0:
                multiplier = -1
            else:
                multiplier = 1

            time_step = time_format.get_date_from_sec(time_step.get_sec_from_date()/2)

            new_time_sec = test_time_diff.get_sec_from_date() + multiplier*time_step.get_sec_from_date()
            test_time_diff = time_format.get_date_from_sec(new_time_sec)

        if verbose:
            print(f"{date}: {test_time_diff}")

        out.append(EclipticCorrectorTime(time_of_year=date, time_difference=test_time_diff))
        test_time_diff_list.append(test_time_diff.get_sec_from_date())
        expected_diff_list.append(expected_diff)
        diff_from_noon_list.append(diff_from_noon)
        diff_from_calculated_and_exoected_list.append(diff_from_calculated_and_exoected)

    if verbose:
        plt.plot(time_samples,expected_diff_list,label="expected_diff_list")
        plt.plot(time_samples,diff_from_noon_list,label="diff_from_noon_list")
        plt.plot(time_samples,diff_from_calculated_and_exoected_list,label="diff_from_calculated_and_exoected_list")
        plt.grid()
        plt.legend()
        plt.show()

        plt.plot(time_samples,np.array(test_time_diff_list)/60/60,"o-")
        plt.ylabel("hour diff")
        plt.xlabel("date")
        plt.grid()
        plt.show()
    
    np.save("sun_ecliptic_time_corr.npy",out)
    return out


if __name__:

    fehervar_pos = geological_pos()
    fehervar_pos.latitude = AngleDegree(degree=47,minute=11,second=28)
    fehervar_pos.longitude = AngleDegree(degree=18,minute=24,second=39)

    greenwich_pos = geological_pos()
    greenwich_pos.latitude = AngleDegree(degree=51,minute=28,second=48)
    greenwich_pos.longitude = AngleDegree(degree=0,minute=0,second=0)

    budapest_pos = geological_pos()
    budapest_pos.latitude = AngleDegree(degree=47,minute=29,second=54)
    budapest_pos.longitude = AngleDegree(degree=19,minute=2,second=27)

    polar_pos = geological_pos()
    polar_pos.latitude = AngleDegree(degree=90,minute=0,second=0)
    polar_pos.longitude = AngleDegree(degree=0,minute=0,second=0)

    utc_plus = time_format(hour=0)
    pos = budapest_pos

    if 0:
        recta_list = []
        decli_list = []
        for d in range(0,360,1):
            time = time_format(date=d)
            A = get_sun_pos_in_equatorial_coordinates(time)
            recta_list.append((A.rectascense.as_float()+360)%360)
            decli_list.append(A.declination.as_float())

        plt.plot(recta_list,decli_list,"o-")
        plt.grid()
        plt.show()

    if 0:
        for d in range(0,360,10):
            elev_list=[]
            azim_list=[]
        
            time_of_day_list=[]
            for h in range(0,24,1):
                for m in range(0,60,60):
                    time = time_format(date=d, hour=h, min=m)
                    time_of_day = time_format(hour=h, min=m)
                    time_of_day_list.append(time_of_day.get_sec_from_date()/3600)
                    # print(f"\n\nhour = {h}")
                    A = get_sun_pos_in_equatorial_coordinates(time)
                    # A.print()
                    B = equat_2_horiz(A,time, utc_plus, geo_pos=pos)
                    # B.print()
                    # plt.scatter(A.rectascense_deg, A.declination_deg)
                    azim_list.append((B.azimuth.as_float()+360)%360)
                    elev_list.append(B.elevation.as_float())


                    # plt.scatter(B.azimuth,B.elevation,color="C0")
            # plt.plot(azim_list,elev_list,"o-")
            plt.plot(time_of_day_list,elev_list,"o-")
            plt.axvline(12)

            print(d)
        # plt.title(f"day={d}")
        plt.grid()
        plt.show()


    def get_sun_pos_in_horizontal_coordinates(time: time_format, 
                                              utc_plus: float, 
                                              geo_pos: geological_pos,
                                              sun_ecliptic_longitude_time_diff_for_eot:time_format=time_format()
                                              )->horizontal_coord:
        A = get_sun_pos_in_equatorial_coordinates(time, sun_ecliptic_longitude_time_diff_for_eot)
        B = equat_2_horiz(A,time,utc_plus, geo_pos=geo_pos)
        return B
    
    def is_the_sun_up(time: time_format, 
                      utc_plus: float, 
                      geo_pos: geological_pos,
                      sun_ecliptic_longitude_time_diff_for_eot:time_format=time_format()
                      ) -> bool:
        horiontal_pos = get_sun_pos_in_horizontal_coordinates(time, utc_plus, geo_pos, sun_ecliptic_longitude_time_diff_for_eot)
        if horiontal_pos.elevation.as_float() >=0:
            return True
        else:
            return False

    def is_the_sun_east(time: time_format, 
                        utc_plus: float, 
                        geo_pos: geological_pos,
                        sun_ecliptic_longitude_time_diff_for_eot:time_format=time_format()
                        ) -> bool:
        horiontal_pos = get_sun_pos_in_horizontal_coordinates(time, utc_plus, geo_pos, sun_ecliptic_longitude_time_diff_for_eot)
        if horiontal_pos.azimuth.as_float() <=180:
            return True
        else:
            return False

          




    if 0:

        plt.figure(figsize=[10,7])
        rise_time_list=[]
        fall_time_list=[]

        day_step = 1
        step_by_step_differece_assumer = 0.01

        for d in range(365):
            rise_time_list.append(find_sun_set_time(time_format(date=d), pos, time_resolution=1, sunset=True).get_day_from_time().get_sec_from_date()/3600)
            fall_time_list.append(find_sun_set_time(time_format(date=d), pos, time_resolution=1, sunset=False).get_day_from_time().get_sec_from_date()/3600)


        x_axis = range(0,365,day_step)

        def find_max(time_list):
            max_idx = time_list.index(max(time_list))
            max_date = x_axis[max_idx]
            return max_date
        
        def find_min(time_list):
            min_idx = time_list.index(min(time_list))
            min_date = x_axis[min_idx]
            return min_date

        max_rise = find_max(rise_time_list)
        min_rise = find_min(rise_time_list)

        max_fall = find_max(fall_time_list)
        min_fall = find_min(fall_time_list)

        plt.plot(x_axis,np.array(rise_time_list)/3600,"o-")
        plt.plot(x_axis,np.array(fall_time_list)/3600,"o-")

        plt.axvline(max_rise,color="C0",linestyle="--",label="latest rise")
        plt.axvline(min_rise,color="C0",linestyle=":",label="earliest rise")
        plt.axvline(max_fall,color="C1",linestyle="--",label="latest set")
        plt.axvline(min_fall,color="C1",linestyle=":",label="earliest set")
        

        plt.title(f"Rise and set times of the Sun from Budapest\nearliest rise date= {min_rise}\nlatest set date= {max_fall}\nlatest rise date = {max_rise}\nearliest set date {min_fall}")
        plt.grid()
        plt.legend()
        plt.xlabel("Time passed since spring equinox [day]")
        plt.ylabel("time of day [hour]")
        plt.tight_layout()
        plt.savefig("out.png")
        plt.show()

    if 0:
        eot_diff_list=[]
        for d in range(365):
            eot_diff_list.append(get_eot_from_date(time_format(d)).get_sec_from_date())

        plt.plot(eot_diff_list)
        plt.show()

    get_analemma = False
    if get_analemma:

        horiz_list_elev=[]
        horiz_list_azim=[]
        for d in range(365):
            sun = get_sun_pos_in_horizontal_coordinates(time_format(d,12,00,00),time_format(),polar_pos)
            horiz_list_azim.append(sun.azimuth.as_float())
            horiz_list_elev.append(sun.elevation.as_float())
        plt.scatter(horiz_list_azim,horiz_list_elev)

        horiz_list_elev=[]
        horiz_list_azim=[]
        for d in range(365):
            sun = get_sun_pos_in_horizontal_coordinates(time_format(d,12,00,00),time_format(),polar_pos)
            horiz_list_azim.append(sun.azimuth.as_float())
            horiz_list_elev.append(sun.elevation.as_float())
        plt.scatter(horiz_list_azim,horiz_list_elev)

        plt.axis("equal")
        plt.grid()
        plt.ylabel("elevation [deg]")
        plt.xlabel("azimuth [deg]")
        plt.title("Sun position on the nort pole at every noon")

        plt.show()
    
    test_eot = False
    if test_eot:
        plt.figure(figsize=[10,7])

        simulated_noon_diff_list = []
        list2 = []

        for d in range(365):
            date=time_format(d)
            simulated_noon_diff_list.append(get_sun_pos_in_ecliptic_coordinates(date).longitude.as_float())
            list2.append(get_sun_pos_in_ecliptic_coordinates(date,eot=True).longitude.as_float())


        plt.plot(simulated_noon_diff_list,'o-')
        plt.plot(list2,'o-')

        plt.show()

    if 0:
        simulated_noon_diff_list = []
        eot_diff_list = []
        time_samples = range(0,365,5)
        for d in time_samples:
            simulated_noon_diff_list.append(find_sun_noon_time(time_format(d),utc_plus=utc_plus, pos=greenwich_pos,time_resolution=1).get_day_from_time().get_sec_from_date()-time_format(0,12).get_sec_from_date())
            eot_diff_list.append(get_eot_from_date(time_format(d)).get_sec_from_date())

        plt.plot(time_samples,simulated_noon_diff_list,"o-")
        plt.plot(time_samples,eot_diff_list,"o-")

        plt.show()

        # plt.plot(time_samples,np.array(eot_diff_list)-np.array(simulated_noon_diff_list))
        # plt.show()

    calculate_ecliptic_longitude_from_eot_table_flag=False
    if calculate_ecliptic_longitude_from_eot_table_flag:
        calculate_ecliptic_longitude_from_eot_table(day_step=1,verbose=True)
        out = np.load("sun_ecliptic_time_corr.npy",allow_pickle=True)
        print(out)

    if 1:
        raw: np.ndarray[EclipticCorrectorTime] = np.load("sun_ecliptic_time_corr.npy",allow_pickle=True)
        out: list[EclipticCorrectorTime] = list(raw)

        dates=[]
        values=[]
        for i in out:
            dates.append(i.time_of_year.get_sec_from_date())
            values.append(i.time_difference.get_sec_from_date())

        plt.plot(dates,np.array(values)/3600)
        plt.show()


