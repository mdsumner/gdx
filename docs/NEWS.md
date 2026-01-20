## [0.2.0] - 2025-01-20

### Fixed
- Fixed slice index parsing where `0` was incorrectly treated as `None` due to Python's falsy evaluation (`k.start or 0` → `k.start if k.start is not None else 0`).

### Added
- CF datetime decoding for time coordinates using `units` from `MDArray.GetUnit()` and `calendar` attribute.
- Backend arrays accessible via `ds['var'].encoding['gdal_backend']` for debugging and introspection.
- GDAL dataset and group objects retained in `ds.encoding['gdal_dataset']` and `ds.encoding['gdal_group']` to keep MDArray methods functional.

### Changed
- Re-enabled `AdviseRead` for chunk-aligned prefetching on remote datasets.

## [0.1.0] - 2025-01-20

- Fixed Dask lazy loading for remote Zarr datasets. Zero-sized slice requests (used by Dask for `_meta` inference) no longer hang or attempt full array allocation.
- Fix: Slice start/stop of `0` now parsed correctly 
- `chunks={}` now uses native block sizes from GDAL's `GetBlockSize()`, aligning Dask chunks with storage chunks for efficient reads.
- `multidim=True` is now the default for `open_dataset()`
