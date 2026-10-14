import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi
from dataclasses import dataclass, field
import trimesh
from shapely.geometry import Polygon


ORDER_OF_ECLIPTIC_LINE  = 0
ORDER_OF_LINES          = 1
ORDER_OF_STARS_MINOR    = 2
ORDER_OF_STARS_MAJOR    = 3
ORDER_OF_BORDES         = 4


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

    def get_dots(self, width=0.005, thickness=1, offset=1): #->ClosedDrawing:
        
        edge_points = []
        for i in range(0,360,20):
            edge_point0 = self + Vector(x=width*np.cos(i/180*np.pi), y=width*np.sin(i/180*np.pi), z=0)
            edge_points.append(Vector(edge_point0.y, edge_point0.x,0))

        output_closed_drawig = ClosedDrawing(points = edge_points, name ="", thickness = thickness, offset = offset)
                
        return output_closed_drawig

    def get_star_shaped_dots(self, width=0.005, thickness=1, offset=1): #->ClosedDrawing:
        
        edge_points = []
        for i in range(0,360,5):
            R = 1+0.25 * np.sin(5*i/180*np.pi) - 0.1* np.cos(10*i/180*np.pi)
            edge_point0 = self + Vector(x = width*np.cos(i/180*np.pi)*R, 
                                        y = width*np.sin(i/180*np.pi)*R, 
                                        z = 0)
            edge_points.append(Vector(edge_point0.y, edge_point0.x,0))

        output_closed_drawig = ClosedDrawing(points = edge_points, name ="", thickness = thickness, offset = offset)
                
        return output_closed_drawig

    def __repr__(self):
        str = f"({self.x}; {self.y}; {self.z})"
        return str

    

@dataclass
class ProjVals():
    center_Dec_deg: float
    center_ra_deg: float
    zrot_deg: float

@dataclass
class ClosedDrawing():
    points: list[Vector] = field(default_factory=list)
    name: str = ""
    thickness: float = 1
    offset: float = 0

    def just_plot_dont_show(self, colour = "black"):
        self.points.append(self.points[0])
        for idx in range(len(self.points)-1):
            A=self.points[idx]
            B=self.points[idx+1]

            plt.plot([A.y,B.y],[A.x,B.x],marker = "o", color=colour)

    def plot_my_drawing(self):
        self.just_plot_dont_show()
        plt.show()

    def multiply_with_scalar(self,a):
        out_list=[]
        for idx, p in enumerate(self.points):
            # print(self.points[idx][0])
            out_list.append(Vector(p.x*a, p.y*a, 0))

        self.points = out_list

    def print(self):
        for p in self.points:
            print(p)

    def get_diffs(self)-> list[Vector]:
        work_vectors = self.points
        work_vectors.append(work_vectors[0])

        diff = []
        for i in range(len(work_vectors)-1):
            diff.append(work_vectors[i+1]-work_vectors[i])
        
        return diff

    def is_this_segmented(self) -> bool:
        diff = self.get_diffs()
        for d in diff:
            if d.abs()> np.pi:
                return True
        return False


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
class ConstellationNameAndAbbrev():
    fullname: str
    abbrev: str

