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
    
    def modulo(self) -> "AngleDegree":
        temp = AngleDegree.from_float(self.as_float())
        temp.degree = temp.degree%360
        return temp

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
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return AngleDegree.from_float(self.as_float() * other)
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
        self._azimuth_like = value

        # azimuth_deg = value.as_float()
        # if azimuth_deg >= 0.0 and azimuth_deg <= 360.0:
        #     self._azimuth_like = value
        # else:
        #     raise ValueError("invalid azimuth")
        
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
    positive: bool = True
    date: int = 0
    hour: int = 0
    min: int = 0
    sec: float = 0.0


    def get_sec_from_date(self):
        if self.positive:
            mul = 1
        else:
            mul = -1

        out = mul*(self.date*86400) + self.hour*3600 + self.min*60 + self.sec
        return out
    
    def process_of_year(self):
        return self.get_sec_from_date()/(365.25*86400)
    
    def get_date_from_sec(sec:float):
        out = time_format()

        if sec >= 0:
            out.positive = True
            out.date = int(sec/60/60/24)
            remain_sec = sec-out.date*60*60*24


        else:
            sec=-sec
            out.positive = False
            out.date = int(sec/60/60/24)+1
            remain_sec = out.date*60*60*24-sec
        

        out.hour = int(remain_sec/60/60)
        remain_sec = remain_sec - out.hour*60*60

        out.min = int(remain_sec/60)
        remain_sec = remain_sec - out.min*60

        out.sec = remain_sec

        return out

    def get_day_from_time(self):
        return time_format(date=0, hour=self.hour, min=self.min, sec=self.sec)
    
    def __str__(self):
        return(f"{np.sign(self.get_sec_from_date())}{self.date:3} d {self.hour:2} h {self.min:2} min {self.sec:2.3f} sec")
    
    def __add__(self, other: "time_format")->"time_format":
        return_time = time_format.get_date_from_sec(self.get_sec_from_date() + other.get_sec_from_date())
        return return_time
    
    def __sub__(self, other: "time_format")->"time_format":
        return_time = time_format.get_date_from_sec(self.get_sec_from_date() - other.get_sec_from_date())
        return return_time
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return time_format.get_date_from_sec(self.get_sec_from_date() * other)
        return NotImplemented
    
    def __rmul__(self, other):
        return self*other


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

@dataclass
class EclipticCorrectorTime:
    time_of_year: time_format
    time_difference: time_format

    def __str__(self):
        return(f"\n\ntime_of_year =\t{self.time_of_year}\ntime_difference =\t{self.time_difference}\n")
    
    def copy(self) -> "EclipticCorrectorTime":
        return EclipticCorrectorTime(time_of_year= self.time_of_year, time_difference=self.time_difference)


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


@dataclass
class observatory:
    name: str = "no name"
    geo_pos: geological_pos = field(default_factory = geological_pos)
    UTC_plus: time_format = field(default_factory = time_format)



fehervar_pos = geological_pos()
fehervar_pos.latitude = AngleDegree(degree=47,minute=11,second=28)
fehervar_pos.longitude = AngleDegree(degree=18,minute=24,second=39)
fehervar_obs = observatory(geo_pos=fehervar_pos, UTC_plus=time_format(hour=1)) 
fehervar_obs.name = "Székesfehérvár"

greenwich_pos = geological_pos()
greenwich_pos.latitude = AngleDegree(degree=51,minute=28,second=48)
greenwich_pos.longitude = AngleDegree(degree=0,minute=0,second=0)
greenwich_obs = observatory(geo_pos=greenwich_pos,UTC_plus=time_format())
greenwich_obs.name = "Greenwich"

budapest_pos = geological_pos()
budapest_pos.latitude = AngleDegree(degree=47,minute=29,second=54)
budapest_pos.longitude = AngleDegree(degree=19,minute=2,second=27)
budapest_obs = observatory(geo_pos=budapest_pos, UTC_plus=time_format(hour=1))
budapest_obs.name = "Budapest"

polar_pos = geological_pos()
polar_pos.latitude = AngleDegree(degree=90,minute=0,second=0)
polar_pos.longitude = AngleDegree(degree=0,minute=0,second=0)
polar_obs = observatory(geo_pos=polar_pos, UTC_plus=time_format())
polar_obs.name = "North Pole"

