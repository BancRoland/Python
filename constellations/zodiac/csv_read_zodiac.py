import csv
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np
import re

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
    DEC_0=float(matchesDEC[0])
    if DEC_0>=0:
        RA_sign=1
    else:
        RA_sign=-1
    DEC_=abs(DEC_0)
    DEC_min=float(matchesDEC[1])
    DEC_sec=float(matchesDEC[2])
    DEC = RA_sign*(DEC_+DEC_min/60+DEC_sec/60/60)

    # print(f'ra: {ra} = {c.ra.deg} = {matchesRA} = {RA}')
    # print(f'dec: {dec} = {c.dec.deg} = {matchesDEC} = {DEC}')
    print(f'ra: {ra} = {matchesRA} = {RA}')
    print(f'dec: {dec} = {matchesDEC} = {DEC}')
    return RA, DEC


# Function to read the CSV file
def read_csv(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert RA and Dec to degrees
            # print(row['Right Ascension'], row['Declination'])
            # print(row['Name'])
            ra_deg, dec_deg = convert_coords(row['Right Ascension'], row['Declination'])
            # Append the processed data to the list
            print(row['Name'])
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