list_of_const_names = [

    ConstellationNameAndAbbrev("Columba_Caelum", "COL_CAE"),
    ConstellationNameAndAbbrev("Delphinus_Equuleus", "DEL_EQU"),
    ConstellationNameAndAbbrev("Monoceros_Canis Minor", "MON_CMI"),
    ConstellationNameAndAbbrev("Sagitta_Vulpecula", "SGE_VUL"),
    ConstellationNameAndAbbrev("Scutum_Serpens_cauda", "SCT_SER2"),

    ConstellationNameAndAbbrev("Andromeda", "AND"),
    ConstellationNameAndAbbrev("Antlia", "ANT"),
    ConstellationNameAndAbbrev("Apus", "APS"),
    ConstellationNameAndAbbrev("Aquarius", "AQR"),
    ConstellationNameAndAbbrev("Aquila", "AQL"),
    ConstellationNameAndAbbrev("Ara", "ARA"),
    ConstellationNameAndAbbrev("Aries", "ARI"),
    ConstellationNameAndAbbrev("Auriga", "AUR"),
    ConstellationNameAndAbbrev("Boötes", "BOO"),
    ConstellationNameAndAbbrev("Caelum", "CAE"),
    ConstellationNameAndAbbrev("Camelopardalis", "CAM"),
    ConstellationNameAndAbbrev("Cancer", "CNC"),
    ConstellationNameAndAbbrev("Canes Venatici", "CVN"),
    ConstellationNameAndAbbrev("Canis Major", "CMA"),
    ConstellationNameAndAbbrev("Canis Minor", "CMI"),
    ConstellationNameAndAbbrev("Capricornus", "CAP"),
    ConstellationNameAndAbbrev("Carina", "CAR"),
    ConstellationNameAndAbbrev("Cassiopeia", "CAS"),
    ConstellationNameAndAbbrev("Centaurus", "CEN"),
    ConstellationNameAndAbbrev("Cepheus", "CEP"),
    ConstellationNameAndAbbrev("Cetus", "CET"),
    ConstellationNameAndAbbrev("Chamaeleon", "CHA"),
    ConstellationNameAndAbbrev("Circinus", "CIR"),
    ConstellationNameAndAbbrev("Columba", "COL"),
    ConstellationNameAndAbbrev("Coma Berenices", "COM"),
    ConstellationNameAndAbbrev("Corona Australis", "CRA"),
    ConstellationNameAndAbbrev("Corona Borealis", "CRB"),
    ConstellationNameAndAbbrev("Corvus", "CRV"),
    ConstellationNameAndAbbrev("Crater", "CRT"),
    ConstellationNameAndAbbrev("Crux", "CRU"),
    ConstellationNameAndAbbrev("Cygnus", "CYG"),
    ConstellationNameAndAbbrev("Delphinus", "DEL"),
    ConstellationNameAndAbbrev("Dorado", "DOR"),
    ConstellationNameAndAbbrev("Draco", "DRA"),
    ConstellationNameAndAbbrev("Equuleus", "EQU"),
    ConstellationNameAndAbbrev("Eridanus", "ERI"),
    ConstellationNameAndAbbrev("Fornax", "FOR"),
    ConstellationNameAndAbbrev("Gemini", "GEM"),
    ConstellationNameAndAbbrev("Grus", "GRU"),
    ConstellationNameAndAbbrev("Hercules", "HER"),
    ConstellationNameAndAbbrev("Horologium", "HOR"),
    ConstellationNameAndAbbrev("Hydra", "HYA"),
    ConstellationNameAndAbbrev("Hydrus", "HYI"),
    ConstellationNameAndAbbrev("Indus", "IND"),
    ConstellationNameAndAbbrev("Lacerta", "LAC"),
    ConstellationNameAndAbbrev("Leo", "LEO"),
    ConstellationNameAndAbbrev("Leo Minor", "LMI"),
    ConstellationNameAndAbbrev("Lepus", "LEP"),
    ConstellationNameAndAbbrev("Libra", "LIB"),
    ConstellationNameAndAbbrev("Lupus", "LUP"),
    ConstellationNameAndAbbrev("Lynx", "LYN"),
    ConstellationNameAndAbbrev("Lyra", "LYR"),
    ConstellationNameAndAbbrev("Mensa", "MEN"),
    ConstellationNameAndAbbrev("Microscopium", "MIC"),
    ConstellationNameAndAbbrev("Monoceros", "MON"),
    ConstellationNameAndAbbrev("Musca", "MUS"),
    ConstellationNameAndAbbrev("Norma", "NOR"),
    ConstellationNameAndAbbrev("Octans", "OCT"),
    ConstellationNameAndAbbrev("Ophiuchus", "OPH"),
    ConstellationNameAndAbbrev("Orion", "ORI"),
    ConstellationNameAndAbbrev("Pavo", "PAV"),
    ConstellationNameAndAbbrev("Pegasus", "PEG"),
    ConstellationNameAndAbbrev("Perseus", "PER"),
    ConstellationNameAndAbbrev("Phoenix", "PHE"),
    ConstellationNameAndAbbrev("Pictor", "PIC"),
    ConstellationNameAndAbbrev("Pisces", "PSC"),
    ConstellationNameAndAbbrev("Piscis Austrinus", "PSA"),
    ConstellationNameAndAbbrev("Puppis", "PUP"),
    ConstellationNameAndAbbrev("Pyxis", "PYX"),
    ConstellationNameAndAbbrev("Reticulum", "RET"),
    ConstellationNameAndAbbrev("Sagitta", "SGE"),
    ConstellationNameAndAbbrev("Sagittarius", "SGR"),
    ConstellationNameAndAbbrev("Scorpius", "SCO"),
    ConstellationNameAndAbbrev("Sculptor", "SCL"),
    ConstellationNameAndAbbrev("Scutum", "SCT"),
    ConstellationNameAndAbbrev("Serpens", "SER"),
    ConstellationNameAndAbbrev("Sextans", "SEX"),
    ConstellationNameAndAbbrev("Taurus", "TAU"),
    ConstellationNameAndAbbrev("Telescopium", "TEL"),
    ConstellationNameAndAbbrev("Triangulum", "TRI"),
    ConstellationNameAndAbbrev("Triangulum Australe", "TRA"),
    ConstellationNameAndAbbrev("Tucana", "TUC"),
    ConstellationNameAndAbbrev("Ursa Major", "UMA"),
    ConstellationNameAndAbbrev("Ursa Minor", "UMI"),
    ConstellationNameAndAbbrev("Vela", "VEL"),
    ConstellationNameAndAbbrev("Virgo", "VIR"),
    ConstellationNameAndAbbrev("Volans", "VOL"),
    ConstellationNameAndAbbrev("Vulpecula", "VUL"),


]