madrid_pos = geological_pos()
madrid_pos.latitude = AngleDegree(degree=40,minute=30,second=0)
madrid_pos.longitude = AngleDegree(positive_sign=False,degree=3,minute=40,second=0)
madrid_obs = observatory(geo_pos=madrid_pos, UTC_plus=time_format(hour=1))
madrid_obs.name = "Madrid"

moscow_pos = geological_pos()
moscow_pos.latitude = AngleDegree(degree=55,minute=45,second=0)
moscow_pos.longitude = AngleDegree(positive_sign=True,degree=37,minute=37,second=0)
moscow_obs = observatory(geo_pos=moscow_pos, UTC_plus=time_format(hour=3))
moscow_obs = "Moscow"

mexico_pos = geological_pos()
mexico_pos.latitude = AngleDegree(degree=19,minute=15,second=0)
mexico_pos.longitude = AngleDegree(positive_sign=False,degree=99,minute=8,second=0)
mexico_obs = observatory(geo_pos=mexico_pos, UTC_plus=time_format(hour=-6))
mexico_obs.name = "Mexico"

quito_pos = geological_pos()
quito_pos.latitude = AngleDegree(degree=0,minute=13,second=0)
quito_pos.longitude = AngleDegree(positive_sign=False,degree=78,minute=31,second=0)
quito_obs = observatory(geo_pos=quito_pos, UTC_plus=time_format(hour=-5))
quito_obs.name = "Quito"

oslo_pos = geological_pos()
oslo_pos.latitude = AngleDegree(degree=59,minute=55,second=0)
oslo_pos.longitude = AngleDegree(positive_sign=True,degree=10,minute=44,second=0)
oslo_obs = observatory(geo_pos=oslo_pos, UTC_plus=time_format(hour=1))
oslo_obs.name = 'Oslo'



def find_zero_crossing_time( function,
                            test_time: time_format, 
                            time_span: time_format = time_format(date=90), 
                            time_resolution: time_format = time_format(min=1)
                            ) -> time_format:
    diff_val: float = function(test_time)
    time_step: time_format = time_format.get_date_from_sec(time_span.get_sec_from_date()*0.5)

    left_end = function(test_time+time_step)
    right_end = function(test_time-time_step)
    # if np.sign(left_end) == np.sign(right_end):
    #     raise ValueError(f"given range has no, or multiple zero crossing\nleft end: {test_time+time_step}\t{left_end}\nrigt end: {test_time-time_step}\t{right_end}")
    if left_end == 0:
        return test_time + time_step

    sign_multiplier = 1 if left_end > 0 else -1

    while time_step.get_sec_from_date() > time_resolution.get_sec_from_date():

        if diff_val > 0:
            multiplier = -1
        else:
            multiplier = 1
        
        test_time = test_time + (sign_multiplier*multiplier) * time_step
        time_step = time_format.get_date_from_sec(time_step.get_sec_from_date()*0.5)
        diff_val = function(test_time)
    
    return test_time

def find_extreme_value_time( function,
                            test_time: time_format, 
                            time_span: time_format = time_format(date=90), 
                            time_resolution: time_format = time_format(min=1),
                            type: str = "max"
                            ) -> time_format:
    # diff_val: float = function(test_time)

    if type == "max":
        mul = 1
    elif type == "min":
        mul = -1
    else:
        raise
    time_step: time_format = time_format.get_date_from_sec(time_span.get_sec_from_date()*0.5)

    while time_step.get_sec_from_date() > time_resolution.get_sec_from_date():
        # print(test_time)

        test_time_left = test_time-time_step
        test_time_right = test_time+time_step

        left_val = function(test_time_left)
        right_val = function(test_time_right)
        # print(f"{test_time_left} = {left_val:.2f} \t {test_time_right} = {right_val:.2f}")

        time_step = time_format.get_date_from_sec(time_step.get_sec_from_date()*0.5)

        if left_val > right_val:
            if type == "max":
                test_time = test_time_left + time_step
            elif type == "min":
                test_time = test_time_right - time_step

        else:
            if type == "max":
                test_time = test_time_right - time_step
            elif type == "min":
                test_time = test_time_left + time_step
            
        
    return test_time





