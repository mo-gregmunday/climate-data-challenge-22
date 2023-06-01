import re

import numpy as np
import iris
from iris.util import equalise_attributes
import iris.util
import iris.cube
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from utils import land_mask


def courtrooms_data(courtroom_df):
    """
    Reads in courtroom data csv file, isolates courtroom coords
    """
    df = pd.DataFrame(courtroom_df)
    df.columns = df.columns.str.replace(' ', '') 
    df["Sitestatus"] = df["Sitestatus"].str.upper()

    df.drop(df[df.iloc[:, 4] != 'ACTIVE'].index, inplace=True)

    coords = df.iloc[:,15]
    coords_split = coords.str.split('|', expand=True)
    
    court_long = coords_split[0]
    court_lat = coords_split[1]

    return court_long.dropna(), court_lat.dropna()


def climate_data(cubelist):
    """
    Concatenates UKCP time sliced cubes
    """
    _ = equalise_attributes(cubelist)
    tas = cubelist.concatenate_cube()[0] # Only one ensemble member present
    print(tas)
    
    return tas


def distance(lat1, lon1, lat2, lon2):
    # this calculates the great circle distance between 2 points 
    p = 0.017453292519943295
    hav = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p)*np.cos(lat2*p) \
        * (1-np.cos((lon2-lon1)*p)) / 2
        
    return 12742 * np.arcsin(np.sqrt(hav))


def get_lat_long(court_long, court_lat):
    """
    Gets courtroom and tas lat/lons 
    """
    court_long = court_long.to_list()
    court_lat = court_lat.to_list()
    
    court_long = np.array([float(x) for x in court_long])
    court_lat = np.array([float(x) for x in court_lat])
    
    return court_long, court_lat
    
    
def calculate_baseline_avg(tas):
    baseline_period = tas[:20]
    baseline_avg = baseline_period.collapsed('time', iris.analysis.MEAN)
    
    return baseline_avg
    
    
def plotting_article_plot(tas, court_long, court_lat):
    """
    Plots UKCP climate projections with locations of courtrooms superimposed 
    """
    ten_metre_borders = cfeature.NaturalEarthFeature(category='cultural',
    name='admin_0_countries',
    scale='10m',
    facecolor = 'none')

    # 2080-1981 anomaly
    baseline = calculate_baseline_avg(tas)
    anomaly = tas[59] - baseline
    lon, lat = anomaly.coord('longitude').points, anomaly.coord('latitude').points
    
    land_mask = iris.load_cube('/project/ukcp/extra/lsm_land-cpm_uk_5km.nc')
    anomaly = iris.util.mask_cube(anomaly, land_mask.data.mask)
    
    
    font = {'family': 'sans-serif',
        'weight': 'normal',
        'size': 14,
        }

    matplotlib.rc('font', **font)
    
    transform = ccrs.PlateCarree()
    fig, ax = plt.subplots(1, 1, figsize=(7,9), subplot_kw={'projection': ccrs.OSGB()})
    im = ax.pcolormesh(lon, lat, anomaly.data, transform=transform, cmap='plasma')

    ax.plot(court_long, court_lat, 'kx', transform=transform, markersize=4)
    ax.add_feature(ten_metre_borders)
    ax.text(40000, 1120000, '2080', fontdict={'size': 16})
    
    fig.colorbar(im, ax=ax, orientation='vertical', \
        label="1.5m air temperature anomaly (C\u00B0)")
    
    plt.tight_layout()
    plt.savefig('rmets_article/plots/anomaly_plot.png')


def main():
    courtroom_df = pd.read_csv(
        "data/courtroom_coords.csv",
         encoding='cp1252')
    
    annual_cubelist = iris.load(['data/annual/*nc'])
    
    court_long, court_lat = courtrooms_data(courtroom_df)

    # annual and monthly tas, switch accordingly
    tas_annual = climate_data(annual_cubelist)
    
    court_long, court_lat = get_lat_long(court_long, court_lat)
    
    plotting_article_plot(tas_annual, court_long, court_lat)


if __name__ == '__main__':
    main()
    