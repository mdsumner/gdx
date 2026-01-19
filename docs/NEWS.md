## [0.1.0] - 2025-01-20

- Fix: Dask `_meta` probe (zero-sized slices) no longer triggers GDAL reads
- Fix: Slice start/stop of `0` now parsed correctly 
- `chunks={}` uses native GDAL block sizes for optimal chunking
- `multidim=True` is now the default for `open_dataset()`
