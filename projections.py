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


def courtrooms_data(courtroom_df):
    df = pd.DataFrame(courtroom_df)
    df.columns = df.columns.str.replace(' ', '') 
    df["Sitestatus"] = df["Sitestatus"].str.upper()

    df.drop(df[df.iloc[:, 4] != 'ACTIVE'].index, inplace=True)

    coords = df.iloc[:,15]
    coords_split = coords.str.split('|', expand=True)
    
    court_long = coords_split[1]
    court_lat = coords_split[0]

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
    
    cubelist = iris.load(['data/*nc'])
    
    court_long, court_lat = courtrooms_data(courtroom_df)

    tas = climate_data(cubelist)
    
    court_long = court_long.to_list()
    court_lat = court_lat.to_list()
    
    court_long = [float(x) for x in court_long]
    court_lat = [float(x) for x in court_lat]

    x, y = mercator_from_lat_long(np.array([float(x) for x in court_long]), 
                                  np.array([float(x) for x in court_lat]))
    

    qplt.pcolormesh(tas[0, 0], zorder=2)
    plt.plot(x, y, 'bo', markersize=0.4, zorder=20)
    plt.show()


if __name__ == '__main__':
    main()
    