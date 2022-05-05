import numpy as np
import iris
from iris.util import equalise_attributes
from iris.coords import DimCoord
import iris.cube
import iris.quickplot as qplt
import iris.plot as iplt
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
import math


def courtrooms_data(courtroom_df):
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
    _ = equalise_attributes(cubelist)
    tas = cubelist.concatenate_cube()
    
    return tas


def mercator_from_lat_long(lats, lons):
        r_major = 6378137.000
        x = r_major*np.radians(lons)
        scale = x/lons
        y = 180.0/np.pi*np.log(np.tan(np.pi/4.0+lats*(np.pi/180.0)/2.0))*scale
        
        return (x, y)


# def make_cube(x, y):
#     courts = np.empty(len(x))
    
#     latitude = DimCoord(y, standard_name='latitude', units='degrees')
#     longitude = DimCoord(x, standard_name='longitude', units='degrees')

#     dim_coords_and_dims = [(latitude, 0), (longitude, 1)] 
    
#     courts_cube = iris.cube.Cube(courts,
#                                  dim_coords_and_dims=dim_coords_and_dims,
#                                  var_name="courts")

#     return courts_cube


def main():
    courtroom_df = pd.read_csv(
        "data/courtroom_coords.csv",
         encoding='cp1252')
    
    cubelist = iris.load(['data/annual/*nc'])
    
    court_long, court_lat = courtrooms_data(courtroom_df)

    tas = climate_data(cubelist)
    
    court_long = court_long.to_list()
    court_lat = court_lat.to_list()
    
    court_long = np.array([float(x) for x in court_long])
    court_lat = np.array([float(x) for x in court_lat])

    tas_long = tas.coord("longitude").points
    tas_lat = tas.coord("latitude").points
    
    transform = ccrs.PlateCarree()
    
    for i in range(0, 59):
        ax = plt.axes(projection=ccrs.OSGB())
        ax.pcolormesh(tas_long, tas_lat, tas[0, i].data, transform=transform, zorder=2)
        ax.plot(court_long, court_lat, 'k*', transform=transform, markersize=1, zorder=20)
        ax.set_title(str(tas[0, i].coord("year").points))
        plt.savefig("plots/" + str(tas[0, i].coord("year").points) + ".png")
        plt.close()

if __name__ == '__main__':
    main()
    