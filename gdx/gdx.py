from xarray.backends import BackendEntrypoint
import numpy
from xarray import Dataset, DataArray

def my_open_dataset0(filename_or_obj, drop_variables): 
  c = range(10)
  a = numpy.zeros(10)
  ds = Dataset(data_vars = dict(athing = ("coord", a)), 
        coords =  dict(x = c), 
        attrs = {})
  return(ds)

from osgeo import gdal
gdal.UseExceptions()
dsn = "vrt:///vsicurl/https://s3.ap-southeast-2.amazonaws.com/ausseabed-public-warehouse-bathymetry/L3/6009f454-290d-4c9a-a43d-00b254681696/Australian_Bathymetry_and_Topography_2023_250m_MSL_cog.tif?outsize=12,0"
dsn = "/vsicurl/https://projects.pawsey.org.au/idea-10.7289-v5sq8xb5/www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access/avhrr/198109/oisst-avhrr-v02r01.19810901.nc"
def build_coords(dataset):
  gt = dataset.GetGeoTransform()  
  dm = (dataset.RasterXSize, dataset.RasterYSize)
  cx = [gt[0] + x * gt[1] for x in range(dm[0])]
  cy = [gt[3] + x * gt[5] for x in range(dm[1])]
  return(dict(y = cy, x = cx))

def my_open_dataset(filename_or_obj, drop_variables, mdim): 
  of_type = None
  if mdim: 
    of_type = gdal.OF_MULTIDIM_RASTER
  else: 
    of_type = gdal.OF_RASTER
  ds = gdal.OpenEx(filename_or_obj, of_type)
  if mdim: 
    rg = ds.GetRootGroup()
    md = rg.OpenMDArray("sst")
    ads = md.AsClassicDataset(3, 2)
    cd = build_coords(ads)
    a = ads.ReadAsArray()
  else: 
    a = ds.ReadAsArray()
    cd = build_coords(ds)
  ds = Dataset(data_vars = dict(array = (["y", "x"], a)), 
        coords = dict(y = cd["y"], x = cd["x"]), 
        attrs = {"mike": "sillystuff"})
  return(ds)        
  

class GDALBackend(BackendEntrypoint):
    def open_dataset(
        self,
        filename_or_obj,
        *,
        drop_variables=None,
        mdim = False
        # other backend specific keyword arguments
        # `chunks` and `cache` DO NOT go here, they are handled by xarray
    ):
        return my_open_dataset(filename_or_obj, drop_variables=drop_variables, mdim = mdim)

    open_dataset_parameters = ["filename_or_obj", "drop_variables"]

    def guess_can_open(self, filename_or_obj):
        try:
            _, ext = os.path.splitext(filename_or_obj)
        except TypeError:
            return False
        return ext in {".my_format", ".my_fmt"}

    description = "Use GDAL source descriptions in Xarray"

    url = "https://link_to/your_backend/documentation"
