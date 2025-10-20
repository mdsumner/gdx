
<!-- README.md is generated from README.Rmd. Please edit that file -->

# gdx

<!-- badges: start -->

<!-- badges: end -->

The goal of gdx is to integrate GDAL with xarray, especially for the
multidimensional API which is still relatively underutilized.

## Todo

- [ ] apply xarray indexes when relevant in Raster and Multidim
- [ ] explore when we need to control driver choice
- [ ] compare to opening with GDAL itself after `mdim mosaic`

Here’s a basic example, this could be registered as an xarray backend
*engine*.

``` python
from gdx import GDALBackendEntrypoint
backend = GDALBackendEntrypoint()
dsn =  "/vsicurl/https://projects.pawsey.org.au/idea-sealevel-glo-phy-l4-nrt-008-046/data.marine.copernicus.eu/SEALEVEL_GLO_PHY_L4_NRT_008_046/cmems_obs-sl_glo_phy-ssh_nrt_allsat-l4-duacs-0.125deg_P1D_202506/2025/08/nrt_global_allsat_phy_l4_20250825_20250825.nc"
ds = backend.open_dataset(f'vrt://{dsn}?sd_name=vgos', chunks = {})
ds1 = backend.open_dataset(dsn, multidim = True, chunks = {}) 


ds.band_1.isel(x = 0)
# <xarray.DataArray 'band_1' (y: 1440)> Size: 6kB
# dask.array<getitem, shape=(1440,), dtype=int32, chunksize=(1440,), chunktype=numpy.ndarray>
# Coordinates:
#     x        float64 8B -180.0
#   * y        (y) float64 12kB 90.0 89.88 89.75 89.62 ... -89.62 -89.75 -89.88
# Attributes:
#     nodata:   -2147483647.0
#     scale:    0.0001
#     offset:   0.0
    
## the raw values for now
ds.band_1.sel(x = 100, y = -50).values
# array(441, dtype=int32)


ds1.sla.isel(longitude = 0, latitude = 1000).values
#array([2404], dtype=int32)


big_virtual_mdim = "/vsicurl/https://gist.githubusercontent.com/mdsumner/18c5d302d00b9a456bb73d30ac758764/raw/f26e1b2e202f759d6aace4d7deb3e04ea3c85f15/mdim.vrt"

bvm = backend.open_dataset(big_virtual_mdim, multidim = True, chunks = {})
# <xarray.Dataset> Size: 3TB
# Dimensions:   (Time: 5479, st_ocean: 51, yt_ocean: 1500, xt_ocean: 3600)
# Coordinates:
#   * Time      (Time) float64 44kB 1.132e+04 1.132e+04 ... 1.68e+04 1.68e+04
#   * st_ocean  (st_ocean) float64 408B 2.5 7.5 12.5 ... 3.603e+03 4.509e+03
#   * yt_ocean  (yt_ocean) float64 12kB -74.95 -74.85 -74.75 ... 74.75 74.85 74.95
#   * xt_ocean  (xt_ocean) float64 29kB 0.05 0.15 0.25 0.35 ... 359.8 359.9 360.0
# Data variables:
#     temp      (Time, st_ocean, yt_ocean, xt_ocean) int16 3TB dask.array<chunksize=(5479, 51, 1500, 3600), meta=np.ndarray>
    

bvm.sel(xt_ocean = slice(140, 150), yt_ocean = slice(-55, -45), st_ocean = slice(8, 13)).isel(Time = -1).temp.values

# array([[[-30770, -30784, -30799, ..., -30418, -30424, -30445],
#         [-30755, -30771, -30788, ..., -30418, -30425, -30446],
#         [-30744, -30764, -30788, ..., -30417, -30426, -30448],
#         ...,
#         [-29852, -29868, -29889, ..., -29413, -29338, -29325],
#         [-29835, -29851, -29883, ..., -29385, -29327, -29324],
#         [-29821, -29840, -29879, ..., -29353, -29319, -29322]]],
#       shape=(1, 100, 100), dtype=int16)
```

Lots to do, make sure scaling happens on compute() with .values, convert
from mdim mosaic to xarray, …

Let’s template a bunch of netcdf files out there. (Note this requires
GDAL\>=3.12.0 which isn’t actually yet).

``` python
month = "202501"
url = [f"/vsicurl/https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access/avhrr/{month}/oisst-avhrr-v02r01.{month}{(day+1):02d}.nc" for day in range(31)]
gdal.Run("mdim mosaic", input = url, output =  "oisst.vrt", array = "sst")
from gdx import GDALBackendEntrypoint
backend = GDALBackendEntrypoint()

backend.open_dataset("oisst.vrt", multidim = True)

# <xarray.Dataset> Size: 64MB
# Dimensions:  (lat: 720, lon: 1440, time: 31, zlev: 1)
# Coordinates:
#   * lat      (lat) float64 6kB -89.88 -89.62 -89.38 -89.12 ... 89.38 89.62 89.88
#   * lon      (lon) float64 12kB 0.125 0.375 0.625 0.875 ... 359.4 359.6 359.9
#   * time     (time) float64 248B 1.717e+04 1.72e+04 ... 1.717e+04 1.717e+04
#   * zlev     (zlev) float64 8B 0.0
# Data variables:
#     sst      (time, zlev, lat, lon) int16 64MB ...
# 
```

## Code of Conduct

Please note that the gdx project is released with a [Contributor Code of
Conduct](https://contributor-covenant.org/version/2/1/CODE_OF_CONDUCT.html).
By contributing to this project, you agree to abide by its terms.