def distance_arrows(beg_pos,end_pos,text,text_pos,color):
    plt.text(
        text_pos[0],
        text_pos[1],
        text,
        va="center",
        ha = "center",
        color = color
    )

    # draw the arrow itself
    plt.annotate(
        "",
        xy=(beg_pos[0], beg_pos[1]),
        xytext=(end_pos[0], end_pos[1]),
        arrowprops=dict(
            arrowstyle="<->",
            color=color
        )
    )

def distance_arrows2(beg_pos,end_pos,text,text_pos_vertical,color):
    distance_arrows(beg_pos,
                    end_pos,
                    text,
                    text_pos=[(beg_pos[0]+end_pos[0])/2,text_pos_vertical], 
                    color=color
                    )
    
def function_equatorial__wiki(time: time_format)->float:
    return get_sun_pos_in_equatorial_coordinates__wiki(time).declination.as_float()

def function_equatorial__naive(time: time_format)->float:
    return get_sun_pos_in_equatorial_coordinates__adjustable_ecliptic_lon(time).declination.as_float()




def get_eot_from_date(date: time_format)->time_format:
    EOT_TABLE0=csv_read.getEOT_csv()
    EOT_TABLE=np.concatenate((EOT_TABLE0[80::],EOT_TABLE0[:80:]))

    idx=int(date.date)%365
    out = time_format.get_date_from_sec(EOT_TABLE[idx])
    return out


sun_latitude_lookup:list[EclipticCorrectorTime] = None

def ecliptic_longitude_time_diff_interpolator(time: time_format)->time_format:
    sun_latitude_lookup0 = sun_latitude_lookup.copy()
    sun_latitude_lookup0.append(sun_latitude_lookup0[0].copy())

    time_step = sun_latitude_lookup0[1].time_of_year-sun_latitude_lookup0[0].time_of_year
    sun_latitude_lookup0[-1].time_of_year = sun_latitude_lookup0[-2].time_of_year + time_step

    for i in range(len(sun_latitude_lookup0)-1):
        check_date = sun_latitude_lookup0[i].time_of_year.get_sec_from_date()
        check_date_next = sun_latitude_lookup0[i+1].time_of_year.get_sec_from_date()

        if time.get_sec_from_date()>=check_date and time.get_sec_from_date()<check_date_next:
            check_val = sun_latitude_lookup0[i].time_difference.get_sec_from_date()
            check_val_next = sun_latitude_lookup0[i+1].time_difference.get_sec_from_date()

            time_sec = time.get_sec_from_date()

            out = (check_val_next-check_val)/(check_date_next-check_date)*(time_sec-check_date)+check_val
            return time_format.get_date_from_sec(out)
    else:
        raise Exception(f"no interpolatabel values found for: {time} in list: {sun_latitude_lookup0}")

def get_sun_pos_in_ecliptic_coordinates__adjustable_ecliptic_lon(time: time_format, 
                                        sun_ecliptic_longitude_time_diff_for_eot:time_format=time_format())->EclipticCoord:

    # sun_ecliptic_longitude_time_diff_for_eot=get_ecliptic_longitude(time)

    # if sun_latitude_lookup == None:
    #     sun_ecliptic_longitude_time_diff_for_eot == time_format()

    time = time + sun_ecliptic_longitude_time_diff_for_eot

    deg_from_time = 360*time.process_of_year()
    longitude_deg = (deg_from_time)%360

    longitude = AngleDegree.from_float(longitude_deg)
    
    coord = EclipticCoord(AngleDegree(0),AngleDegree(0))
    coord.longitude = longitude
    coord.latitude = AngleDegree(0)

    return coord


def get_sun_pos_in_ecliptic_coordinates__wiki(time: time_format) -> EclipticCoord:
    # https://en.wikipedia.org/wiki/Position_of_the_Sun
    # def get_julian_date():

    # JD = get_julian_date()

    # days since 2000.01.01.
    # n = JD - 2451545.0

    n=time_format(date=80,hour=17) + time
    
    # mean longitude
    L = AngleDegree(degree=280.460) + AngleDegree(degree=0.9856474*n.get_sec_from_date()/86400)
    #mean anomaly
    g = AngleDegree(degree=357.528) + AngleDegree(degree=0.9856003*n.get_sec_from_date()/86400)

    # ecliptic_longitude
    lmbd = L + AngleDegree(degree=1.915*sind(g)) + AngleDegree(degree=0.020*sind(g*2))
    coord = EclipticCoord(latitude=AngleDegree(),longitude=lmbd.modulo())

    return coord


