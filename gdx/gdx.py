import xarray as xr
from xarray.backends import BackendEntrypoint, BackendArray
from xarray.core import indexing
import numpy as np
import dask.array as da
from osgeo import gdal
from typing import Iterable, Optional


class GDALBackendArray(BackendArray):
    """Wrapper around GDAL dataset that implements xarray's BackendArray interface."""
    
    def __init__(self, dataset, band_index=1):
        self.dataset = dataset
        self.band_index = band_index
        self.band = dataset.GetRasterBand(band_index)
        
        # Get shape and dtype
        self._shape = (dataset.RasterYSize, dataset.RasterXSize)
        
        # Map GDAL data types to numpy dtypes
        gdal_dtype = self.band.DataType
        self._dtype = self._gdal_to_numpy_dtype(gdal_dtype)
    
    @staticmethod
    def _gdal_to_numpy_dtype(gdal_dtype):
        """Convert GDAL data type to numpy dtype."""
        dtype_map = {
            gdal.GDT_Byte: np.uint8,
            gdal.GDT_UInt16: np.uint16,
            gdal.GDT_Int16: np.int16,
            gdal.GDT_UInt32: np.uint32,
            gdal.GDT_Int32: np.int32,
            gdal.GDT_Float32: np.float32,
            gdal.GDT_Float64: np.float64,
            gdal.GDT_CInt16: np.complex64,
            gdal.GDT_CInt32: np.complex64,
            gdal.GDT_CFloat32: np.complex64,
            gdal.GDT_CFloat64: np.complex128,
        }
        return dtype_map.get(gdal_dtype, np.float32)
    
    @property
    def shape(self):
        return self._shape
    
    @property
    def dtype(self):
        return np.dtype(self._dtype)
    
    @property
    def ndim(self):
        return len(self._shape)
    
    @property
    def size(self):
        return np.prod(self._shape)
    
    @property
    def ndim(self):
        return len(self._shape)
    
    def __getitem__(self, key):
        # Handle direct array indexing
        if isinstance(key, tuple):
            return self._raw_indexing_method(key)
        else:
            return self._raw_indexing_method((key,))
    
    def _raw_indexing_method(self, key):
        """Read data from GDAL using basic indexing."""
        # Ensure we have a tuple
        if len(key) != 2:
            raise IndexError(f"Expected 2D index, got {len(key)}D")
        
        y_idx, x_idx = key
        
        # Convert integers and slices to window parameters
        if isinstance(y_idx, int):
            y_start, y_size = y_idx, 1
            squeeze_y = True
        elif isinstance(y_idx, slice):
            y_start = y_idx.start or 0
            y_stop = y_idx.stop or self.shape[0]
            y_size = y_stop - y_start
            squeeze_y = False
        else:
            raise IndexError(f"Unsupported y index type: {type(y_idx)}")
        
        if isinstance(x_idx, int):
            x_start, x_size = x_idx, 1
            squeeze_x = True
        elif isinstance(x_idx, slice):
            x_start = x_idx.start or 0
            x_stop = x_idx.stop or self.shape[1]
            x_size = x_stop - x_start
            squeeze_x = False
        else:
            raise IndexError(f"Unsupported x index type: {type(x_idx)}")
        
        # Read from GDAL
        data = self.band.ReadAsArray(
            xoff=x_start,
            yoff=y_start,
            win_xsize=x_size,
            win_ysize=y_size
        )
        
        # Squeeze dimensions if we indexed with integers
        if squeeze_y and squeeze_x:
            return data[0, 0]
        elif squeeze_y:
            return data[0, :]
        elif squeeze_x:
            return data[:, 0]
        else:
            return data


