import numpy as np
import iris
from iris.util import equalise_attributes
import iris.cube
import iris.quickplot as qplt
import iris.plot as iplt
import matplotlib.pyplot as plt
import pandas as pd

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


def main():
    courtroom_df = pd.read_csv(
        "data/courtroom_coords.csv",
         encoding='cp1252')
    
    cubelist = iris.load(['data/*nc'])
    
    court_long, court_lat = courtrooms_data(courtroom_df)

    tas = climate_data(cubelist)
    
    qplt.pcolormesh(tas[0, 0])
    # plt.scatter(court_long, court_lat, 'bo')
    plt.show()


if __name__ == '__main__':
    main()
    