@dataclass
class SkyPoint():
    name: str
    ra_dec_deg: RaDecDegCoord_deg
    apparent_mag: float
    constellation: str

    def __repr__(self):
        ra1 = self.ra_dec_deg.right_ascension_deg
        dec1 = self.ra_dec_deg.declination_deg

        return f"({ra1:.2f}, {dec1:.2f})"

    def correct_name(self):
        for const in list_of_const_names:
            if self.constellation == const.fullname:
                self.constellation = const.abbrev

        

@dataclass
class ListOfSkypoints():

    list_of_skypoints: list[SkyPoint]

    def get_only_the_stars_from_this_constellation(self, constellation: str):
        output_borders = []
        for i in self.list_of_skypoints:
            if (i.constellation == constellation):
                output_borders.append(i)
        return(ListOfSkypoints(output_borders))

    def get_a_list_of_separated_constellations(self):
        constellation_already_used = []
        for i in self.list_of_skypoints:
            if not (i.constellation in constellation_already_used):
                constellation_already_used.append(i.constellation)
        return(constellation_already_used)

    def print_points(self):
        for i in self.list_of_skypoints:
            print(i)


@dataclass
class SkyLine():
    point_data_1: SkyPoint
    point_data_2: SkyPoint

    linestyle: str = ""
    color: str = ""
    width: str = ""
    alpha: str = ""

    def __repr__(self):
        s1 = self.point_data_1
        s2 = self.point_data_2
        return f"{s1} - {s2}"

@dataclass
class ListOfSkylines():

    list_of_skylines: list[SkyLine]

    def get_only_the_lines_realted_to_this_constellation(self, constellation: str):
        output_borders = []
        for i in self.list_of_skylines:
            i.point_data_1.correct_name()
            # print(f"#{i.point_data_1.constellation}# =? #{constellation}# : {i.point_data_1.constellation == constellation}")
            if (i.point_data_1.constellation == constellation):
                output_borders.append(i)
        return(ListOfSkylines(output_borders))

    def get_a_list_of_separated_constellations(self) -> list[str]:
        constellation_already_used = []
        for i in self.list_of_skylines:
            if not (i.point_data_1.constellation in constellation_already_used):
                constellation_already_used.append(i.point_data_1.constellation)
        return(constellation_already_used)

    def print_points(self):
        for i in self.list_of_skylines:
            print(i)





