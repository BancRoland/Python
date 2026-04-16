import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi
from dataclasses import dataclass

ORDER_OF_ECLIPTIC_LINE  = 0
ORDER_OF_LINES          = 1
ORDER_OF_STARS_MINOR    = 2
ORDER_OF_STARS_MAJOR    = 3
ORDER_OF_BORDES         = 4



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

def get_transformed_vector(ra: float,dec: float,center_Dec_deg: float, center_ra_deg: float, zrot_deg: float):   
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



def plot_lines_polar(lines, center_Dec_deg,center_ra_deg,zrot_deg, ax):
    for idx,line in enumerate(lines):
        print(f"polar lines:\t{idx/len(lines)*100:.2f}%")
        ra1  = line['Right Ascension (deg)1']/180*pi
        dec1 = line['Declination (deg)1']/180*np.pi
        ra2  = line['Right Ascension (deg)2']/180*pi
        dec2 = line['Declination (deg)2']/180*np.pi
        linestyle = line['linestyle']
        color = line['color']
        width = line['width']
        alpha = line['alpha']
        
        v1 = get_transformed_vector(ra1,dec1,center_Dec_deg, center_ra_deg, zrot_deg)
        theta_R1 = polar_upproject(v1)

        v2 = get_transformed_vector(ra2,dec2,center_Dec_deg, center_ra_deg, zrot_deg)
        theta_R2 = polar_upproject(v2)

        theta1=theta_R1[0]
        theta2=theta_R2[0]
        R1=theta_R1[1]
        R2=theta_R2[1]
        ax.plot([theta1,theta2],[R1,R2],linewidth=width,linestyle=linestyle,alpha=1,color=color,zorder=ORDER_OF_LINES)

