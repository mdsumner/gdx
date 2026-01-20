import time
filename_or_obj = "/rdsi/PUBLIC/raad/data/ftp.cdc.noaa.gov/Datasets/noaa.oisst.v2/sst.mnmean.nc"
from gdx import GDALBackendEntrypoint
backend = GDALBackendEntrypoint()
t0 = time.time()
ds = backend.open_dataset(filename_or_obj, multidim = True, chunks = None)
print(f"open time: {time.time() - t0:.3f}s")
t0 = time.time()
ds = backend.open_dataset(filename_or_obj, multidim = True, chunks = {})
print(f"open time: {time.time() - t0:.3f}s")



dsntime = 'ZARR:"/vsicurl/https://s3.waw3-1.cloudferro.com/mdl-arco-time-045/arco/SEALEVEL_GLO_PHY_L4_MY_008_047/cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.125deg_P1D_202411/timeChunked.zarr"'
dsngeo = 'ZARR:"/vsicurl/https://s3.waw3-1.cloudferro.com/mdl-arco-geo-045/arco/SEALEVEL_GLO_PHY_L4_MY_008_047/cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.125deg_P1D_202411/geoChunked.zarr"'

from gdx import GDALBackendEntrypoint
backend = GDALBackendEntrypoint()
#ds = backend.open_dataset(filename_or_obj, multidim = True, chunks = None)
dstime = backend.open_dataset(dsntime, multidim = True, chunks = {})
dsgeo = backend.open_dataset(dsngeo, multidim = True, chunks = {})

# geoChunked
dsgeo.adt.sel(longitude = slice(147, 152), latitude = slice(-44, -43), time = slice("2020-01-01", "2020-01-10")).values
## timeChunked
dstime.adt.sel(longitude = slice(147, 148), latitude = slice(-44, -43), time = slice("2022-01-01", "2022-01-03")).values



#adt = ds.sel(longitude = slice(147, 152), latitude = slice(-44, -43),  time  = slice(18682, 18690)).adt
ds.adt.sel(longitude = slice(147, 152), latitude = slice(-44, -43), time = slice(18682, 18690)).mean(dim = ("longitude", "latitude")).values

#ds.adt.sel(longitude = slice(147, 152), latitude = slice(-44, -43), time = slice("2020-01-01", "2020-01-10")).mean(dim = ("longitude", "latitude")).values


from osgeo import gdal
import numpy as np
import xarray as xr
import dask.array as da


exec(open("gdx/gdx.py").read())

# --- Parameters ---
filename_or_obj = 'ZARR:"/vsicurl/https://s3.waw3-1.cloudferro.com/mdl-arco-time-045/arco/SEALEVEL_GLO_PHY_L4_MY_008_047/cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.125deg_P1D_202411/timeChunked.zarr"'
#filename_or_obj = "/rdsi/PUBLIC/raad/data/ftp.cdc.noaa.gov/Datasets/noaa.oisst.v2/sst.mnmean.nc"
chunks = {}  # or None, or {"time": 1, "latitude": 512, "longitude": 1024}
group = None
drop_variables = None

# --- Open dataset ---
dataset = gdal.OpenEx(filename_or_obj, gdal.OF_MULTIDIM_RASTER | gdal.GA_ReadOnly)
assert dataset is not None, f"Could not open {filename_or_obj}"

# --- Get root group ---
root_group = dataset.GetRootGroup()
assert root_group is not None

# --- Navigate to group ---
if group:
    target_group = root_group.OpenGroup(group)
else:
    target_group = root_group

# --- Get array names ---
array_names = target_group.GetMDArrayNames()
print(f"Found {len(array_names)} arrays: {array_names}")

# --- Process one array (pick one to inspect) ---
array_name = array_names[2]  # change this to explore
print(f"\nProcessing: {array_name}")

mdarray = target_group.OpenMDArray(array_name)

# --- Get dimensions ---
dims = mdarray.GetDimensions()
dim_names = [dim.GetName() or f"dim_{i}" for i, dim in enumerate(dims)]
dim_sizes = [dim.GetSize() for dim in dims]
print(f"Dimensions: {list(zip(dim_names, dim_sizes))}")


# --- Chunking logic ---
if chunks is not None:
    if chunks == {}:
        # auto chunks - get native block size from GDAL
        block_size = mdarray.GetBlockSize()
        print(f"Native block size: {block_size}")
        
        # GetBlockSize() returns in array order, 0 means "whole dimension"
        chunk_tuple = tuple(
            b if b > 0 else dim_sizes[i] 
            for i, b in enumerate(block_size)
        )
    else:
        chunk_tuple = tuple(chunks.get(dim_name, -1) for dim_name in dim_names)
    print(f"Chunk tuple: {chunk_tuple}")

# --- Create backend array (you'll need your GDALMultiDimArray class) ---
backend_array = GDALMultiDimArray(mdarray)
    
# This is where the dask graph gets built:
#dask_array = da.from_array(backend_array, chunks=chunk_tuple, asarray=False)


import time

# Single array - should be fast
t0 = time.time()
dask_array = da.from_array(backend_array, chunks=(1, 512, 1024), asarray=False)
print(f"da.from_array: {time.time() - t0:.3f}s")

# Wrapping in DataArray?
t0 = time.time()
da_xr = xr.DataArray(dask_array, dims=["time", "latitude", "longitude"])
print(f"xr.DataArray: {time.time() - t0:.3f}s")

# Full loop over all arrays?
t0 = time.time()
for array_name in array_names:
    mdarray = target_group.OpenMDArray(array_name)
    print(f"Loop over arrays: {time.time() - t0:.3f}s")




# --- Attributes ---
attrs = {}
for attr in mdarray.GetAttributes():
    attr_name = attr.GetName()
    attr_value = attr.Read()
    if attr_value is not None:
        attrs[attr_name] = attr_value
print(f"Attributes: {list(attrs.keys())}")

# --- Is it a coordinate? ---
is_coord = any(dim.GetName() == array_name for dim in dims)
print(f"Is coordinate: {is_coord}")



from osgeo import gdal
filename_or_obj = 'ZARR:"/vsicurl/https://s3.waw3-1.cloudferro.com/mdl-arco-time-045/arco/SEALEVEL_GLO_PHY_L4_MY_008_047/cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.125deg_P1D_202411/timeChunked.zarr"'
exec(open("gdx/gdx.py").read())

dataset = gdal.OpenEx(filename_or_obj, gdal.OF_MULTIDIM_RASTER | gdal.GA_ReadOnly)
root_group = dataset.GetRootGroup()
array_names = root_group.GetMDArrayNames()

# Just one array
mdarray = root_group.OpenMDArray(array_names[4])
dims = mdarray.GetDimensions()
block_size = mdarray.GetBlockSize()
backend_array = GDALMultiDimArray(mdarray)

# Now the critical one - does THIS hang?
t0 = time.time()
chunk_tuple = (1, 512, 1024)
dask_array = da.from_array(backend_array, chunks=chunk_tuple, asarray=False)
print(f"da.from_array: {time.time() - t0:.3f}s")
