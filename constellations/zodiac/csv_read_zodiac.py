import csv
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np
import re
import utils
import pickle





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
def read_stars_csv(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ra_deg, dec_deg = convert_coords(row['Right Ascension'], row['Declination'])

            current_star = utils.PointDatas(name = row['Name'], 
                                            ra_dec_deg = utils.RaDecDegCoord_deg(right_ascension_deg=ra_deg, declination_deg= dec_deg),
                                            apparent_mag = float(row['Apparent Magnitude']),
                                            constellation = row['Constellation'])

            data.append(current_star)

    return data



# Function to read the CSV file
def read_lines_csv(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ra_deg1, dec_deg1 = convert_coords(row['Right Ascension1'], row['Declination1'])
            ra_deg2, dec_deg2 = convert_coords(row['Right Ascension2'], row['Declination2'])

            current_line = utils.SkyLine(
                point_data_1=utils.PointDatas(
                    name=row['Name1'],
                    ra_dec_deg=utils.RaDecDegCoord_deg(
                        right_ascension_deg=ra_deg1,
                        declination_deg=dec_deg1
                    ),
                    apparent_mag=float(row['Apparent Magnitude1']),
                    constellation=row['Constellation1'],
                    ),

                point_data_2=utils.PointDatas(
                    name=row['Name2'],
                    ra_dec_deg=utils.RaDecDegCoord_deg(
                        right_ascension_deg=ra_deg2,
                        declination_deg=dec_deg2
                    ),
                    apparent_mag=float(row['Apparent Magnitude2']),
                    constellation=row['Constellation2'],
                    ),

                linestyle=row['linestyle'],
                color =  row['color'],
                width =  row['width'],
                alpha =  row['alpha']
            )

            data.append(current_line)

    output = utils.ListOfSkylines(list_of_skylines=data)

    return output



if __name__ == "__main__":
    
    #Export stars
    filename = 'zodiac.csv'  # Replace 'stars.csv' with the path to your CSV file
    data = read_stars_csv(filename)

    with open("stars_data.pkl", "wb") as f:
        pickle.dump(data, f)


    #Export lines
    filename_lines = 'zodiac_lines.csv'  # Replace 'stars.csv' with the path to your CSV file
    lines_data = read_lines_csv(filename_lines)

    with open("lines_data.pkl", "wb") as f:
        pickle.dump(lines_data, f)


    #Export borders
    filename_borders = 'zodiac_borders.csv'  # Replace 'stars.csv' with the path to your CSV file
    borders_data = read_lines_csv(filename_borders)

    with open("borders_data.pkl", "wb") as f:
        pickle.dump(borders_data, f)