def plot_lines_str_grph(lines, center_Dec_deg,center_ra_deg,zrot_deg, ax):
    for idx,line in enumerate(lines):
        print(f"str_grp lines:\t{idx/len(lines)*100:.2f}%")
        ra1  = line['Right Ascension (deg)1']/180*pi
        dec1 = line['Declination (deg)1']/180*np.pi
        ra2  = line['Right Ascension (deg)2']/180*pi
        dec2 = line['Declination (deg)2']/180*np.pi
        linestyle = line['linestyle']
        color = line['color']
        width = line['width']
        alpha = line['alpha']
        
        v1 = get_transformed_vector(ra1,dec1,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_1 = upproject(v1)

        v2 = get_transformed_vector(ra2,dec2,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_2 = upproject(v2)

        x1=xyz_1[0]
        x2=xyz_2[0]
        y1=xyz_1[1]
        y2=xyz_2[1]
        plt.plot([y1,y2],[x1,x2],linewidth=width,linestyle=linestyle,alpha=0.9,color=color,zorder=ORDER_OF_LINES)
                        
def plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax):
    for idx,line in enumerate(borders):
        if idx%100==0:
            print(f"polar borders:\t{idx/len(borders)*100:.2f}%")
        ra1  = line['Right Ascension (deg)1']/180*pi
        dec1 = line['Declination (deg)1']/180*np.pi
        ra2  = line['Right Ascension (deg)2']/180*pi
        dec2 = line['Declination (deg)2']/180*np.pi
        linestyle = line['linestyle']
        color = line['color']
        width = line['width']
        alpha = line['alpha']

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

            v1 = get_transformed_vector(ra_now,dec_now,center_Dec_deg, center_ra_deg, zrot_deg)
            theta_R1 = polar_upproject(v1)

            v2 = get_transformed_vector(ra_next,dec_next,center_Dec_deg, center_ra_deg, zrot_deg)
            theta_R2 = polar_upproject(v2)

            theta1=theta_R1[0]
            theta2=theta_R2[0]
            R1=theta_R1[1]
            R2=theta_R2[1]
            ax.plot([theta1,theta2],[R1,R2],linewidth=0.5,linestyle="-",alpha=1,color=color)

            ra_now = ra_next
            dec_now = dec_next


def read_borders__gen_graph(borders,center_Dec_deg=90,center_ra_deg=0,zrot_deg=0):
    points = []
    rank_count =[]
    matrix_of_borders=np.zeros([0,0])

    for idx,line in enumerate(borders):
        if idx%10 == 0:
            print(f"gen_graph_borders:\t{idx/len(borders)*100:.2f}%")
        ra1  = line['Right Ascension (deg)1']/180*pi
        dec1 = line['Declination (deg)1']/180*np.pi
        ra2  = line['Right Ascension (deg)2']/180*pi
        dec2 = line['Declination (deg)2']/180*np.pi
        linestyle = line['linestyle']
        color = line['color']
        width = line['width']
        alpha = line['alpha']
        point1 = [ra1, dec1]
        point2 = [ra2, dec2]


        idx_vertex=[None,None]

        for i,p in enumerate([point1, point2]):
            # print(f"point1: {point1}")
            if p not in points:
                points.append(p)
                rank_count.append(1)
                print("NEW found")
                size=len(points)
                idx=size-1
                mx2=np.zeros([size,size])
                mx2[:size-1, :size-1] = matrix_of_borders
                matrix_of_borders=mx2
                # print(matrix_of_borders)
            else:
                idx=points.index(p)
                rank_count[idx]+=1
                print(f"Already found with index: {idx}")
            idx_vertex[i]=idx
        matrix_of_borders[idx_vertex[0],idx_vertex[1]]=1
        matrix_of_borders[idx_vertex[1],idx_vertex[0]]=1
            


    for i,star in enumerate(points):
        ra  = star[0]
        # print(ra)
        dec = star[1]
        # print(dec)
        v = get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
        x_y_z = cylindrical_project(v)

        if rank_count[i] != 4:
            if rank_count[i] == 2:
                color="blue"
            if rank_count[i] == 6:
                color="red"
            if rank_count[i] == 8:
                color="green"
            if rank_count[i] >= 10:
                color="orange"
                
            plt.scatter(x_y_z[0], x_y_z[1], color=color,  s=10, marker="o", alpha=1)

    for i in range(len(points)):
        for j in range(len(points)):
            if i>j:
                if matrix_of_borders[i,j] == 1:
                    point1=points[i]
                    point2=points[j]
                    ra1=point1[0]
                    dec1=point1[1]
                    ra2=point2[0]
                    dec2=point2[1]

                    v1 = get_transformed_vector(ra1,dec1,center_Dec_deg, center_ra_deg, zrot_deg)
                    xyz_1 = cylindrical_project(v1)

                    # v2 = get_transformed_vector(ra2,dec2,center_Dec_deg, center_ra_deg, zrot_deg)
                    # xyz_2 = upproject(v2)

                    v2 = get_transformed_vector(ra2,dec2,center_Dec_deg, center_ra_deg, zrot_deg)
                    xyz_2 = cylindrical_project(v2)

                    x1=xyz_1[0]
                    x2=xyz_2[0]
                    y1=xyz_1[1]
                    y2=xyz_2[1]
                    plt.plot([x1,x2],[y1,y2],linewidth=2,linestyle="-",alpha=0.1,color="black",zorder=ORDER_OF_BORDES)

    plt.show()

           
        



def plot_borders_str_grph(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax):
    used_borders = []
    for idx,line in enumerate(borders):
        if idx%100 == 0:
            print(f"str_graph_borders:\t{idx/len(borders)*100:.2f}%")
        ra1  = line['Right Ascension (deg)1']/180*pi
        dec1 = line['Declination (deg)1']/180*np.pi
        ra2  = line['Right Ascension (deg)2']/180*pi
        dec2 = line['Declination (deg)2']/180*np.pi
        linestyle = line['linestyle']
        color = line['color']
        width = line['width']
        alpha = line['alpha']

        # print(f"ra1= {ra1:.3f}\tra2= {ra2:.3f}\tdec1= {dec1:.3f}\tdec2= {dec2:.3f}")



        if [[ra1,dec1],[ra2,dec2]] not in used_borders and [[ra2,dec2],[ra1,dec1]] not in used_borders:

            used_borders.append([[ra1,dec1],[ra2,dec2]])       

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

                v1 = get_transformed_vector(ra_now,dec_now,center_Dec_deg, center_ra_deg, zrot_deg)
                # theta_R1 = polar_upproject(v1)
                x_y_z__1 = upproject(v1)

                v2 = get_transformed_vector(ra_next,dec_next,center_Dec_deg, center_ra_deg, zrot_deg)
                # theta_R2 = polar_upproject(v2)
                x_y_z__2 = upproject(v2)


                x1=x_y_z__1[0]
                x2=x_y_z__2[0]
                y1=x_y_z__1[1]
                y2=x_y_z__2[1]
                color="red"
                plt.plot([y1,y2],[x1,x2],linewidth=0.5,linestyle="-",alpha=1,color=color)

                ra_now = ra_next
                dec_now = dec_next

        # else:
        #     print("ALREADY FOUND BORDER!")


def plot_stars_polar(const, center_Dec_deg,center_ra_deg,zrot_deg, ax, hmg, hmg2, a):
    x=[]
    y=[]
    for idx,star in enumerate(const):
        if idx%100 == 0:
            print(f"polar stars:\t{idx/len(const)*100:.2f}%")
        ra  = star['Right Ascension (deg)']/180*pi
        dec = star['Declination (deg)']/180*np.pi
        v = get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
        theta_R = polar_upproject(v)
        S,marker,alpha = condition_magnitudes(star,hmg,hmg2)
        ax.scatter(theta_R[0], theta_R[1], c="black", marker=marker, s=a*(1+hmg-S), alpha=alpha, zorder=ORDER_OF_STARS_MINOR)
        x.append(theta_R[1])
        y.append(theta_R[0])


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
            ra  = star['Right Ascension (deg)']/180*np.pi
            dec = star['Declination (deg)']/180*np.pi
            v = get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
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
            ra  = star['Right Ascension (deg)']/180*np.pi
            dec = star['Declination (deg)']/180*np.pi
            v = get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
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
            ra  = star['Right Ascension (deg)']/180*np.pi
            dec = star['Declination (deg)']/180*np.pi
            v = get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
            x_y_z = cylindrical_project(v)

            S=1
            lw = 1.5
            x=x_y_z[0]
            y=x_y_z[1]

            if x<0:
                x=x+2*np.pi
            
            plt.scatter(x, y, color=star_color,  s=S, marker="o", alpha=1, zorder=ORDER_OF_STARS_MAJOR,linewidths=lw)   # <— skinny!)  
            plt.scatter(x-2*pi, y, color=star_color,  s=S, marker="o", alpha=1, zorder=ORDER_OF_STARS_MAJOR,linewidths=lw)   # <— skinny!) 



def plot_cylindrical_lines(lines,center_Dec_deg,center_ra_deg,zrot_deg,*,Break_line=0):
    
    segmentation_flag = False
    lines_to_print_list=[]
    # alpha_list=[]
    width_list=[]
    for idx,line in enumerate(lines):
        if idx%10 == 0:
            print(f"cylindrical lines:\t{idx/len(lines)*100:.2f}%")
        constellation=line['Constellation1']
        ra1  = line['Right Ascension (deg)1']/180*pi
        dec1 = line['Declination (deg)1']/180*np.pi
        ra2  = line['Right Ascension (deg)2']/180*pi
        dec2 = line['Declination (deg)2']/180*np.pi
        linestyle = line['linestyle']
        color = line['color']
        width = line['width']
        # width = 0.5
        alpha = line['alpha']

        v1 = get_transformed_vector(ra1,dec1,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_1 = cylindrical_project(v1)


        v2 = get_transformed_vector(ra2,dec2,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_2 = cylindrical_project(v2)

        x1=xyz_1[0]
        x2=xyz_2[0]
        y1=xyz_1[1]
        y2=xyz_2[1]

        if abs(x1-x2)>np.pi:    
            segmentation_flag = True
            print("FLAG!!!")

        lines_to_print_list.append([[x1,x2],[y1,y2]])
        width_list.append(width)
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

                plt.plot([x1,x2],[y1,y2],linewidth=width,linestyle=linestyle,alpha=1,color=color,zorder=ORDER_OF_LINES)
        else:   
            plt.plot([x1,x2],[y1,y2],linewidth=width,linestyle=linestyle,alpha=1,color=color,zorder=ORDER_OF_LINES)

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



def plot_cylindrical_borders(border_line_list, center_Dec_deg,center_ra_deg,zrot_deg, used_borders_list):
    # used_borders=[]
    crossing_border_flag = False
    break_flag = False
    segmented_lines_to_print_list=[]
    possibly_broken_lines_list=[]
    unsegmented_lines_to_print_list=[]
    current_constellation_used_lines=[]

    for idx,border_line in enumerate(border_line_list):
        
        ra1  = border_line['Right Ascension (deg)1']/180*np.pi
        dec1 = border_line['Declination (deg)1']/180*np.pi
        ra2  = border_line['Right Ascension (deg)2']/180*np.pi
        dec2 = border_line['Declination (deg)2']/180*np.pi
        linestyle = border_line['linestyle']
        color = border_line['color']
        width = border_line['width']
        alpha = border_line['alpha']

        # ra1=ra1-(2*np.pi)*np.floor(ra1/(2*np.pi))
        # ra2=ra2-(2*np.pi)*np.floor(ra2/(2*np.pi))
        # print(len(used_borders_list))

        v1 = get_transformed_vector(ra1,dec1,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_1 = cylindrical_project(v1)

        v2 = get_transformed_vector(ra2,dec2,center_Dec_deg, center_ra_deg, zrot_deg)
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

            # ra_diff = (ra2-ra1)
            # dec_diff = (dec2-dec1)
            # ra_diff_rounded_degs = (np.floor(abs(ra_diff)/(2*np.pi)*360))+1
            # dec_diff_rounded_degs = (np.floor(abs(dec_diff)/(2*np.pi)*360))+1
            # border_segment_num = max( ra_diff_rounded_degs, dec_diff_rounded_degs)
            # border_segment_num = 1

            # ra_step = ra_diff/border_segment_num
            # dec_step = dec_diff/border_segment_num
            # ra_now = ra1
            # dec_now = dec1

            # for _ in range(int(border_segment_num)):
            #     ra_next = ra_now + ra_step
            #     dec_next = dec_now + dec_step

            #     segmented_lines_to_print_list.append([[x1,x2],[y1,y2]])
                        
            #     # plt.plot([x1,x2],[y1,y2],linewidth=0.5,linestyle="-",alpha=1,color="red",zorder=2)

            #     ra_now = ra_next
            #     dec_now = dec_next



    for line_coordinate in current_constellation_used_lines:
        x_coordinates = line_coordinate[0]+np.random.random(2)/20*0
        y_coordinates = line_coordinate[1]+np.random.random(2)/20*0
        
        plt.plot(x_coordinates, y_coordinates, linewidth=0.5, linestyle="-", alpha=1, color="red", zorder=ORDER_OF_BORDES)

    # # else:
    #     print("border_line_already_found")        

