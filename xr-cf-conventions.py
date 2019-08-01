"""
High-level functions to generate Conventions-1.4 compliant netCDF files of 
projected datasets using xarray.

"""



def create_grid_mapping(crs):
    srs = osr.SpatialReference()
    srs.ImportFromProj4(crs) 
    gm = xr.DataArray(0, encoding={'dtype': np.dtype('int8')})
    gm.attrs['projected_crs_name'] = srs.GetAttrValue('projcs')
    gm.attrs['grid_mapping_name'] = 'universal_transverse_mercator'
    gm.attrs['scale_factor_at_central_origin'] = srs.GetProjParm('scale_factor')
    gm.attrs['standard_parallel'] = srs.GetProjParm('latitude_of_origin')
    gm.attrs['straight_vertical_longitude_from_pole'] = srs.GetProjParm('central_meridian')
    gm.attrs['false_easting'] = srs.GetProjParm('false_easting')
    gm.attrs['false_northing'] = srs.GetProjParm('false_northing')
    gm.attrs['latitude_of_projection_origin'] = srs.GetProjParm('latitude_of_origin')

    return gm



def create_latlon_da(x_name, y_name):

	S2 = georaster.SingleBandRaster(fileB2, load_data=False)
    lon, lat = S2.coordinates(latlon=True)
    S2 = None

    coords_geo = {y_name: S2vals[y_name], x_name: S2vals[x_name]}

    encoding = {'_FillValue': -9999., 
                'dtype': 'int16', 
                'scale_factor': 0.000000001}

    lon_array = xr.DataArray(lon, coords=coords_geo, dims=['y', 'x'],
                             encoding=encoding)
    lon_array.attrs['grid_mapping'] = proj_info.attrs['grid_mapping_name']
    lon_array.attrs['units'] = 'degrees'
    lon_array.attrs['standard_name'] = 'longitude'

    lat_array = xr.DataArray(lat, coords=coords_geo, dims=['y', 'x'],
                             encoding=encoding)
    lat_array.attrs['grid_mapping'] = proj_info.attrs['grid_mapping_name']
    lat_array.attrs['units'] = 'degrees'
    lat_array.attrs['standard_name'] = 'latitude'

    return (lon_array, lat_array)



def add_geo_info(ds, x_name, y_name, author, title):

	# add metadata for dataset
    ds.attrs['Conventions'] = 'CF-1.4'
    ds.attrs['Author'] = netcdf_metadata['author']
    ds.attrs['title'] = netcdf_metadata['title']

    # Additional geo-referencing
    ds.attrs['nx'] = len(ds[x_name])
    ds.attrs['ny'] = len(ds[y_name])
    ds.attrs['xmin'] = float(ds[x_name].min())
    ds.attrs['ymax'] = float(ds[y_name].max())
    ds.attrs['spacing'] = ds[x_name].isel()

    # NC conventions metadata for dimensions variables
    ds[x_name].attrs['units'] = 'meters'
    ds[x_name].attrs['standard_name'] = 'projection_x_coordinate'
    ds[x_name].attrs['point_spacing'] = 'even'
    ds[x_name].attrs['axis'] = 'x'

    ds[y_name].attrs['units'] = 'meters'
    ds[y_name].attrs['standard_name'] = 'projection_y_coordinate'
    ds[y_name].attrs['point_spacing'] = 'even'
    ds[y_name].attrs['axis'] = 'y'

    return ds