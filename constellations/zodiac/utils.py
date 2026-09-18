import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi
from dataclasses import dataclass
import trimesh
from shapely.geometry import Polygon


ORDER_OF_ECLIPTIC_LINE  = 0
ORDER_OF_LINES          = 1
ORDER_OF_STARS_MINOR    = 2
ORDER_OF_STARS_MAJOR    = 3
ORDER_OF_BORDES         = 4

@dataclass
class ClosedDrawing():
    points: list
    name: str

    def just_plot_dont_show(self):
        self.points.append(self.points[0])
        for idx in range(len(self.points)-1):
            A=self.points[idx]
            B=self.points[idx+1]
            plt.plot([A[0],B[0]],[A[1],B[1]],marker = "o", color="black")

    def plot_my_drawing(self):
        self.just_plot_dont_show()
        plt.show()

    def multiply_with_scalar(self,a):
        out_list=[]
        for idx, p in enumerate(self.points):
            # print(self.points[idx][0])
            out_list.append((p[0]*a, p[1]*a))

        self.points = out_list

    def print(self):
        for p in self.points:
            print(f"{p}")


@dataclass
class Sexagesimal:
    is_positive: bool =True
    deg: int=0
    min: int=0
    sec: float=0.0

    @classmethod
    def from_hourDeg_to_Sexagesimal(cls, hour_or_deg: float):
        # cls is the class itself
        if hour_or_deg < 0:
            is_positive = False
        else:
            is_positive = True

        hour_or_deg = abs(hour_or_deg)

        h = int(hour_or_deg)
        m = int((hour_or_deg - h) * 60)
        s = (hour_or_deg - h - m/60) * 3600

        return cls(is_positive, h, m, s)  # creates a new instance

    def from_Sexagesimal_to_hourDeg(self):
        # self is the specific instance
        if self.is_positive:
            sign = 1
        else:
            sign = -1

        return sign*(self.deg + self.min/60 + self.sec/3600)

    def get_string__hour_sec_min(self) -> str:
        if not self.is_positive:
            hourDeg = self.from_Sexagesimal_to_hourDeg()
            out = self.from_hourDeg_to_Sexagesimal(hourDeg+24)
        else:
            out=self
        return f"{out.deg:02.0f} h {out.min:02.0f} m {out.sec:02.0f} s"
    
    def get_string__deg_min_sec(self) -> str:
        if self.is_positive:
            sign = "+"
        else:
            sign = "-"

        return f"{sign}{self.deg:02.0f}˚ {self.min:02.0f}' {self.sec:02.0f}\""

@dataclass
class RaDecDegCoord_deg():
    right_ascension_deg: float
    declination_deg: float

@dataclass
class PointDatas():
    name: str
    ra_dec_deg: RaDecDegCoord_deg
    apparent_mag: float
    constellation: str


@dataclass
class SkyLine():
    point_data_1: PointDatas
    point_data_2: PointDatas

    linestyle: str
    color: str
    width: str
    alpha: str

    def __repr__(self):
        ra1 = self.point_data_1.ra_dec_deg.right_ascension_deg
        dec1 = self.point_data_1.ra_dec_deg.declination_deg
        ra2 = self.point_data_2.ra_dec_deg.right_ascension_deg
        dec2 = self.point_data_2.ra_dec_deg.declination_deg
        return f"({ra1:.2f}, {dec1:.2f}) - ({ra2:.2f}, {dec2:.2f})"

@dataclass
class ListOfSkylines():

    list_of_skylines: list[SkyLine]

    def get_only_the_borders_from_this_constellation(self, constellation: str):
        output_borders = []
        for i in self.list_of_skylines:
            if (i.point_data_1.constellation == constellation):
                output_borders.append(i)
        return(output_borders)

    def get_a_list_of_separated_constellations(self):
        constellation_already_used = []
        for i in self.list_of_skylines:
            if not (i.point_data_1.constellation in constellation_already_used):
                constellation_already_used.append(i.point_data_1.constellation)
        return(constellation_already_used)

    def print_points(self):
        for i in self.list_of_skylines:
            print(i)

@dataclass
class Vector:
    x: float
    y: float
    z: float

    def __sub__(self, other: "Vector"):
        return Vector(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
        )

    def __add__(self, other: "Vector"):
        return Vector(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
        )

    def __rmul__(self, m):
        return Vector(
            x=m*self.x,
            y=m*self.y,
            z=m*self.z,
        )

    def abs(self):
        return np.sqrt(self.x**2+self.y**2+self.z**2)

    def norm(self):
        L=self.abs()
        return Vector(x=self.x/L,
                      y=self.y/L,
                      z=self.z/L)

