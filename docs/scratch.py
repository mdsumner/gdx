## rinse repeat for working from RStudio:
# system("rm -rf ~/lib/python3.10/site-packages/gdx")
# system("rm -rf build")
# ". ~/workenv/bin/activate"
# "uv pip install ."
# reticulate::use_python("~/workenv/bin/python3")
# reticulate::repl_python()
## -----------------------------------------------

from gdx import GDALBackendEntrypoint
backend = GDALBackendEntrypoint()
from osgeo import gdal
gdal.UseExceptions()
gdal.SetConfigOption("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
gdal.SetConfigOption("GS_NO_SIGN_REQUEST", "YES")
dsn =  "/vsicurl/https://projects.pawsey.org.au/idea-sealevel-glo-phy-l4-nrt-008-046/data.marine.copernicus.eu/SEALEVEL_GLO_PHY_L4_NRT_008_046/cmems_obs-sl_glo_phy-ssh_nrt_allsat-l4-duacs-0.125deg_P1D_202506/2025/08/nrt_global_allsat_phy_l4_20250825_20250825.nc"
ds = backend.open_dataset(f'vrt://{dsn}?sd_name=vgos', chunks = {})
#ds.band_1.isel(x = 0).values

ds = backend.open_dataset(dsn, multidim = True, chunks = {}) 
ds.sla.isel(longitude = 0, latitude = 1000).values
# import xarray
# xarray.open_dataset(dsn, engine = "gdal")
big_virtual_mdim = "/vsicurl/https://gist.githubusercontent.com/mdsumner/18c5d302d00b9a456bb73d30ac758764/raw/f26e1b2e202f759d6aace4d7deb3e04ea3c85f15/mdim.vrt"
ds = backend.open_dataset(big_virtual_mdim, multidim = True, chunks = {}) 


ds = backend.open_dataset(big, multidim = True, chunks = {}) 
ds
ds.isel(xt_ocean=2000, yt_ocean=1000, Time = 0).temp.values


gs = "/vsigs/gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"
ds = backend.open_dataset(gs, multidim = True, chunks = {})

ds  = ds["10m_u_component_of_wind"].isel(time = 1000000).values



# ds = xarray.open_zarr(
#     'gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3',
#     chunks=None,
#     storage_options=dict(token='anon'),
# )
#  ds["10m_u_component_of_wind"].isel(time = 1000000).values
# array([[ 0.02293867,  0.02293867,  0.02293867, ...,  0.02293867,
#          0.02293867,  0.02293867],
#        [-1.4116697 , -1.4050103 , -1.3983511 , ..., -1.426891  ,
#         -1.4221344 , -1.4173777 ],
#        [-1.6875559 , -1.6780427 , -1.6656753 , ..., -1.7113392 ,
#         -1.7008746 , -1.6932639 ],
#        ...,
#        [-3.5759494 , -3.5664363 , -3.5521662 , ..., -3.6082947 ,
#         -3.5949762 , -3.5835602 ],
#        [-3.0270312 , -3.018469  , -3.0089557 , ..., -3.0479603 ,
#         -3.041301  , -3.0336905 ],
#        [ 0.34639144,  0.34639144,  0.34639144, ...,  0.34639144,
#          0.34639144,  0.34639144]], shape=(721, 1440), dtype=float32)
# 



url = "https://s3.waw3-1.cloudferro.com/mdl-arco-time-025/arco/GLOBAL_MULTIYEAR_PHY_001_030/cmems_mod_glo_phy_my_0.083deg_P1D-m_202311/timeChunked.zarr"
#data.marine.copernicus.eu/SEALEVEL_GLO_PHY_L4_MY_008_047/cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.25deg_P1D_202112/1993/01/dt_global_allsat_phy_l4_19930101_20210726.nc

#https://s3.waw3-1.cloudferro.com/mdl-arco-time-025/arco/SEALEVEL_GLO_PHY_L4_MY_008_047/cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.25deg_P1D_202112/timeChunked.zarr
dsn = f"ZARR:\"/vsicurl/{url}\""

from gdx import GDALBackendEntrypoint
backend = GDALBackendEntrypoint()

from osgeo import gdal
gdal.UseExceptions()
gdal.SetConfigOption("GDAL_HTTP_HEADER_FILE", "/perm_storage/home/mdsumner/cmemsdata")

gdal.SetConfigOption("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
backend.open_dataset(dsn, multidim = True, chunks = None)
