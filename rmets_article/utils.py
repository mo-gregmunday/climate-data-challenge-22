import iris
from iris.analysis.geometry import geometry_area_weights
from iris.util import mask_cube
import numpy as np#
import cartopy
from cartopy.feature import NaturalEarthFeature
from shapely.ops import unary_union

def land_mask(cube):
    cube.remove_coord('latitude')
    cube.remove_coord('longitude')
    lat = cube.coord('projection_y_coordinate')
    lon = cube.coord('projection_x_coordinate')
    lat.rename('latitude')
    lon.rename('longitude')
     # create landsea mask
    land_feature = NaturalEarthFeature(scale="110m", name="land", category="physical")
    land_masses = land_feature.geometries()
    masses = [mass for mass in land_masses]
    all_masses = unary_union(masses)
    
    # Make sure your coordinates have bounds before doing this.
    weights = geometry_area_weights(cube, all_masses, normalize=True)
    mask = np.where(weights > 0, False, True)
    masked_cube = mask_cube(cube, mask)
    
    return masked_cube


def project_cube(cube):
    """Project cube to PlateCaree projection"""
    cube_proj = iris.analysis.cartography.project(cube, cartopy.crs.OSGB())[0]
    cube_proj.coord('latitude').guess_bounds()
    cube_proj.coord('longitude').guess_bounds()
    
    return cube_proj