@dataclass
class Line():
    start_point: Vector
    end_point: Vector


    def get_stripe(self, width=0.005)->ClosedDrawing:
        dir = self.end_point - self.start_point
        step_aside_vector = Vector(x=dir.y, y=-1*dir.x, z = 0)
        step_aside_vector = width*(step_aside_vector.norm())

        A = self.start_point + step_aside_vector
        B = A+ dir
        C = B-2*step_aside_vector
        D = C -dir        

        points=[]
        points.append((A.y, A.x))
        points.append((B.y, B.x))
        points.append((C.y, C.x))
        points.append((D.y, D.x))


        return ClosedDrawing(points=points,name ="")


    def get_dots(self, width=0.005)->list[ClosedDrawing]:
        
        output_closed_drawig_list=[]
        for point in [self.start_point, self.end_point]:
            edge_points = []

            for i in range(0,360,10):
                edge_point0 = point + Vector(x=width*np.cos(i/180*np.pi), y=width*np.sin(i/180*np.pi), z=0)
                edge_points.append((edge_point0.y, edge_point0.x))

            output_closed_drawig_list.append(ClosedDrawing(points=edge_points, name =""))    
                
        return output_closed_drawig_list


def abs_vector(v:np.ndarray) -> float:
    x = v[0]
    y = v[1]
    z = v[2]
    return np.sqrt(x**2+y**2+z**2)

def norm_vector(v:np.ndarray) -> np.ndarray:
    return v/abs_vector(v)

def disolve_vector(v):
    return v[0],v[1],v[2]

def upproject(v):
    """
    return: [x,y,z]
    """
    v=np.array(v)+np.array([0,0,1])
    w=v/v[2]
    return w

def equirectangular_project(v):
    x = np.arctan2(v[0],v[1])
    # y=v[2]
    y=np.arcsin(v[2])
    w = np.array([x,y])
    return w

def central_cylindrical_project(v):
    v_x = v[0]
    v_y = v[1]
    v_z = v[2]
    x = np.arctan2(v[0],v[1])
    # y=v[2]
    # y = np.arcsin(v[2])
    # y = v_z/np.sqrt(v_x**2+v_y**2)
    b=np.arctan(v_z/np.sqrt(v_x**2+v_y**2))
    y=np.tan(b)
    w = np.array([x,y])
    return w

def mercator_project(v):
    v_x = v[0]
    v_y = v[1]
    v_z = v[2]
    x = np.arctan2(v[0],v[1])
    # y=v[2]
    # y = np.arcsin(v[2])
    # y = v_z/np.sqrt(v_x**2+v_y**2)
    b=np.arctan(v_z/np.sqrt(v_x**2+v_y**2))
    y = np.log(1/np.cos(b) + np.tan(b))
    w = np.array([x,y])
    return w


def lambert_project(v):
    v_x = v[0]
    v_y = v[1]
    v_z = v[2]
    x = np.arctan2(v[0],v[1])
    y=v[2]
    w = np.array([x,y])
    return w


# cylindrical_project=equirectangular_project
cylindrical_project = mercator_project

# X axis originally points to equinox point
def xrot(v,alpha_deg):
    alp=alpha_deg/180*pi
    R=np.array([[1,0,0],[0,cos(alp),-sin(alp)],[0,sin(alp),cos(alp)]])
    return v @ R

# X axis originally points to equinox point
def yrot(v,alpha_deg):
    alp=alpha_deg/180*pi
    R=np.array([[cos(alp),0,sin(alp)],[0,1,0],[-sin(alp),0,cos(alp)]])
    return v @ R

# X axis originally points to equinox point
def zrot(v,alpha_deg):
    alp=alpha_deg/180*pi
    R=np.array([[cos(alp),-sin(alp),0],[sin(alp),cos(alp),0],[0,0,1]])
    return v @ R

def center_to_RaDec(v,Dec_deg,Ra_deg):
    w0=zrot(v,Ra_deg)
    w1=yrot(w0,-(Dec_deg-90))
    # w1=w0
    return w1

def get_3d_vec_from_RaDec(ra,dec):
    v = np.array([cos(ra)*cos(dec),sin(ra)*cos(dec), sin(dec)])
    return v

def get_RaDec_from_3dVector(v:np.ndarray):
    v_x = v[0]
    v_y = v[1]
    v_z = v[2]
    ra = np.arctan2(v_y,v_x)*24/(2*np.pi)
    if ra <0:
        ra = ra + 24
    dec = np.arcsin(v_z)*180/np.pi
    return ra,dec

def get_transformed_vector(ra_dec_coord_deg: RaDecDegCoord_deg, center_Dec_deg: float, center_ra_deg: float, zrot_deg: float):   
    ra = ra_dec_coord_deg.right_ascension_deg/180*np.pi
    dec = ra_dec_coord_deg.declination_deg/180*np.pi
    v = get_3d_vec_from_RaDec(ra,dec)
    v = center_to_RaDec(v,center_Dec_deg,center_ra_deg)
    v = zrot(v,zrot_deg)
    return v

