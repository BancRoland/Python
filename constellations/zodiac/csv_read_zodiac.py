import csv
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np
import re
import utils




print("csv_read_zodiac.py started")

# Function to convert Right Ascension and Declination to degrees
def convert_coords0(ra, dec):
    ra = ra.replace('\xa0', ' ')
    dec = dec.replace('\xa0', ' ')
    c = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))
    return c.ra.deg, c.dec.deg

def convert_coords(ra, dec):
    ra = ra.replace('\xa0', ' ')
    dec = dec.replace('\xa0', ' ')
    # c = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))

    matchesRA = re.findall(r'-?\d+(?:\.\d+)?', ra)

    RA_h0=float(matchesRA[0])
    if RA_h0>=0:
        RA_sign=1
    else:
        RA_sign=-1
    RA_h=abs(RA_h0)
    RA_min=float(matchesRA[1])
    RA_sec=float(matchesRA[2])
    RA = 360+360*RA_sign*(RA_h/24+RA_min/24/60+RA_sec/24/60/60)

    matchesDEC = re.findall(r'[+-]?\d+(?:\.\d+)?', dec)
    first_string = matchesDEC[0]
    DEC_0=float(first_string)
    if first_string[0] == "-":
        DEC_sign=-1
    else:
        DEC_sign=1
    DEC_=abs(DEC_0)
    DEC_min=float(matchesDEC[1])
    DEC_sec=float(matchesDEC[2])
    DEC = DEC_sign*(DEC_+DEC_min/60+DEC_sec/60/60)

    # print(f'ra: {ra} = {c.ra.deg} = {matchesRA} = {RA}')
    # print(f'dec: {dec} = {c.dec.deg} = {matchesDEC} = {DEC}')
    # print(f'ra: {ra} = {matchesRA} = {RA}')
    # print(f'dec: {dec} = {matchesDEC} = {DEC}')
    return RA, DEC


# Function to read the CSV file
def read_csv(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ra_deg, dec_deg = convert_coords(row['Right Ascension'], row['Declination'])
            data.append({
                'Name': row['Name'],
                'Right Ascension (deg)': ra_deg,
                'Declination (deg)': dec_deg,
                'Apparent Magnitude': float(row['Apparent Magnitude']),
                'Constellation': row['Constellation']
                })
    return data

# Example usage
filename = 'zodiac.csv'  # Replace 'stars.csv' with the path to your CSV file
stars_data = read_csv(filename)

np.save("stars_test.npy", stars_data)
# for star in stars_data:
#     print(star)


# Function to read the CSV file
def read_lines_csv(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ra_deg1, dec_deg1 = convert_coords(row['Right Ascension1'], row['Declination1'])
            ra_deg2, dec_deg2 = convert_coords(row['Right Ascension2'], row['Declination2'])
            # Append the processed data to the list
            # print(row['Name1'])
            data.append({
                'Name1': row['Name1'],
                'Right Ascension (deg)1': ra_deg1,
                'Declination (deg)1': dec_deg1,
                'Apparent Magnitude1': float(row['Apparent Magnitude1']),
                'Constellation1': row['Constellation1'],
                'Name2': row['Name2'],
                'Right Ascension (deg)2': ra_deg2,
                'Declination (deg)2': dec_deg2,
                'Apparent Magnitude2': float(row['Apparent Magnitude2']),
                'Constellation2': row['Constellation2'],
                'linestyle': row['linestyle'],
                'color': row['color'],
                'width': row['width'],
                'alpha': row['alpha']
                })
    return data

# def get_ecliptic_lines(n_points=100):
#     data = []

#     sun_positons_3dv=[]

#     EQINOX_POINT = utils.get_3d_vec_from_RaDec(ra=0, dec=0)
#     for i in range(0,24,1):
#         time_rot = utils.zrot(EQINOX_POINT,i/24*360)
#         space_rot= utils.xrot(time_rot,23.5)

#         sun_positons_3dv.append(space_rot)

#         ra_deg1, dec_deg1 = convert_coords(row['Right Ascension1'], row['Declination1'])
#         ra_deg2, dec_deg2 = convert_coords(row['Right Ascension2'], row['Declination2'])
#         # Append the processed data to the list
#         # print(row['Name1'])
        
#         data.append({
#             'Name1': row['Name1'],
#             'Right Ascension (deg)1': ra_deg1,
#             'Declination (deg)1': dec_deg1,
#             'Apparent Magnitude1': float(row['Apparent Magnitude1']),
#             'Constellation1': row['Constellation1'],
#             'Name2': row['Name2'],
#             'Right Ascension (deg)2': ra_deg2,
#             'Declination (deg)2': dec_deg2,
#             'Apparent Magnitude2': float(row['Apparent Magnitude2']),
#             'Constellation2': row['Constellation2'],
#             'linestyle': row['linestyle'],
#             'color': row['color'],
#             'width': row['width'],
#             'alpha': row['alpha']
#             })
#     return data

def __name__():
    # Example usage
    filename_lines = 'zodiac_lines.csv'  # Replace 'stars.csv' with the path to your CSV file
    lines_data = read_lines_csv(filename_lines)

    np.save("lines_data.npy", lines_data)



    # Example usage
    filename_borders = 'zodiac_borders.csv'  # Replace 'stars.csv' with the path to your CSV file
    borders_data = read_lines_csv(filename_borders)

    np.save("borders_data.npy", borders_data)