import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi

def upproject(v):
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