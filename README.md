# gdx README


Nothing much yet. 

TODO: 

- [ ] dask chunks
- [ ] interface for classic vs mdim, and helpers
- [ ] indicators for presence of subdatasets, mdim-capability, driver recognition, GCPs/RCPs, geolocation arrays


```python
dsn1 = "vrt:///vsicurl/https://s3.ap-southeast-2.amazonaws.com/ausseabed-public-warehouse-bathymetry/L3/6009f454-290d-4c9a-a43d-00b254681696/Australian_Bathymetry_and_Topography_2023_250m_MSL_cog.tif?outsize=12,0"
dsn2 = "vrt:///vsicurl/https://projects.pawsey.org.au/idea-10.7289-v5sq8xb5/www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access/avhrr/198109/oisst-avhrr-v02r01.19810901.nc?sd_name=sst"

import gdx
gdx.my_open_dataset(dsn1)

gdx.my_open_dataset(dsn2)


```

  
## Code of Conduct
  
Please note that the gdx project is released with a [Contributor Code of Conduct](https://contributor-covenant.org/version/2/1/CODE_OF_CONDUCT.html). By contributing to this project, you agree to abide by its terms.