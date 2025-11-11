import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi

def upproject(v):
    """
    return: [x,y,z]
    """
    v=np.array(v)+np.array([0,0,1])
    w=v/v[2]
    return w

def cylinder_project(v):
    x = np.arctan2(v[0],v[1])
    # y=v[2]
    y=np.arcsin(v[2])
    w = np.array([x,y])
    return w

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

def get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg):    
    v = get_3d_vec_from_RaDec(ra,dec)
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
        print(f"lines:\t{idx/len(lines)*100:.2f}%")
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
        ax.plot([theta1,theta2],[R1,R2],linewidth=width,linestyle=linestyle,alpha=1,color=color,zorder=2)

def plot_lines_str_grph(lines, center_Dec_deg,center_ra_deg,zrot_deg, ax):
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
        
        v1 = get_transformed_vector(ra1,dec1,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_1 = upproject(v1)

        v2 = get_transformed_vector(ra2,dec2,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_2 = upproject(v2)

        x1=xyz_1[0]
        x2=xyz_2[0]
        y1=xyz_1[1]
        y2=xyz_2[1]
        plt.plot([y1,y2],[x1,x2],linewidth=width,linestyle=linestyle,alpha=1,color=color,zorder=2)
                        
def plot_borders_polar(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax):
    for idx,line in enumerate(borders):
        print(f"borders:\t{idx/len(borders)*100:.2f}%")
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

        

def plot_borders_str_grph(borders, center_Dec_deg,center_ra_deg,zrot_deg, ax):
    for idx,line in enumerate(borders):
        print(f"borders:\t{idx/len(borders)*100:.2f}%")
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
            # theta_R1 = polar_upproject(v1)
            x_y_z__1 = upproject(v1)

            v2 = get_transformed_vector(ra_next,dec_next,center_Dec_deg, center_ra_deg, zrot_deg)
            # theta_R2 = polar_upproject(v2)
            x_y_z__2 = upproject(v2)


            x1=x_y_z__1[0]
            x2=x_y_z__2[0]
            y1=x_y_z__1[1]
            y2=x_y_z__2[1]
            plt.plot([y1,y2],[x1,x2],linewidth=0.5,linestyle="-",alpha=1,color=color)

            ra_now = ra_next
            dec_now = dec_next


def plot_stars_polar(const, center_Dec_deg,center_ra_deg,zrot_deg, ax, hmg, hmg2, a):
    x=[]
    y=[]
    for idx,star in enumerate(const):
        print(f"stars:\t{idx/len(const)*100:.2f}%")
        ra  = star['Right Ascension (deg)']/180*pi
        dec = star['Declination (deg)']/180*np.pi
        v = get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
        theta_R = polar_upproject(v)
        S,marker,alpha = condition_magnitudes(star,hmg,hmg2)
        ax.scatter(theta_R[0], theta_R[1], c="black", marker=marker, s=a*(1+hmg-S), alpha=alpha, zorder=3)
        x.append(theta_R[1])
        y.append(theta_R[0])


def plot_cylindrical_stars(const,center_Dec_deg,center_ra_deg,zrot_deg,hmg,hmg2,a):
    x=[]
    y=[]
    for star in const:
        ra  = star['Right Ascension (deg)']/180*pi
        dec = star['Declination (deg)']/180*np.pi
        v = get_transformed_vector(ra,dec,center_Dec_deg, center_ra_deg, zrot_deg)
        x_y_z = cylinder_project(v)
        S,marker,alpha = condition_magnitudes(star,hmg,hmg2)
        plt.scatter(x_y_z[0], x_y_z[1], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha)
        y.append(x_y_z[1])
        x.append(x_y_z[0])

def plot_cylindrical_lines(lines,center_Dec_deg,center_ra_deg,zrot_deg):
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
        
        # v1 = get_transformed_vector(ra1,dec1,center_Dec_deg, center_ra_deg, zrot_deg)
        # xyz_1 = upproject(v1)

        v1 = get_transformed_vector(ra1,dec1,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_1 = cylinder_project(v1)

        # v2 = get_transformed_vector(ra2,dec2,center_Dec_deg, center_ra_deg, zrot_deg)
        # xyz_2 = upproject(v2)

        v2 = get_transformed_vector(ra2,dec2,center_Dec_deg, center_ra_deg, zrot_deg)
        xyz_2 = cylinder_project(v2)

        x1=xyz_1[0]
        x2=xyz_2[0]
        y1=xyz_1[1]
        y2=xyz_2[1]
        plt.plot([x1,x2],[y1,y2],linewidth=width,linestyle=linestyle,alpha=1,color=color,zorder=2)





def plot_borders_cylindrical(borders, center_Dec_deg,center_ra_deg,zrot_deg):
    for idx,line in enumerate(borders):
        print(f"borders:\t{idx/len(borders)*100:.2f}%")
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
            # theta_R1 = polar_upproject(v1)
            x_y_z__1 = cylinder_project(v1)

            v2 = get_transformed_vector(ra_next,dec_next,center_Dec_deg, center_ra_deg, zrot_deg)
            # theta_R2 = polar_upproject(v2)
            x_y_z__2 = cylinder_project(v2)


            x1=x_y_z__1[0]
            x2=x_y_z__2[0]
            y1=x_y_z__1[1]
            y2=x_y_z__2[1]
            plt.plot([x1,x2],[y1,y2],linewidth=0.5,linestyle="-",alpha=1,color=color)

            ra_now = ra_next
            dec_now = dec_next