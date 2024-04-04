import csv
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np

# Function to convert Right Ascension and Declination to degrees
def convert_coords(ra, dec):
    ra = ra.replace('\xa0', ' ')
    dec = dec.replace('\xa0', ' ')
    c = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))
    return c.ra.deg, c.dec.deg


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