class GDALMultiDimArray(BackendArray):
    """Wrapper around GDAL multidimensional array."""
    
    def __init__(self, mdarray):
        self.mdarray = mdarray
        
        # Get shape and dtype from multidim array
        dims = mdarray.GetDimensions()
        self._shape = tuple(dim.GetSize() for dim in dims)
        
        # Get numpy dtype
        gdal_dtype = mdarray.GetDataType().GetNumericDataType()
        self._dtype = GDALBackendArray._gdal_to_numpy_dtype(gdal_dtype)
    
    @property
    def shape(self):
        return self._shape
    
    @property
    def dtype(self):
        return self._dtype
    
    def __getitem__(self, key):
        # Handle direct array indexing
        if not isinstance(key, tuple):
            key = (key,)
        return self._raw_indexing_method(key)
    
    def _raw_indexing_method(self, key):
        """Read data from GDAL multidim array."""
        # Convert key to array of slices
        if not isinstance(key, tuple):
            key = (key,)
        
        # Build start, count, and step arrays for GDAL
        ndim = len(self.shape)
        starts = []
        counts = []
        steps = []
        
        for i, k in enumerate(key):
            if isinstance(k, slice):
                start = k.start or 0
                stop = k.stop or self.shape[i]
                step = k.step or 1
                count = (stop - start + step - 1) // step
            elif isinstance(k, int):
                start = k
                count = 1
                step = 1
            else:
                raise IndexError(f"Unsupported index type: {type(k)}")
            
            starts.append(start)
            counts.append(count)
            steps.append(step)
        print("another array")
        print(starts)
        print(counts)
        print(steps)
        # Read from GDAL multidim array
        data = self.mdarray.ReadAsArray(
            array_start_idx=starts,
            count=counts,
            array_step=steps
        )
        
        return data


