from xarray.backends import BackendArray
import xarray 
import numpy as np
import xarray.core.indexing as indexing


from xarray.backends import BackendEntrypoint
import numpy
from xarray import Dataset, DataArray
from osgeo import gdal
gdal.UseExceptions()



class GDALBackendArray(BackendArray):
    def __init__(
        self,
        shape,
        dtype,
        lock,
        # other backend specific keyword arguments
    ):
        self.shape = shape
        self.dtype = dtype
        self.lock = lock
        
    ## MDSumner 2025-04-22
    ## _get_indexer lifted entirely from rioxarray https://github.com/corteva/rioxarray/blob/f97bf9b85c3daa565c3ae123872b42fef58ea1b5/rioxarray/_io.py#L364
    def _get_indexer(self, key):
        """Get indexer for rasterio array.

        Parameter
        ---------
        key: tuple of int

        Returns
        -------
        band_key: an indexer for the 1st dimension
        window: two tuples. Each consists of (start, stop).
        squeeze_axis: axes to be squeezed
        np_ind: indexer for loaded numpy array

        See also
        --------
        indexing.decompose_indexer
        """
        if len(key) != 3:
            raise RioXarrayError("rasterio datasets should always be 3D")

        # bands cannot be windowed but they can be listed
        band_key = key[0]
        np_inds = []
        # bands (axis=0) cannot be windowed but they can be listed
        if isinstance(band_key, slice):
            start, stop, step = band_key.indices(self.shape[0])
            band_key = numpy.arange(start, stop, step)
        # be sure we give out a list
        band_key = (numpy.asarray(band_key) + 1).tolist()
        if isinstance(band_key, list):  # if band_key is not a scalar
            np_inds.append(slice(None))

        # but other dims can only be windowed
        window = []
        squeeze_axis = []
        for iii, (ikey, size) in enumerate(zip(key[1:], self.shape[1:])):
            if isinstance(ikey, slice):
                # step is always positive. see indexing.decompose_indexer
                start, stop, step = ikey.indices(size)
                np_inds.append(slice(None, None, step))
            elif is_scalar(ikey):
                # windowed operations will always return an array
                # we will have to squeeze it later
                squeeze_axis.append(-(2 - iii))
                start = ikey
                stop = ikey + 1
            else:
                start, stop = numpy.min(ikey), numpy.max(ikey) + 1
                np_inds.append(ikey - start)
            window.append((start, stop))

        if isinstance(key[1], numpy.ndarray) and isinstance(key[2], numpy.ndarray):
            # do outer-style indexing
            np_inds[-2:] = numpy.ix_(*np_inds[-2:])

        return band_key, tuple(window), tuple(squeeze_axis), tuple(np_inds)
    
    ## lifted from rioxarray _getitem_ see comment above
    def _outer_indexing_method(self, key):
        band_key, window, squeeze_axis, np_inds = self._get_indexer(key)
        if not band_key or any(start == stop for (start, stop) in window):
            # no need to do IO
            shape = (len(band_key),) + tuple(stop - start for (start, stop) in window)
            out = numpy.zeros(shape, dtype=self.dtype)
        else:
            with self.lock:
                ds = gdal.OpenEx(self.open_dataset_params[0], gdal.OF_RASTER)
                out = gdal.ReadAsArray(band_key, window[0], window[1])
        #if squeeze_axis:
        #    out = numpy.squeeze(out, axis=squeeze_axis)
        return out[np_inds]
      
    def __getitem__(
        self, key: indexing.ExplicitIndexer
    ) -> np.typing.ArrayLike:
        return indexing.explicit_indexing_adapter(
            key,
            self.shape,
            indexing.IndexingSupport.OUTER,
            self._outer_indexing_method,
        )

    def _raw_indexing_method(self, key: tuple) -> np.typing.ArrayLike:
        # thread safe method that access to data on disk
        with self.lock:
            ...
            return item







def build_coords(dataset):
      gt = dataset.GetGeoTransform()  
      dm = (dataset.RasterXSize, dataset.RasterYSize)
      cx = [gt[0] + x * gt[1] for x in range(dm[0])]
      cy = [gt[3] + x * gt[5] for x in range(dm[1])]
      return(dict(y = cy, x = cx))
    
def lazy_gdal_dataset(filename_or_obj, drop_variables = None): 
  ds = gdal.OpenEx(filename_or_obj, gdal.OF_RASTER)
  ## just assuming we have Float32 here because example does for now
  backend_array = GDALBackendArray(shape = (ds.RasterCount, ds.RasterXSize, ds.RasterYSize), dtype = np.float32, lock = True)
  data = indexing.LazilyIndexedArray(backend_array)
  dims = ["band", "y", "x"]
  attrs = {}
  encoding = {}
  var = xarray.Variable(dims, data, attrs=attrs, encoding=encoding)
  return(var)

# def my_open_dataset(filename_or_obj, drop_variables = None): 
#       of_type = gdal.OF_RASTER
#       ds = gdal.OpenEx(filename_or_obj, of_type)
#       a = ds.ReadAsArray()
#       cd = build_coords(ds)
#       ds = Dataset(data_vars = dict(array = (["y", "x"], a)), 
#         coords = dict(y = cd["y"], x = cd["x"]), 
#         attrs = {"mike": "sillystuff"})
#       return(ds) 
#     
class GDALBackendEntryPoint(BackendEntrypoint):
    def open_dataset(
        self,
        filename_or_obj,
        *,
        drop_variables=None
        # other backend specific keyword arguments
        # `chunks` and `cache` DO NOT go here, they are handled by xarray
    ):
        return lazy_gdal_dataset(filename_or_obj, drop_variables=drop_variables)
    open_dataset_parameters = ["filename_or_obj", "drop_variables"]

    def guess_can_open(self, filename_or_obj):
        try:
            _, ds = gdal.Open(filename_or_obj)
        except TypeError:
            return False
        return True

    description = "Use GDAL source descriptions in Xarray"

    url = "https://github.com/mdsumner/gdx"
