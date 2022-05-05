import numpy as np
import iris
import iris.quickplot as qplt
from iris.util import equalise_attributes
import iris.util
import iris.cube
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature


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
    tas = cubelist.concatenate_cube()
    
    return tas


def distance(lat1, lon1, lat2, lon2):
    # this calculates the great circle distance between 2 points 
    p = 0.017453292519943295
    hav = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p)*np.cos(lat2*p) \
        * (1-np.cos((lon2-lon1)*p)) / 2
        
    return 12742 * np.arcsin(np.sqrt(hav))


def find_lat_lon(our_lat, our_lon, map_latitude, map_longitude):
    # this finds the indices of our lat and lon point.
    # it uses a midpoint type search algorithm, first on i(lat), then on j(lon)
    # we compare to the middle point of the 2 boxes
    
    # initialise the max and min on the 2d ends
    imin=0;imax=map_longitude.shape[0];
    jmin=0;jmax=map_latitude.shape[1];

    for iter_int in range(18):
        # now find the mid points of the i and j we 
        imid=int(np.floor((imin+imax)/2));imid1=int(np.floor((imin+imid)/2)); \
            imid2=int(np.floor((imid+imax)/2));
        jmid=int(np.floor((jmin+jmax)/2));jmid1=int(np.floor((jmin+jmid)/2)); \
            jmid2=int(np.floor((jmid+jmax)/2));

        # start with 2 i boxes, and keep j constant
        # get the location of the mid points
        pt={};pt['lat']=np.empty(2);pt['lon']=np.empty(2)
        pt['lat'][0] = map_latitude[imid1,jmid]
        pt['lon'][0] = map_longitude[imid1,jmid]
        pt['lat'][1] = map_latitude[imid2,jmid]
        pt['lon'][1] = map_longitude[imid2,jmid]

        # here we compare the haversine distance of our point to the mid point of the 2 splits
        # we then choose our imax and imin on the basis of the box that is closest
        if distance(pt['lat'][0],pt['lon'][0],our_lat,our_lon) > \
            distance(pt['lat'][1],pt['lon'][1],our_lat,our_lon):
            imin = imid
            imax = imax
        else:
            imin=imin
            imax=imid
            
        # now find the mid points again
        imid=int(np.floor((imin+imax)/2));imid1=int(np.floor((imin+imid)/2)); \
            imid2=int(np.floor((imid+imax)/2));
        jmid=int(np.floor((jmin+jmax)/2));jmid1=int(np.floor((jmin+jmid)/2)); \
            jmid2=int(np.floor((jmid+jmax)/2)); # this is redundant

        # now 2 j boxes keeping our i constant
        # get the location of the mid points
        pt={};pt['lat']=np.empty(2);pt['lon']=np.empty(2)
        pt['lat'][0] = map_latitude[imid,jmid1]
        pt['lon'][0] = map_longitude[imid,jmid1]
        pt['lat'][1] = map_latitude[imid,jmid2]
        pt['lon'][1] = map_longitude[imid,jmid2]

        # and compare the distance of our point to the 2 boxes
        # then redefine the jmax and jmin
        if distance(pt['lat'][0],pt['lon'][0],our_lat,our_lon) > \
            distance(pt['lat'][1],pt['lon'][1],our_lat,our_lon):
            jmin = jmid
            imax = jmax
        else:
            jmin = jmin
            jmax = jmid

    return imid,jmid 


def get_lat_long(court_long, court_lat, tas_annual):
    """
    Gets courtroom and tas lat/lons 
    """
    court_long = court_long.to_list()
    court_lat = court_lat.to_list()
    
    court_long = np.array([float(x) for x in court_long])
    court_lat = np.array([float(x) for x in court_lat])

    tas_long = tas_annual.coord("longitude").points
    tas_lat = tas_annual.coord("latitude").points
    
    return court_long, court_lat, tas_long, tas_lat
    
    
def plotting_gif(tas_long, tas_lat, tas, court_long, court_lat):
    """
    Plots UKCP climate projections with locations of courtrooms superimposed 
    """
    ten_metre_borders = cfeature.NaturalEarthFeature(category='cultural',
    name='admin_0_countries',
    scale='10m',
    facecolor = 'none')
    
    transform = ccrs.PlateCarree()

    for i in range(0, 59):
        plt.figure(figsize=(6, 8))
        ax = plt.axes(projection=ccrs.OSGB())
        im = ax.pcolormesh(tas_long, tas_lat, 
                        tas[0, i].data, transform=transform, vmin=0, vmax=18)

        ax.plot(court_long, court_lat, 'ro', transform=transform, markersize=2)
        
        plt.colorbar(im, orientation='vertical', \
            label="Air Temperature / C\u00B0")
        ax.add_feature(ten_metre_borders)
        ax.set_title("Average Annual Temperature with Courtooms, " + \
                     str(tas[0, i].coord("year").points))
        plt.savefig("plots/" + str(tas[0, i].coord("year").points) + ".png")
        plt.close()


def courtroom_temps(tas_long, tas_lat, tas, court_long, court_lat, courtroom_df):
    """
    Calculates specific courtroom area temperatures over timeseries 
    """
    court_locn_on_UKCP_grid=[] # put the indices of each court here, lat index, long index
    court_long_UKCP=[] # the long of the court in UKCP space
    court_lat_UKCP=[] # the lat of the court in UKCP space

    for i_court  in range(len(court_long)):
        tmp = find_lat_lon(court_lat[i_court], court_long[i_court], tas_lat, tas_long)
        court_long_UKCP.append(tas_long[tmp])
        court_lat_UKCP.append(tas_lat[tmp])
        court_locn_on_UKCP_grid.append(tmp)

    court_long_UKCP = np.array(court_long_UKCP) 
    court_lat_UKCP = np.array(court_lat_UKCP) 

    court_time_series=[]
    for i_court  in range(len(court_long)):   
        court_time_series.append(np.squeeze(
            tas.data[:, :, court_locn_on_UKCP_grid[i_court][0], \
                court_locn_on_UKCP_grid[i_court][1]]))

    i_court = 300
    plt.plot(tas.coord("year").points, court_time_series[i_court])
    plt.title('Projected mean temperature for ' + courtroom_df.Sitename[i_court])
    plt.ylabel('Temperature ($^{\circ}$C)')
    plt.xlabel('Year')
    plt.savefig('plots/courtroom_temp.png')

    # saving to csv
    df={} # a dictionary to put the data ready to output to csv
    df['time'] = tas.coord("year").points
    for i_court  in range(len(court_long)):
        df[courtroom_df.Sitename[i_court]] = court_time_series[i_court]

    return df


def main():
    courtroom_df = pd.read_csv(
        "data/courtroom_coords.csv",
         encoding='cp1252')
    
    annual_cubelist = iris.load(['data/annual/*nc'])
    monthly_cubelist = iris.load(['data/monthly/*nc'])
    
    court_long, court_lat = courtrooms_data(courtroom_df)

    # annual and monthly tas, switch accordingly
    tas_annual = climate_data(annual_cubelist)
    tas_monthly = climate_data(monthly_cubelist)
    
    (court_long, court_lat,
     tas_long, tas_lat) = get_lat_long(court_long, court_lat, tas_annual)
    
    plotting_gif(tas_long, tas_lat, tas_annual, court_long, court_lat)

    court_temp_df = pd.DataFrame(courtroom_temps(
        tas_long, tas_lat, tas_annual, court_long, court_lat, courtroom_df))
    court_temp_df.to_csv('courts_temp_projections.csv')


if __name__ == '__main__':
    main()
    