class GDALBackendEntrypoint(BackendEntrypoint):
    """Xarray backend for reading geospatial files with GDAL."""
    
    available = True
    
    def open_dataset(
        self,
        filename_or_obj,
        *,
        drop_variables=None,
        chunks=None,
        multidim=False,
        group=None,
        **kwargs
    ):
        """
        Open a dataset using GDAL.
        
        Parameters
        ----------
        filename_or_obj : str
            Path to the file to open
        drop_variables : list, optional
            Variables to drop from the dataset
        chunks : dict, optional
            Chunk sizes for Dask arrays
        multidim : bool, default False
            If True, use GDAL multidimensional API (OpenEx with OF_MULTIDIM_RASTER)
            If False, use standard raster API
        group : str, optional
            Group path for multidimensional datasets (e.g., "/group/subgroup")
        **kwargs
            Additional backend-specific options
        """
        
        if multidim:
            return self._open_multidim(filename_or_obj, chunks, group, drop_variables)
        else:
            return self._open_raster(filename_or_obj, chunks, drop_variables)
    
    def _open_raster(self, filename_or_obj, chunks, drop_variables):
        """Open using standard GDAL raster API."""
        
        # Open with GDAL
        dataset = gdal.Open(filename_or_obj, gdal.GA_ReadOnly)
        if dataset is None:
            raise ValueError(f"Could not open {filename_or_obj} with GDAL")
        
        # Get geotransform for coordinates
        geotransform = dataset.GetGeoTransform()
        
        # Calculate coordinates
        x_coords = np.arange(dataset.RasterXSize) * geotransform[1] + geotransform[0]
        y_coords = np.arange(dataset.RasterYSize) * geotransform[5] + geotransform[3]
        
        # Get CRS
        projection = dataset.GetProjection()
        
        # Create data variables for each band
        data_vars = {}
        num_bands = dataset.RasterCount
        
        for band_idx in range(1, num_bands + 1):
            band = dataset.GetRasterBand(band_idx)
            band_name = band.GetDescription() or f"band_{band_idx}"
            
            if drop_variables and band_name in drop_variables:
                continue
            
            # Create backend array
            backend_array = GDALBackendArray(dataset, band_idx)
            
            # Wrap with Dask if chunks specified
            if chunks is not None:
                dask_array = da.from_array(
                    backend_array,
                    chunks=chunks,
                    name=f"gdal-{filename_or_obj}-{band_name}",
                    asarray=False
                )
                data = dask_array
            else:
                data = backend_array
            
            # Get band metadata
            band_attrs = {
                'nodata': band.GetNoDataValue(),
                'scale': band.GetScale() or 1.0,
                'offset': band.GetOffset() or 0.0,
            }
            band_attrs = {k: v for k, v in band_attrs.items() if v is not None}
            
            # Create DataArray
            data_vars[band_name] = xr.DataArray(
                data,
                dims=["y", "x"],
                attrs=band_attrs
            )
        
        # Create coordinates
        coords = {
            "x": x_coords,
            "y": y_coords,
        }
        
        # Create dataset
        ds = xr.Dataset(data_vars, coords=coords)
        
        # Add global attributes
        ds.attrs['crs'] = projection
        ds.attrs['geotransform'] = geotransform
        
        return ds
    
    def _open_multidim(self, filename_or_obj, chunks, group, drop_variables):
        """Open using GDAL multidimensional API."""
        
        # Open with multidimensional API
        dataset = gdal.OpenEx(filename_or_obj, gdal.OF_MULTIDIM_RASTER | gdal.GA_ReadOnly)
        if dataset is None:
            raise ValueError(f"Could not open {filename_or_obj} with GDAL multidim API")
        
        # Get root group
        root_group = dataset.GetRootGroup()
        if root_group is None:
            raise ValueError(f"No root group found in {filename_or_obj}")
        
        # Navigate to specified group if provided
        if group:
            target_group = root_group.OpenGroup(group)
            if target_group is None:
                raise ValueError(f"Group {group} not found")
        else:
            target_group = root_group
        
        # Get arrays from the group
        array_names = target_group.GetMDArrayNames()
        
        data_vars = {}
        coords = {}
        
        for array_name in array_names:
            if drop_variables and array_name in drop_variables:
                continue
            
            mdarray = target_group.OpenMDArray(array_name)
            if mdarray is None:
                continue
            
            # Get dimensions
            dims = mdarray.GetDimensions()
            dim_names = [dim.GetName() or f"dim_{i}" for i, dim in enumerate(dims)]
            
            # Create backend array
            backend_array = GDALMultiDimArray(mdarray)
            
            # Wrap with Dask if chunks specified
            if chunks is not None:
                # Convert chunks dict to tuple based on dim names
                chunk_tuple = tuple(
                    chunks.get(dim_name, -1) for dim_name in dim_names
                )
                dask_array = da.from_array(
                    backend_array,
                    chunks=chunk_tuple,
                    name=f"gdal-multidim-{filename_or_obj}-{array_name}",
                    asarray=False
                )
                data = dask_array
            else:
                data = backend_array
            
            # Get attributes
            attrs = {}
            md = mdarray.GetAttributes()
            for attr in md:
                attr_name = attr.GetName()
                attr_value = attr.Read()
                if attr_value is not None:
                    attrs[attr_name] = attr_value
            
            # Check if this is a coordinate variable
            is_coord = any(dim.GetName() == array_name for dim in dims)
            
            if is_coord and len(dim_names) == 1:
                # Add as coordinate
                coords[array_name] = xr.DataArray(data, dims=dim_names, attrs=attrs)
            else:
                # Add as data variable
                data_vars[array_name] = xr.DataArray(data, dims=dim_names, attrs=attrs)
                
                # Create coordinate arrays for each dimension if not already present
                for dim, dim_name in zip(dims, dim_names):
                    if dim_name not in coords and dim_name not in data_vars:
                        # Create simple index coordinate
                        coords[dim_name] = np.arange(dim.GetSize())
        
        # Get group attributes
        group_attrs = {}
        group_md = target_group.GetAttributes()
        for attr in group_md:
            attr_name = attr.GetName()
            attr_value = attr.Read()
            if attr_value is not None:
                group_attrs[attr_name] = attr_value
        
        # Create dataset
        #ds = xr.Dataset(data_vars, coords=coords, attrs=group_attrs)
        
        return {"data_vars": data_vars, "coords": coords}
    
    def guess_can_open(self, filename_or_obj):
        """Guess if this backend can open the file."""
        if isinstance(filename_or_obj, str):
            try:
                ds = gdal.Open(filename_or_obj, gdal.GA_ReadOnly)
                if ds is not None:
                    ds = None
                    return True
            except:
                pass
        return False


# Register the backend
#xr.backends.register_backend("gdal", GDALBackendEntrypoint)



# Example usage:
if __name__ == "__main__":
    # Method 1: Standard raster mode
    backend = GDALBackendEntrypoint()
    ds_raster = backend.open_dataset(
        "path/to/your/file.tif",
        chunks=None
    )
    print("Raster mode:")
    print(ds_raster)
    #print(ds_raster['band_1'][0:100, 0:100])
    # Method 2: Multidimensional mode
    ds_multidim = backend.open_dataset(
        "path/to/your/CS2WFA_25km_201007.nc",
        multidim=True,
        chunks={}
    )
    print("\nMultidim mode:")
    print(ds_multidim)
    # 
    # # Method 3: Multidimensional mode with group
    # ds_group = backend.open_dataset(
    #     "path/to/your/file.hdf5",
    #     multidim=True,
    #     group="/my/data/group",
    #     chunks={"time": 1, "lat": 256, "lon": 256}
    # )
    # print("\nMultidim mode with group:")
    # print(ds_group)