def get_transformed_vector_from3d(v: np.ndarray, center_Dec_deg: float, center_ra_deg: float, zrot_deg: float):   
    v = center_to_RaDec(v,center_Dec_deg,center_ra_deg)
    v = zrot(v,zrot_deg)
    return v

def condition_magnitudes(star, hmg, hmg2):
    if star['Apparent Magnitude'] <= hmg:
        S=star['Apparent Magnitude']
        alpha=1
    else:
        S=hmg
        alpha=0.5
    if star['Apparent Magnitude'] <= hmg2:
        marker='*'
    else:
        marker='.'
    return S,marker,alpha

def polar_upproject(v):
    w0 = upproject(v)
    w = zrot(w0,90)
    theta_R = np.array([-np.arctan2(w[1],w[0]),np.sqrt(w[1]**2+w[0]**2)])
    return theta_R

def vector2ra_dec(v):
    ra2 = np.arctan2(v[1],v[0])
    xy_shadow_len=np.sqrt(v[0]**2+v[1]**2)
    dec2 = np.arctan2(v[2],xy_shadow_len)
    return ra2,dec2



def plot_lines_polar(lines: list[SkyLine], center_Dec_deg,center_ra_deg,zrot_deg, ax):
    for idx,line in enumerate(lines):
        print(f"polar lines:\t{idx/len(lines)*100:.2f}%")

        v1 = get_transformed_vector(line.point_data_1.ra_dec_deg, center_Dec_deg, center_ra_deg, zrot_deg)
        theta_R1 = polar_upproject(v1)

        v2 = get_transformed_vector(line.point_data_2.ra_dec_deg, center_Dec_deg, center_ra_deg, zrot_deg)
        theta_R2 = polar_upproject(v2)

        theta1=theta_R1[0]
        theta2=theta_R2[0]
        R1=theta_R1[1]
        R2=theta_R2[1]
        ax.plot([theta1,theta2],[R1,R2],linewidth=line.width,linestyle=line.linestyle,alpha=1,color=line.color,zorder=ORDER_OF_LINES)