@dataclass
class Line():
    start_point: Vector
    end_point: Vector


    def get_stripe(self, width=0.005, thickness=1, offset=1)->ClosedDrawing:
        dir = self.end_point - self.start_point
        step_aside_vector = Vector(x=dir.y, y=-1*dir.x, z = 0)
        step_aside_vector = width*(step_aside_vector.norm())

        A = self.start_point + step_aside_vector
        B = A+ dir
        C = B-2*step_aside_vector
        D = C -dir        

        points=[]
        points.append(Vector(A.y, A.x, 0))
        points.append(Vector(B.y, B.x, 0))
        points.append(Vector(C.y, C.x, 0))
        points.append(Vector(D.y, D.x, 0))


        return ClosedDrawing(points=points,name ="",thickness=thickness,offset=offset)


    def get_dots(self, width=0.005, thickness=1, offset=1)->list[ClosedDrawing]:
        
        output_closed_drawig_list=[]
        for point in [self.start_point, self.end_point]:

            output_closed_drawig_list.append(point.get_dots())    
                
        return output_closed_drawig_list

    def get_stripes_and_dots(self, width=0.005, thickness=1, offset=0) -> list[ClosedDrawing]:
        out = []
        out.append(self.get_stripe(width, thickness, offset))
        out.extend(self.get_dots(width, thickness, offset))
        return out

    def len(self):
        diff_vec = self.end_point - self.start_point
        return diff_vec.abs()


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

def get_transformed_vector(ra_dec_coord_deg: RaDecDegCoord_deg, proj_vals: ProjVals):   
    ra = ra_dec_coord_deg.right_ascension_deg/180*np.pi
    dec = ra_dec_coord_deg.declination_deg/180*np.pi
    v = get_3d_vec_from_RaDec(ra,dec)
    v = center_to_RaDec(v, proj_vals.center_Dec_deg, proj_vals.center_ra_deg)
    v = zrot(v, proj_vals.zrot_deg)
    return v

def get_transformed_vector_from3d(v: np.ndarray, proj_vals: ProjVals):   
    v = center_to_RaDec(v, proj_vals.center_Dec_deg, proj_vals.center_ra_deg)
    v = zrot(v, proj_vals.zrot_deg)
    return v

def condition_magnitudes(star: SkyPoint, hmg, hmg2):
    if star.apparent_mag <= hmg:
        S=star.apparent_mag
        alpha=1
    else:
        S=hmg
        alpha=0.5
    if star.apparent_mag <= hmg2:
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



def plot_lines_polar(lines: list[SkyLine], proj_vals: ProjVals, ax):
    for idx,line in enumerate(lines):
        print(f"polar lines:\t{idx/len(lines)*100:.2f}%")

        v1 = get_transformed_vector(line.point_data_1.ra_dec_deg, proj_vals)
        theta_R1 = polar_upproject(v1)

        v2 = get_transformed_vector(line.point_data_2.ra_dec_deg, proj_vals)
        theta_R2 = polar_upproject(v2)

        theta1=theta_R1[0]
        theta2=theta_R2[0]
        R1=theta_R1[1]
        R2=theta_R2[1]
        ax.plot([theta1,theta2],[R1,R2],linewidth=line.width,linestyle=line.linestyle,alpha=1,color=line.color,zorder=ORDER_OF_LINES)

             

def plot_borders_polar(borders: list[SkyLine], proj_vals: ProjVals, ax):
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


            v1 = get_transformed_vector(ra_dec_now_deg, proj_vals)
            theta_R1 = polar_upproject(v1)

            v2 = get_transformed_vector(ra_dec_next_deg, proj_vals)
            theta_R2 = polar_upproject(v2)

            theta1=theta_R1[0]
            theta2=theta_R2[0]
            R1=theta_R1[1]
            R2=theta_R2[1]
            ax.plot([theta1,theta2],[R1,R2],linewidth=0.5,linestyle="-",alpha=1,color=line.color)

            ra_now_rad = ra_next_rad
            dec_now_rad = dec_next_rad








        