def get_sun_pos_in_ecliptic_coordinates__interpolated_eot_table(time: time_format)->EclipticCoord:

    # sun_ecliptic_longitude_time_diff_for_eot=get_ecliptic_longitude(time)

    # if sun_latitude_lookup == None:
    #     sun_ecliptic_longitude_time_diff_for_eot == time_format()



    time = time + ecliptic_longitude_time_diff_interpolator(time)

    deg_from_time = 360*time.process_of_year()
    longitude_deg = (deg_from_time)%360

    longitude = AngleDegree.from_float(longitude_deg)
    
    coord = EclipticCoord(AngleDegree(0),AngleDegree(0))
    coord.longitude = longitude
    coord.latitude = AngleDegree(0)

    return coord


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

def get_sun_pos_in_equatorial_coordinates__adjustable_ecliptic_lon(time: time_format, 
                                          sun_ecliptic_longitude_time_diff_for_eot:time_format=time_format()
                                          )->equatorial_coord:
    sun_ecliptic_coord = get_sun_pos_in_ecliptic_coordinates__adjustable_ecliptic_lon(time= time, 
                                                             sun_ecliptic_longitude_time_diff_for_eot = sun_ecliptic_longitude_time_diff_for_eot)   
    sun_vector_ecliptic = get_vector_form_ecliptic_coordinates(sun_ecliptic_coord)

    equinox_ecliptic_coord = EclipticCoord(AngleDegree(), AngleDegree())
    equinox_vector_ecliptic = get_vector_form_ecliptic_coordinates(equinox_ecliptic_coord)
    
    sun_vector_equatorial = rotate_vector(sun_vector_ecliptic, equinox_vector_ecliptic, AXIAL_TILT)
    sun_equatorial = get_equatorial_from_vector(sun_vector_equatorial)
    return sun_equatorial

def get_sun_pos_in_equatorial_coordinates__interpolated_eot_table(time: time_format)->equatorial_coord:

    sun_ecliptic_coord = get_sun_pos_in_ecliptic_coordinates__interpolated_eot_table(time= time)   
    sun_vector_ecliptic = get_vector_form_ecliptic_coordinates(sun_ecliptic_coord)

    equinox_ecliptic_coord = EclipticCoord(AngleDegree(), AngleDegree())
    equinox_vector_ecliptic = get_vector_form_ecliptic_coordinates(equinox_ecliptic_coord)
    
    sun_vector_equatorial = rotate_vector(sun_vector_ecliptic, equinox_vector_ecliptic, AXIAL_TILT)
    sun_equatorial = get_equatorial_from_vector(sun_vector_equatorial)
    return sun_equatorial

def get_sun_pos_in_equatorial_coordinates__wiki(time: time_format
                                          )->equatorial_coord:
    sun_ecliptic_coord = get_sun_pos_in_ecliptic_coordinates__wiki(time= time)   
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

def equat_2_horiz(equatorial_coordinates: equatorial_coord, 
                  time: time_format, 
                  observ: observatory
                  )->horizontal_coord:
    rotational_axis     = descates_vector(0,0,1)
    solar_day           = time_format(0,hour = 24)
    siderical_year      = time_format(date=365,hour=6,min=9,sec=10)

    def replus(a,b):
        return((a*b)/(a+b))
    
    siderical_day:time_format = time_format.get_date_from_sec(replus(solar_day.get_sec_from_date(),siderical_year.get_sec_from_date()))

    rotations_by_date = time.get_sec_from_date()/siderical_day.get_sec_from_date()
    longitude_deg = observ.geo_pos.longitude.as_float()

    utc_plus_sec = observ.UTC_plus.get_sec_from_date()
    utc_plus_sec_deg = utc_plus_sec/siderical_day.get_sec_from_date()*360.0

    rotations_deg = rotations_by_date*360 + longitude_deg - utc_plus_sec_deg

    V = get_vector_form_equatorial(equatorial_coordinates)

    W = rotate_vector(V,rotational_axis,-rotations_deg)

    latitude_axis = descates_vector(0,1,0)
    latitude_deg = observ.geo_pos.latitude.as_float()

    WW = rotate_vector(W,latitude_axis,90-latitude_deg)

    out = get_horizontal_from_vector(WW)

    return out

