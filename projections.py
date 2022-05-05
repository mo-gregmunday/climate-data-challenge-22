import numpy as np
import iris
from iris.util import equalise_attributes
import iris.util
import iris.cube
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature


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


def main():
    courtroom_df = pd.read_csv(
        "data/courtroom_coords.csv",
         encoding='cp1252')
    
    annual_cubelist = iris.load(['data/annual/*nc'])
    monthly_cubelist = iris.load(['data/monthly/*nc'])
    
    court_long, court_lat = courtrooms_data(courtroom_df)

    # annual tas
    tas = climate_data(annual_cubelist)
    
    court_long = court_long.to_list()
    court_lat = court_lat.to_list()
    
    court_long = np.array([float(x) for x in court_long])
    court_lat = np.array([float(x) for x in court_lat])

    tas_long = tas.coord("longitude").points
    tas_lat = tas.coord("latitude").points
    
    # mask = np.ma.getmask(tas.data)
    # masked_array = np.ma.masked_array(tas.data, mask=mask)
    # tas_masked = tas.copy(data=masked_array)

    ten_metre_borders = cfeature.NaturalEarthFeature(category='cultural',
        name='admin_0_countries',
        scale='10m',
        facecolor = 'none')
    
    transform = ccrs.PlateCarree()

    for i in range(0, 59):
        plt.figure(figsize=(6, 8))
        ax = plt.axes(projection=ccrs.OSGB())
        im = ax.pcolormesh(tas_long, tas_lat, tas[0, i].data, transform=transform, vmin=0, vmax=18)

        ax.plot(court_long, court_lat, 'ro', transform=transform, markersize=2)
        
        plt.colorbar(im, orientation='vertical', label="Air Temperature / C\u00B0")
        ax.add_feature(ten_metre_borders)
        ax.set_title("Average Annual Temperature with Courtooms, " + str(tas[0, i].coord("year").points))
        plt.savefig("plots/" + str(tas[0, i].coord("year").points) + ".png")
        plt.close()

if __name__ == '__main__':
    main()
    