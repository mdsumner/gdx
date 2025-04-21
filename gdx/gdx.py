from xarray.backends import BackendEntrypoint
import numpy
from xarray import Dataset, DataArray
from osgeo import gdal
gdal.UseExceptions()

def build_coords(dataset):
      gt = dataset.GetGeoTransform()  
      dm = (dataset.RasterXSize, dataset.RasterYSize)
      cx = [gt[0] + x * gt[1] for x in range(dm[0])]
      cy = [gt[3] + x * gt[5] for x in range(dm[1])]
      return(dict(y = cy, x = cx))
    
def my_open_dataset(filename_or_obj, drop_variables = None): 
      of_type = gdal.OF_RASTER
      ds = gdal.OpenEx(filename_or_obj, of_type)
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