def get_a_fragmented_line(iteration_num, line, ra_step_rad, dec_step_rad, proj_vals: ProjVals):
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

        v1 = get_transformed_vector(ra_dec_now_deg, proj_vals)
        # theta_R1 = polar_upproject(v1)
        x_y_z__1 = upproject(v1)

        ra_dec_next_deg = RaDecDegCoord_deg(right_ascension_deg=    ra_next_rad/np.pi*180,
                                            declination_deg=        dec_next_rad/np.pi*180)

        v2 = get_transformed_vector(ra_dec_next_deg, proj_vals)
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
class ListOfLines():
    list_of_lines: list[Line] = field(default_factory=list)

    def is_this_segmented(self) -> bool:
        if len(self.list_of_lines) == 0:
            return False
        # print(self.list_of_lines)
        for l in self.list_of_lines:

            if l.len()> np.pi:
                return True
        return False

    def __repr__(self) -> str:
        return "\n".join(str(l) for l in self.list_of_lines)

@dataclass
class ListOfVectors():
    list_of_vector: list[Vector] = field(default_factory=list)

    def get_full_graph(self) -> ListOfLines:
        out=[]
        for v1 in self.list_of_vector:
            for v2 in self.list_of_vector:
                line = Line(v1,v2)
                out.append(line)
        return ListOfLines(out)


    def is_this_segmented(self) -> bool:
        full_graph = self.get_full_graph()
        return full_graph.is_this_segmented()

    # def __repr__(self)->str:
    #     out=self.list_of_vector
    def __repr__(self) -> str:
        return "\n".join(str(l) for l in self.list_of_vector)


@dataclass
class OnePieceOfPuzzle():
    border: ClosedDrawing = field(default_factory=ClosedDrawing)

    line_skeleton: ListOfLines = field(default_factory=ListOfLines)
    line_contours: list[ClosedDrawing] =  field(default_factory=list)

    star_points: ListOfVectors  = field(default_factory=ListOfVectors)
    star_contours: list[ClosedDrawing] =  field(default_factory=list)
    name: str = ""


    def plot_my_drawing(self, save: bool = False, dest = ""):
        if dest == "":
            dest = f"{self.name}.png"

        self.border.just_plot_dont_show()


        for line in self.line_contours:
            line.just_plot_dont_show(colour="C00")


        for star in self.star_contours:
            star.just_plot_dont_show(colour="C01")


        plt.title(self.border.name)
        plt.axis("equal")
        if save:
            plt.savefig(dest)
            plt.close()
        else:
            plt.show()

    def is_this_piece_segmented(self):
        border_segmented = self.border.is_this_segmented()
        lines_segmented = self.line_skeleton.is_this_segmented()

        stars_segmented = self.star_points.is_this_segmented()

        return border_segmented or lines_segmented or stars_segmented

    def __repr__(self) -> str:
        return (
            f"OnePieceOfPuzzle(name={self.name!r})\n"
            f"Border: {self.border}\n"
            f"Line skeleton: {self.line_skeleton}\n"
            f"Star points: {self.star_points}\n")




def plot_stars_polar(const_list, proj_vals: ProjVals, hmg, hmg2, a):
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
            v = get_transformed_vector(ra,dec, proj_vals)
            theta_R = polar_upproject(v)
            S,marker,alpha = condition_magnitudes(star,hmg,hmg2)
            plt.scatter(theta_R[0], theta_R[1], c="black", marker=marker, s=a*(1+hmg-S), alpha=alpha, zorder=ORDER_OF_STARS_MINOR)







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





def plot_a_list_of_closedDrawing(mylist :list[ClosedDrawing]):
    for l in mylist:
        l.just_plot_dont_show()

    plt.axis("equal")
    plt.show()
    