def plot_lines_str_grph(lines: list[SkyLine], center_Dec_deg,center_ra_deg,zrot_deg, ax):
    for idx,line in enumerate(lines):
        print(f"str_grp lines:\t{idx/len(lines)*100:.2f}%")

        v1 = get_transformed_vector(line.point_data_1.ra_dec_deg,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_1 = upproject(v1)

        v2 = get_transformed_vector(line.point_data_2.ra_dec_deg,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_2 = upproject(v2)

        x1=xyz_1[0]
        x2=xyz_2[0]
        y1=xyz_1[1]
        y2=xyz_2[1]
        plt.plot([y1,y2],[x1,x2],linewidth=line.width,linestyle=line.linestyle,alpha=0.9,color=line.color,zorder=ORDER_OF_LINES)
                        

def plot_borders_polar(borders: list[SkyLine], center_Dec_deg,center_ra_deg,zrot_deg, ax):
    for idx,line in enumerate(borders):
        if idx%100==0:
            print(f"polar borders:\t{idx/len(borders)*100:.2f}%")
        ra1_rad  = line.point_data_1.ra_dec_deg.right_ascension_deg/180*pi
        dec1_rad = line.point_data_1.ra_dec_deg.declination_deg/180*pi
        ra2_rad  = line.point_data_2.ra_dec_deg.right_ascension_deg/180*pi
        dec2_rad = line.point_data_2.ra_dec_deg.declination_deg/180*pi

        ra_diff_rad = (ra2_rad-ra1_rad)
        if abs(ra_diff_rad)>pi:
            if ra1_rad<ra2_rad:
                ra1_rad=ra1_rad+2*pi
            else:
                ra1_rad=ra1_rad-2*pi  
            ra_diff_rad = (ra2_rad-ra1_rad)

        dec_diff_rad = (dec2_rad-dec1_rad)
        if abs(dec_diff_rad)>pi:
            if dec1_rad<dec2_rad:
                dec1_rad=dec1_rad+2*pi
            else:
                dec1_rad=dec1_rad-2*pi   
            dec_diff_rad = (dec2_rad-dec1_rad)
        iteration_num = max((np.floor(abs(ra_diff_rad)/(2*np.pi)*360))+1 , (np.floor(abs(dec_diff_rad)/(2*np.pi)*360))+1)

        ra_step_rad = ra_diff_rad/iteration_num
        dec_step_rad = dec_diff_rad/iteration_num
        ra_now_rad = ra1_rad
        dec_now_rad = dec1_rad

        ra_dec_now_deg = line.point_data_1.ra_dec_deg

        for i in range(int(iteration_num)):
            ra_next_rad = ra_now_rad + ra_step_rad
            dec_next_rad = dec_now_rad + dec_step_rad

            ra_dec_next_deg = RaDecDegCoord_deg(
                right_ascension_deg = ra_next_rad/np.pi*180,
                declination_deg = dec_next_rad/np.pi*180
            
            )


            v1 = get_transformed_vector(ra_dec_now_deg, center_Dec_deg, center_ra_deg, zrot_deg)
            theta_R1 = polar_upproject(v1)

            v2 = get_transformed_vector(ra_dec_next_deg, center_Dec_deg, center_ra_deg, zrot_deg)
            theta_R2 = polar_upproject(v2)

            theta1=theta_R1[0]
            theta2=theta_R2[0]
            R1=theta_R1[1]
            R2=theta_R2[1]
            ax.plot([theta1,theta2],[R1,R2],linewidth=0.5,linestyle="-",alpha=1,color=line.color)

            ra_now_rad = ra_next_rad
            dec_now_rad = dec_next_rad





def plot_borders_str_grph(borders: list[SkyLine], center_Dec_deg,center_ra_deg,zrot_deg, ax):
    used_borders = []
    for idx,line in enumerate(borders):
        if idx%100 == 0:
            print(f"str_graph_borders:\t{idx/len(borders)*100:.2f}%")

        ra1_rad  = line.point_data_1.ra_dec_deg.right_ascension_deg/180*pi
        dec1_rad = line.point_data_1.ra_dec_deg.declination_deg/180*pi
        ra2_rad  = line.point_data_2.ra_dec_deg.right_ascension_deg/180*pi
        dec2_rad = line.point_data_2.ra_dec_deg.declination_deg/180*pi


        # print(f"ra1= {ra1:.3f}\tra2= {ra2:.3f}\tdec1= {dec1:.3f}\tdec2= {dec2:.3f}")

        line_not_used = [[ra1_rad,dec1_rad],[ra2_rad,dec2_rad]] not in used_borders and [[ra2_rad,dec2_rad],[ra1_rad,dec1_rad]] not in used_borders

        if line_not_used:

            used_borders.append([[ra1_rad,dec1_rad],[ra2_rad,dec2_rad]])       

            ra_diff_rad = (ra2_rad-ra1_rad)
            if abs(ra_diff_rad)>pi:
                if ra1_rad<ra2_rad:
                    ra1_rad=ra1_rad+2*pi
                else:
                    ra1_rad=ra1_rad-2*pi  
                ra_diff_rad = (ra2_rad-ra1_rad)

            dec_diff_rad = (dec2_rad-dec1_rad)
            if abs(dec_diff_rad)>pi:
                if dec1_rad<dec2_rad:
                    dec1_rad=dec1_rad+2*pi
                else:
                    dec1_rad=dec1_rad-2*pi   
                dec_diff_rad = (dec2_rad-dec1_rad)
            iteration_num = max((np.floor(abs(ra_diff_rad)/(2*np.pi)*360))+1 , (np.floor(abs(dec_diff_rad)/(2*np.pi)*360))+1)

            ra_step_rad = ra_diff_rad/iteration_num
            dec_step_rad = dec_diff_rad/iteration_num
            ra_now_rad = ra1_rad
            dec_now_rad = dec1_rad

            for i in range(int(iteration_num)):
                ra_next_rad = ra_now_rad + ra_step_rad
                dec_next_rad = dec_now_rad + dec_step_rad

                ra_dec_now_deg = RaDecDegCoord_deg(right_ascension_deg=ra_now_rad/np.pi*180,
                                                   declination_deg=dec_now_rad/np.pi*180)

                v1 = get_transformed_vector(ra_dec_now_deg, center_Dec_deg, center_ra_deg, zrot_deg)
                # theta_R1 = polar_upproject(v1)
                x_y_z__1 = upproject(v1)

                ra_dec_next_deg = RaDecDegCoord_deg(right_ascension_deg=    ra_next_rad/np.pi*180,
                                                    declination_deg=        dec_next_rad/np.pi*180)

                v2 = get_transformed_vector(ra_dec_next_deg, center_Dec_deg, center_ra_deg, zrot_deg)
                # theta_R2 = polar_upproject(v2)
                x_y_z__2 = upproject(v2)


                x1=x_y_z__1[0]
                x2=x_y_z__2[0]
                y1=x_y_z__1[1]
                y2=x_y_z__2[1]
                color="red"
                plt.plot([y1,y2],[x1,x2],linewidth=0.5,linestyle="-",alpha=1,color=color)

                ra_now_rad = ra_next_rad
                dec_now_rad = dec_next_rad



        


def get_a_fragmented_line(iteration_num, line, ra_step_rad, dec_step_rad, center_Dec_deg, center_ra_deg, zrot_deg):
    ra1_rad  = line.point_data_1.ra_dec_deg.right_ascension_deg/180*pi
    dec1_rad = line.point_data_1.ra_dec_deg.declination_deg/180*pi

    ra_now_rad = ra1_rad    
    dec_now_rad = dec1_rad

    one_line=[]

    for i in range(int(iteration_num)):
        ra_next_rad = ra_now_rad + ra_step_rad
        dec_next_rad = dec_now_rad + dec_step_rad

        ra_dec_now_deg = RaDecDegCoord_deg(right_ascension_deg=ra_now_rad/np.pi*180,
                                            declination_deg=dec_now_rad/np.pi*180)

        v1 = get_transformed_vector(ra_dec_now_deg, center_Dec_deg, center_ra_deg, zrot_deg)
        # theta_R1 = polar_upproject(v1)
        x_y_z__1 = upproject(v1)

        ra_dec_next_deg = RaDecDegCoord_deg(right_ascension_deg=    ra_next_rad/np.pi*180,
                                            declination_deg=        dec_next_rad/np.pi*180)

        v2 = get_transformed_vector(ra_dec_next_deg, center_Dec_deg, center_ra_deg, zrot_deg)
        # theta_R2 = polar_upproject(v2)
        x_y_z__2 = upproject(v2)


        x1=x_y_z__1[0]
        x2=x_y_z__2[0]
        y1=x_y_z__1[1]
        y2=x_y_z__2[1]
        color="red"
        one_line.append((y1,x1))

        # plt.plot([y1,y2],[x1,x2],linewidth=0.5,linestyle="-",alpha=1,color=color)

        ra_now_rad = ra_next_rad
        dec_now_rad = dec_next_rad

    return one_line



def get_radec_step_rad(line: SkyLine):
    ra1_rad  = line.point_data_1.ra_dec_deg.right_ascension_deg/180*pi
    dec1_rad = line.point_data_1.ra_dec_deg.declination_deg/180*pi
    ra2_rad  = line.point_data_2.ra_dec_deg.right_ascension_deg/180*pi
    dec2_rad = line.point_data_2.ra_dec_deg.declination_deg/180*pi



    ra_diff_rad = (ra2_rad-ra1_rad)
    if abs(ra_diff_rad)>pi:
        if ra1_rad<ra2_rad:
            ra1_rad=ra1_rad+2*pi
        else:
            ra1_rad=ra1_rad-2*pi  
        ra_diff_rad = (ra2_rad-ra1_rad)

    dec_diff_rad = (dec2_rad-dec1_rad)
    if abs(dec_diff_rad)>pi:
        if dec1_rad<dec2_rad:
            dec1_rad=dec1_rad+2*pi
        else:
            dec1_rad=dec1_rad-2*pi   
        dec_diff_rad = (dec2_rad-dec1_rad)
    iteration_num = max((np.floor(abs(ra_diff_rad)/(2*np.pi)*360))+1 , (np.floor(abs(dec_diff_rad)/(2*np.pi)*360))+1)

    ra_step_rad = ra_diff_rad/iteration_num
    dec_step_rad = dec_diff_rad/iteration_num

    return ra_step_rad, dec_step_rad, iteration_num

@dataclass
class OnePieceOfPuzzle():
    border: ClosedDrawing
    lines: list[ClosedDrawing]


    def plot_my_drawing(self):
        self.border.just_plot_dont_show()

        for line in self.lines:
            line.just_plot_dont_show()
        plt.axis("equal")
        plt.show()


def plot_borders_str_grph_3D(borders: ListOfSkylines, constellation_lines: ListOfSkylines, center_Dec_deg,center_ra_deg,zrot_deg, ax):

    multiplier = 103.27
    clearance = 0.02
    base_thickness_mm = 2
    line_depth_mm = 0.1
    stripe_width = 0.001

    # borders.print_points()
    list_of_separated_constellations = borders.get_a_list_of_separated_constellations()
    # print(list_of_separated_constellations)
    # import time
    # time.sleep(10000)
    # list_of_separated_constellations = ["UMI", "DRA", "CAS"]
    # list_of_separated_constellations = ["DRA", "LMI"]
    # list_of_separated_constellations = ['CAS', 'AND', 'CVN', 'CMI', 'DRA', 'LMI', 'CNC', 'GEM', 'ARI', 'CAM', 'BOO', 'AUR', 'PEG', 'PER', 'CEP', 'COM', 'LAC', 'HER', 'EQU', 'TRI', 'LYN', 'UMI', 'CYG', 'LYR', 'SGE', 'VUL', 'DEL', 'UMA', 'CRB', 'SER1']
    # list_of_separated_constellations = ['LMI', 'CNC', 'GEM', 'ARI', 'CAM', 'BOO']


    remover_element_list=[]
    for constellation in list_of_separated_constellations:
        stripes: list[ClosedDrawing] = []

        print(constellation)

        only_given_lines: list[SkyLine]
        only_given_lines = constellation_lines.get_only_the_borders_from_this_constellation(constellation)
        for line in only_given_lines:

            v1 = get_transformed_vector(line.point_data_1.ra_dec_deg,center_Dec_deg, center_ra_deg, zrot_deg)
            xyz_1 = upproject(v1)

            v2 = get_transformed_vector(line.point_data_2.ra_dec_deg,center_Dec_deg, center_ra_deg, zrot_deg)
            xyz_2 = upproject(v2)

            x1=xyz_1[0]
            x2=xyz_2[0]
            y1=xyz_1[1]
            y2=xyz_2[1]

            start_point = Vector(x=x1,y=y1,z=0)
            end_point = Vector(x=x2, y=y2, z=0)
            descartes_line = Line(start_point=start_point,end_point=end_point)

            stripe = descartes_line.get_stripe(width=stripe_width)
            stripes.append(stripe)

            dots = descartes_line.get_dots(width=stripe_width)
            stripes.append(dots[0])
            stripes.append(dots[1])

        for stripe in stripes:
            stripe = stripe.multiply_with_scalar(multiplier)



        # remover_poly = Polygon(lines[0].points)
        # remover_element = trimesh.creation.extrude_polygon(remover_poly, height = line_depth_mm)
        # remover_element.apply_translation([0, 0, base_thickness_mm-line_depth_mm])
        
        # ultimate_remover = trimesh.boolean.union([remover_element], engine="manifold")
        for idx, line in enumerate(stripes):

            remover_poly = Polygon(line.points)

            remover_element = trimesh.creation.extrude_polygon(remover_poly, height = line_depth_mm)
            remover_element.apply_translation([0, 0, base_thickness_mm-line_depth_mm])
            remover_element_list.append(remover_element)
            # print(remover_element)

            # print(idx)
    ultimate_remover = trimesh.boolean.union(remover_element_list, engine="manifold")




    for constellation in list_of_separated_constellations:

        base_contour = ClosedDrawing(points=[], name=constellation)

        only_given_borders = borders.get_only_the_borders_from_this_constellation(constellation)
        for line in only_given_borders:

            ra_step_rad, dec_step_rad, iteration_num = get_radec_step_rad(line)
            one_line = get_a_fragmented_line(iteration_num, line, ra_step_rad, dec_step_rad, center_Dec_deg, center_ra_deg, zrot_deg)
            base_contour.points.extend(reversed(one_line))



        #define a piece
        one_piece_of_puzzle = OnePieceOfPuzzle(border = base_contour,lines = stripes)

        #scale up
        one_piece_of_puzzle.border.multiply_with_scalar(multiplier)
        for line in one_piece_of_puzzle.lines:
            line.multiply_with_scalar(multiplier)

        #separate and create the base of piece
        base_contour = one_piece_of_puzzle.border
        base_countour_polygon = Polygon(base_contour.points)
        base_countour_polygon = base_countour_polygon.buffer(-clearance)
        base_plate = trimesh.creation.extrude_polygon(base_countour_polygon, height = base_thickness_mm)



        #remove the things
        base_plate = trimesh.boolean.difference([base_plate, ultimate_remover],engine="manifold")   

        combined = base_plate

        # # Save as STL
        combined.export(f"{base_contour.name}.stl")
        # to_remove.export(f"{contour.name}.stl")

        print(f"Created {base_contour.name}.stl")

        
        



def plot_stars_polar(const_list,center_Dec_deg,center_ra_deg,zrot_deg,hmg,hmg2,a):
    x_list=[]
    y_list=[]
    S_list=[]
    alpha_list=[]

    # star_color="orange"
    star_color2="black"
    star_color="black"
    for list_elem in const_list:
        for i,star in enumerate(list_elem):
            ra  = star['Right Ascension (deg)']/180*np.pi
            dec = star['Declination (deg)']/180*np.pi
            v = get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
            theta_R = polar_upproject(v)
            S,marker,alpha = condition_magnitudes(star,hmg,hmg2)
            plt.scatter(theta_R[0], theta_R[1], c="black", marker=marker, s=a*(1+hmg-S), alpha=alpha, zorder=ORDER_OF_STARS_MINOR)






def plot_cylindrical_stars(const_list,center_Dec_deg,center_ra_deg,zrot_deg,hmg,hmg2,a):
    x_list=[]
    y_list=[]
    S_list=[]
    alpha_list=[]

    # star_color="orange"
    star_color2="black"
    star_color="black"
    for list_elem in const_list:
        for i,star in enumerate(list_elem):


            ra_dec_coord = RaDecDegCoord_deg(
            right_ascension_deg=star['Right Ascension (deg)'],
            declination_deg=star['Declination (deg)']
            )

            v = get_transformed_vector(ra_dec_coord,center_Dec_deg, center_ra_deg, zrot_deg)
            
            x_y_z = cylindrical_project(v)

            S,marker,alpha = condition_magnitudes(star,hmg,hmg2)
            s=a*(1+hmg-S)
            x=x_y_z[0]
            y=x_y_z[1]

            if x<0:
                x=x+2*np.pi
            
            if marker == ".":
                S_list.append(s)

                x_list.append(x)
                y_list.append(y)
                alpha_list.append(alpha)
            else:
                plt.scatter(x, y, color=star_color,  s=s, marker=marker, alpha=alpha, zorder=ORDER_OF_STARS_MAJOR)  
                plt.scatter(x-2*pi, y, color=star_color,  s=s, marker=marker, alpha=alpha, zorder=ORDER_OF_STARS_MAJOR) 


    plt.scatter(x_list, y_list, color=star_color2,  s=S_list, marker=".", alpha=alpha_list, zorder=ORDER_OF_STARS_MINOR)
    # plt.scatter(x_y_z[0]+2*pi, x_y_z[1], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha, zorder=3)
    plt.scatter(x_list-2*pi*np.ones(len(x_list)), y_list, color=star_color2,  s=a*(1+hmg-S), marker=marker, alpha=alpha_list, zorder=ORDER_OF_STARS_MINOR)
    # y.append(x_y_z[1])
    # x.append(x_y_z[0])

ecliptic_color="#ddddddff"
def plot_cylindrical_ecliptic(const_list,center_Dec_deg,center_ra_deg,zrot_deg,hmg,hmg2,a):
    x_list=[]
    y_list=[]
    S_list=[]
    alpha_list=[]

    star_color="orange"
    star_color2="black"
    for list_elem in const_list:
        for i,star in enumerate(list_elem):

            ra_dec_coord = RaDecDegCoord_deg(
            right_ascension_deg=star['Right Ascension (deg)'],
            declination_deg=star['Declination (deg)']
            )

            v = get_transformed_vector(ra_dec_coord,center_Dec_deg, center_ra_deg, zrot_deg)
            x_y_z = cylindrical_project(v)

            S,marker,alpha = condition_magnitudes(star,hmg,hmg2)
            s=a*(1+hmg-S)
            x=x_y_z[0]
            y=x_y_z[1]

            if x<0:
                x=x+2*np.pi
            
            S_list.append(s)

            x_list.append(x)
            y_list.append(y)
            alpha_list.append(alpha)

    x_wrapped = np.concatenate([np.array(x_list) - 2*np.pi, x_list])
    y_wrapped = np.concatenate([y_list, y_list])

    idx = np.argsort(x_wrapped)

    x_list = x_wrapped[idx]
    y_list = y_wrapped[idx]


    # plt.scatter(x_list, y_list, color=star_color2,  s=1, marker=".", alpha=1, zorder=5)
    
    for i in range(len(x_list)-1):
        plt.plot([x_list[i],x_list[i+1]],[y_list[i],y_list[i+1]],linewidth=1.0,linestyle="-",alpha=1,color=ecliptic_color,zorder=ORDER_OF_ECLIPTIC_LINE)



def plot_cylindrical_equinox(const_list,center_Dec_deg,center_ra_deg,zrot_deg,hmg,hmg2,a):
    star_color=ecliptic_color

    for list_elem in const_list:
        for i,star in enumerate(list_elem):

            ra_dec_coord = RaDecDegCoord_deg(
            right_ascension_deg=star['Right Ascension (deg)'],
            declination_deg=star['Declination (deg)']
            )

            v = get_transformed_vector(ra_dec_coord,center_Dec_deg, center_ra_deg, zrot_deg)
            x_y_z = cylindrical_project(v)

            S=1
            lw = 1.5
            x=x_y_z[0]
            y=x_y_z[1]

            if x<0:
                x=x+2*np.pi
            
            plt.scatter(x, y, color=star_color,  s=S, marker="o", alpha=1, zorder=ORDER_OF_STARS_MAJOR,linewidths=lw)   # <— skinny!)  
            plt.scatter(x-2*pi, y, color=star_color,  s=S, marker="o", alpha=1, zorder=ORDER_OF_STARS_MAJOR,linewidths=lw)   # <— skinny!) 



def plot_cylindrical_lines(lines: list[SkyLine],center_Dec_deg,center_ra_deg,zrot_deg,*,Break_line=0):
    
    segmentation_flag = False
    lines_to_print_list=[]
    # alpha_list=[]
    width_list=[]
    for idx,line in enumerate(lines):
        if idx%10 == 0:
            print(f"cylindrical lines:\t{idx/len(lines)*100:.2f}%")

        v1 = get_transformed_vector(line.point_data_1.ra_dec_deg,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_1 = cylindrical_project(v1)


        v2 = get_transformed_vector(line.point_data_2.ra_dec_deg,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_2 = cylindrical_project(v2)

        x1=xyz_1[0]
        x2=xyz_2[0]
        y1=xyz_1[1]
        y2=xyz_2[1]

        if abs(x1-x2)>np.pi:    
            segmentation_flag = True
            print("FLAG!!!")

        lines_to_print_list.append([[x1,x2],[y1,y2]])
        width_list.append(line.width)
        # alpha_list.append(alpha)


    for idx,lines_to_print in enumerate(lines_to_print_list):

        x1 = lines_to_print[0][0]       
        x2 = lines_to_print[0][1]
        y1 = lines_to_print[1][0]
        y2 = lines_to_print[1][1]

        if segmentation_flag:
            if x1<0:
                x1=x1+2*np.pi
            if x2<0:
                x2=x2+2*np.pi

        teasing_lines = False

        width=width_list[idx]
        if width == "1":
            width=0.6  
        else:
            width = 0.4

        if teasing_lines:
            # R=0.02
            R=0.0
            
            v1 = np.array([x1,y1,0])
            v2 = np.array([x2,y2,0])
            if abs_vector(v1-v2)> 2*R:
                v3 = norm_vector(v2-v1)*R
                v10 = v1 + v3
                v20 = v2 - v3

                x1,y1,_ = disolve_vector(v10)
                x2,y2,_ = disolve_vector(v20)

                plt.plot([x1,x2],[y1,y2],linewidth=width,linestyle=line.linestyle ,alpha=1,color=line.color,zorder=ORDER_OF_LINES)
        else:   
            plt.plot([x1,x2],[y1,y2],linewidth=width,linestyle=line.linestyle, alpha=1,color=line.color,zorder=ORDER_OF_LINES)

def revese_line_params(line_params):
    ra10 = line_params[0][0]
    ra20 = line_params[0][1]

    dec10 = line_params[1][0]
    dec20 = line_params[1][1]

    reversed_line_param = [ra20,ra10],[dec20,dec10]
    return reversed_line_param

def is_not_yet_used_line(line_params,used_borders_list):
    reversed_line_param = revese_line_params(line_params)          

    if (line_params not in used_borders_list) and (reversed_line_param not in used_borders_list):
        return True
    else:
        return False



def plot_cylindrical_borders(border_line_list: list[SkyLine], center_Dec_deg,center_ra_deg,zrot_deg, used_borders_list):
    # used_borders=[]
    crossing_border_flag = False
    break_flag = False
    segmented_lines_to_print_list=[]
    possibly_broken_lines_list=[]
    unsegmented_lines_to_print_list=[]
    current_constellation_used_lines=[]

    for idx,border_line in enumerate(border_line_list):
        
        v1 = get_transformed_vector(border_line.point_data_1.ra_dec_deg,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_1 = cylindrical_project(v1)

        v2 = get_transformed_vector(border_line.point_data_2.ra_dec_deg,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_2 = cylindrical_project(v2)

        x1=xyz_1[0]
        x2=xyz_2[0]
        y1=xyz_1[1]
        y2=xyz_2[1]

        if abs(x1-x2)>np.pi:    
            break_flag = True
            print("FLAG!!!")

        possibly_boken_line = [x1,x2],[y1,y2]

        possibly_broken_lines_list.append(possibly_boken_line)
    
    for possibly_boken_line in possibly_broken_lines_list:

        x1 = possibly_boken_line[0][0]       
        x2 = possibly_boken_line[0][1]
        y1 = possibly_boken_line[1][0]
        y2 = possibly_boken_line[1][1]

        if break_flag:
            if x1<0:
                x1=x1+2*np.pi
            if x2<0:
                x2=x2+2*np.pi

        unsegmented_line = [x1,x2],[y1,y2]

        unsegmented_lines_to_print_list.append(unsegmented_line)

        
        if is_not_yet_used_line(unsegmented_line,used_borders_list):
            
            used_borders_list.append(unsegmented_line)  
            current_constellation_used_lines.append(unsegmented_line)




    for line_coordinate in current_constellation_used_lines:
        x_coordinates = line_coordinate[0]+np.random.random(2)/20*0
        y_coordinates = line_coordinate[1]+np.random.random(2)/20*0
        
        plt.plot(x_coordinates, y_coordinates, linewidth=0.5, linestyle="-", alpha=1, color="red", zorder=ORDER_OF_BORDES)