def find_sun_set_time(date: time_format, 
                      observ: observatory,
                      time_resolution: float=60, 
                      sunset: bool = True)->time_format:
    time_step = time_format(0,12,0,0)
    test_time = date + time_step
    if not is_the_sun_up(test_time,observ):
        raise Exception(f"sun is not over the horizont at {test_time}")
    
    if sunset:
        set_or_rise_multiplier = 1
    else:
        set_or_rise_multiplier = -1

    time_step: time_format
    while time_step.get_sec_from_date() >= time_resolution:

        if (is_the_sun_up(test_time,observ)):
            horizont_multiplier = 1
        else:
            horizont_multiplier = -1

        time_step = time_format.get_date_from_sec(time_step.get_sec_from_date()/2)

        new_time_sec = test_time.get_sec_from_date() + set_or_rise_multiplier*horizont_multiplier*time_step.get_sec_from_date()
        test_time = time_format.get_date_from_sec(new_time_sec)

    return(test_time)


def find_sun_noon_time(date: time_format, 
                       observ: observatory,
                       time_resolution: float=60,
                       sun_ecliptic_longitude_time_diff_for_eot:time_format=time_format()
                       )->time_format:
    time_step:time_format = time_format(0,12,0,0)
    test_time = date + time_step
    if not is_the_sun_up(test_time, observ, sun_ecliptic_longitude_time_diff_for_eot):
        raise Exception(f"sun is not over the horizont at {test_time}, utc plu: {observ.UTC_plus}, sun cliptical lon diff: {sun_ecliptic_longitude_time_diff_for_eot}")
    
        
    while time_step.get_sec_from_date() >= time_resolution:

        if (is_the_sun_east(test_time,observ,sun_ecliptic_longitude_time_diff_for_eot)):
            horizont_multiplier = 1
        else:
            horizont_multiplier = -1

        time_step = time_format.get_date_from_sec(time_step.get_sec_from_date()/2)

        new_time_sec = test_time.get_sec_from_date() + horizont_multiplier*time_step.get_sec_from_date()
        test_time = time_format.get_date_from_sec(new_time_sec)

    return(test_time)




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
            sun_culmination_time_in_sec = find_sun_noon_time(date=date,
                                                            observ=greenwich_obs,
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


def get_sun_pos_in_horizontal_coordinates__adjustable_ecliptic_lon( time: time_format, 
                                                                    observ: observatory,
                                                                    sun_ecliptic_longitude_time_diff_for_eot: time_format=time_format()
                                                                    )->horizontal_coord:
    A = get_sun_pos_in_equatorial_coordinates__adjustable_ecliptic_lon(time, sun_ecliptic_longitude_time_diff_for_eot)
    B = equat_2_horiz(A,time,observ)
    return B

def get_sun_pos_in_horizontal_coordinates__interpolated_eot_table(  time: time_format, 
                                                                    observ: observatory,
                                                                    )->horizontal_coord:
    A = get_sun_pos_in_equatorial_coordinates__interpolated_eot_table(time)
    B = equat_2_horiz(A,time,observ)
    return B

def get_sun_pos_in_horizontal_coordinates__wiki(    time: time_format, 
                                                    observ: observatory,
                                                    )->horizontal_coord:
    A = get_sun_pos_in_equatorial_coordinates__wiki(time)
    B = equat_2_horiz(A,time,observ)
    return B

def is_the_sun_up(time: time_format, 
                    observ: observatory,
                    sun_ecliptic_longitude_time_diff_for_eot:time_format=time_format()
                    ) -> bool:
    horiontal_pos = get_sun_pos_in_horizontal_coordinates__adjustable_ecliptic_lon(time, observ, sun_ecliptic_longitude_time_diff_for_eot)
    if horiontal_pos.elevation.as_float() >=0:
        return True
    else:
        return False

def is_the_sun_east(time: time_format, 
                    observ: observatory,
                    sun_ecliptic_longitude_time_diff_for_eot:time_format=time_format()
                    ) -> bool:
    horiontal_pos = get_sun_pos_in_horizontal_coordinates__adjustable_ecliptic_lon(time, observ, sun_ecliptic_longitude_time_diff_for_eot)
    if horiontal_pos.azimuth.as_float() <=180:
        return True
    else:
        return False
    

