
<!-- README.md is generated from README.Rmd. Please edit that file -->

# gdx

<!-- badges: start -->

<!-- badges: end -->

The goal of gdx is to integrate GDAL with xarray, especially for the
multidimensional API which is still relatively underutilized.

## Todo

- [x] apply xarray indexes when relevant in Raster
- [ ] apply xarray indexes when relevant in Multidim
- [ ] define stance on representation of “default transform”, and when
  GCPs, RPCs, or geolocation arrays are present
- [ ] explore when we need to control driver choice (netcdf and hdf in
  particular)
- [ ] explore registering as an xarray backend, via `engine = "gdal"`

Here’s a basic example:

``` python
from gdx import GDALBackendEntrypoint
backend = GDALBackendEntrypoint()
dsn =  "/vsicurl/https://projects.pawsey.org.au/idea-sealevel-glo-phy-l4-nrt-008-046/data.marine.copernicus.eu/SEALEVEL_GLO_PHY_L4_NRT_008_046/cmems_obs-sl_glo_phy-ssh_nrt_allsat-l4-duacs-0.125deg_P1D_202506/2025/08/nrt_global_allsat_phy_l4_20250825_20250825.nc"
ds = backend.open_dataset(f'vrt://{dsn}?sd_name=vgos', chunks = {}, multidim = False)
ds1 = backend.open_dataset(dsn, multidim = True, chunks = {}) 
```

We have a Raster xarray:

``` python
ds

<xarray.Dataset> Size: 17MB
Dimensions:  (x: 2880, y: 1440)
Coordinates:
  * x        (x) float64 23kB -180.0 -179.9 -179.8 -179.6 ... 179.6 179.8 179.9
  * y        (y) float64 12kB 90.0 89.88 89.75 89.62 ... -89.62 -89.75 -89.88
Data variables:
    band_1   (y, x) int32 17MB dask.array<chunksize=(1440, 2880), meta=np.ndarray>
Attributes:
    crs:           GEOGCS["unknown",DATUM["unnamed",SPHEROID["Spheroid",63781...
    geotransform:  (-180.0, 0.125, 0.0, 90.0, 0.0, -0.125)
```

and a Multidim xarray:

``` python
ds1

<xarray.Dataset> Size: 166MB
Dimensions:    (latitude: 1440, nv: 2, longitude: 2880, time: 1)
Coordinates:
  * latitude   (latitude) float32 6kB -89.94 -89.81 -89.69 ... 89.69 89.81 89.94
  * nv         (nv) int32 8B 0 1
  * longitude  (longitude) float32 12kB -179.9 -179.8 -179.7 ... 179.8 179.9
  * time       (time) float32 4B 2.763e+04
Data variables:
    lat_bnds   (latitude, nv) float32 12kB dask.array<chunksize=(1440, 2), meta=np.ndarray>
    lon_bnds   (longitude, nv) float32 23kB dask.array<chunksize=(2880, 2), meta=np.ndarray>
    sla        (time, latitude, longitude) int32 17MB dask.array<chunksize=(1, 1440, 2880), meta=np.ndarray>
    err_sla    (time, latitude, longitude) int32 17MB dask.array<chunksize=(1, 1440, 2880), meta=np.ndarray>
    ugosa      (time, latitude, longitude) int32 17MB dask.array<chunksize=(1, 1440, 2880), meta=np.ndarray>
    err_ugosa  (time, latitude, longitude) int32 17MB dask.array<chunksize=(1, 1440, 2880), meta=np.ndarray>
    vgosa      (time, latitude, longitude) int32 17MB dask.array<chunksize=(1, 1440, 2880), meta=np.ndarray>
    err_vgosa  (time, latitude, longitude) int32 17MB dask.array<chunksize=(1, 1440, 2880), meta=np.ndarray>
    adt        (time, latitude, longitude) int32 17MB dask.array<chunksize=(1, 1440, 2880), meta=np.ndarray>
    ugos       (time, latitude, longitude) int32 17MB dask.array<chunksize=(1, 1440, 2880), meta=np.ndarray>
    vgos       (time, latitude, longitude) int32 17MB dask.array<chunksize=(1, 1440, 2880), meta=np.ndarray>
    flag_ice   (time, latitude, longitude) int32 17MB dask.array<chunksize=(1, 1440, 2880), meta=np.ndarray>
Attributes: (12/44)
    Conventions:                     CF-1.6
    Metadata_Conventions:            Unidata Dataset Discovery v1.0
    cdm_data_type:                   Grid
    comment:                         Sea Surface Height measured by Altimetry...
    contact:                         servicedesk.cmems@mercator-ocean.eu
    creator_email:                   servicedesk.cmems@mercator-ocean.eu
    ...                              ...
    summary:                         DUACS Near-Real-Time Level-4 sea surface...
    time_coverage_duration:          P1D
    time_coverage_end:               2025-08-25T12:00:00Z
    time_coverage_resolution:        P1D
    time_coverage_start:             2025-08-24T12:00:00Z
    title:                           NRT merged all satellites Global Ocean G...
```

There’s one variable called ‘band_1’ for the raster:

``` python
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
```

we can access actual values

``` python
## the raw values for now
ds.band_1.sel(x = 100, y = -50, method = "nearest").values
#> array(441, dtype=int32)

ds1.sla.isel(longitude = 0, latitude = 1000).values
#> array([2404], dtype=int32)
```

What about a ZARR from CMEMS?

``` python
from gdx import GDALBackendEntrypoint
dsn = 'ZARR:"/vsicurl/https://s3.waw3-1.cloudferro.com/mdl-arco-time-045/arco/SEALEVEL_GLO_PHY_L4_MY_008_047/cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.125deg_P1D_202411/timeChunked.zarr"'
backend = GDALBackendEntrypoint()
#ds = backend.open_dataset(filename_or_obj, multidim = True, chunks = None)
ds = backend.open_dataset(dsn, multidim = True, chunks = {})
ds
```

<div><svg style="position: absolute; width: 0; height: 0; overflow: hidden">
<defs>
<symbol id="icon-database" viewBox="0 0 32 32">
<path d="M16 0c-8.837 0-16 2.239-16 5v4c0 2.761 7.163 5 16 5s16-2.239 16-5v-4c0-2.761-7.163-5-16-5z"></path>
<path d="M16 17c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
<path d="M16 26c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
</symbol>
<symbol id="icon-file-text2" viewBox="0 0 32 32">
<path d="M28.681 7.159c-0.694-0.947-1.662-2.053-2.724-3.116s-2.169-2.030-3.116-2.724c-1.612-1.182-2.393-1.319-2.841-1.319h-15.5c-1.378 0-2.5 1.121-2.5 2.5v27c0 1.378 1.122 2.5 2.5 2.5h23c1.378 0 2.5-1.122 2.5-2.5v-19.5c0-0.448-0.137-1.23-1.319-2.841zM24.543 5.457c0.959 0.959 1.712 1.825 2.268 2.543h-4.811v-4.811c0.718 0.556 1.584 1.309 2.543 2.268zM28 29.5c0 0.271-0.229 0.5-0.5 0.5h-23c-0.271 0-0.5-0.229-0.5-0.5v-27c0-0.271 0.229-0.5 0.5-0.5 0 0 15.499-0 15.5 0v7c0 0.552 0.448 1 1 1h7v19.5z"></path>
<path d="M23 26h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 22h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 18h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
</symbol>
</defs>
</svg>
<style>/* CSS stylesheet for displaying xarray objects in jupyterlab.
 *
 */
&#10;:root {
  --xr-font-color0: var(
    --jp-content-font-color0,
    var(--pst-color-text-base rgba(0, 0, 0, 1))
  );
  --xr-font-color2: var(
    --jp-content-font-color2,
    var(--pst-color-text-base, rgba(0, 0, 0, 0.54))
  );
  --xr-font-color3: var(
    --jp-content-font-color3,
    var(--pst-color-text-base, rgba(0, 0, 0, 0.38))
  );
  --xr-border-color: var(
    --jp-border-color2,
    hsl(from var(--pst-color-on-background, white) h s calc(l - 10))
  );
  --xr-disabled-color: var(
    --jp-layout-color3,
    hsl(from var(--pst-color-on-background, white) h s calc(l - 40))
  );
  --xr-background-color: var(
    --jp-layout-color0,
    var(--pst-color-on-background, white)
  );
  --xr-background-color-row-even: var(
    --jp-layout-color1,
    hsl(from var(--pst-color-on-background, white) h s calc(l - 5))
  );
  --xr-background-color-row-odd: var(
    --jp-layout-color2,
    hsl(from var(--pst-color-on-background, white) h s calc(l - 15))
  );
}
&#10;html[theme="dark"],
html[data-theme="dark"],
body[data-theme="dark"],
body.vscode-dark {
  --xr-font-color0: var(
    --jp-content-font-color0,
    var(--pst-color-text-base, rgba(255, 255, 255, 1))
  );
  --xr-font-color2: var(
    --jp-content-font-color2,
    var(--pst-color-text-base, rgba(255, 255, 255, 0.54))
  );
  --xr-font-color3: var(
    --jp-content-font-color3,
    var(--pst-color-text-base, rgba(255, 255, 255, 0.38))
  );
  --xr-border-color: var(
    --jp-border-color2,
    hsl(from var(--pst-color-on-background, #111111) h s calc(l + 10))
  );
  --xr-disabled-color: var(
    --jp-layout-color3,
    hsl(from var(--pst-color-on-background, #111111) h s calc(l + 40))
  );
  --xr-background-color: var(
    --jp-layout-color0,
    var(--pst-color-on-background, #111111)
  );
  --xr-background-color-row-even: var(
    --jp-layout-color1,
    hsl(from var(--pst-color-on-background, #111111) h s calc(l + 5))
  );
  --xr-background-color-row-odd: var(
    --jp-layout-color2,
    hsl(from var(--pst-color-on-background, #111111) h s calc(l + 15))
  );
}
&#10;.xr-wrap {
  display: block !important;
  min-width: 300px;
  max-width: 700px;
}
&#10;.xr-text-repr-fallback {
  /* fallback to plain text repr when CSS is not injected (untrusted notebook) */
  display: none;
}
&#10;.xr-header {
  padding-top: 6px;
  padding-bottom: 6px;
  margin-bottom: 4px;
  border-bottom: solid 1px var(--xr-border-color);
}
&#10;.xr-header > div,
.xr-header > ul {
  display: inline;
  margin-top: 0;
  margin-bottom: 0;
}
&#10;.xr-obj-type,
.xr-array-name {
  margin-left: 2px;
  margin-right: 10px;
}
&#10;.xr-obj-type {
  color: var(--xr-font-color2);
}
&#10;.xr-sections {
  padding-left: 0 !important;
  display: grid;
  grid-template-columns: 150px auto auto 1fr 0 20px 0 20px;
}
&#10;.xr-section-item {
  display: contents;
}
&#10;.xr-section-item input {
  display: inline-block;
  opacity: 0;
  height: 0;
}
&#10;.xr-section-item input + label {
  color: var(--xr-disabled-color);
  border: 2px solid transparent !important;
}
&#10;.xr-section-item input:enabled + label {
  cursor: pointer;
  color: var(--xr-font-color2);
}
&#10;.xr-section-item input:focus + label {
  border: 2px solid var(--xr-font-color0) !important;
}
&#10;.xr-section-item input:enabled + label:hover {
  color: var(--xr-font-color0);
}
&#10;.xr-section-summary {
  grid-column: 1;
  color: var(--xr-font-color2);
  font-weight: 500;
}
&#10;.xr-section-summary > span {
  display: inline-block;
  padding-left: 0.5em;
}
&#10;.xr-section-summary-in:disabled + label {
  color: var(--xr-font-color2);
}
&#10;.xr-section-summary-in + label:before {
  display: inline-block;
  content: "►";
  font-size: 11px;
  width: 15px;
  text-align: center;
}
&#10;.xr-section-summary-in:disabled + label:before {
  color: var(--xr-disabled-color);
}
&#10;.xr-section-summary-in:checked + label:before {
  content: "▼";
}
&#10;.xr-section-summary-in:checked + label > span {
  display: none;
}
&#10;.xr-section-summary,
.xr-section-inline-details {
  padding-top: 4px;
  padding-bottom: 4px;
}
&#10;.xr-section-inline-details {
  grid-column: 2 / -1;
}
&#10;.xr-section-details {
  display: none;
  grid-column: 1 / -1;
  margin-bottom: 5px;
}
&#10;.xr-section-summary-in:checked ~ .xr-section-details {
  display: contents;
}
&#10;.xr-array-wrap {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 20px auto;
}
&#10;.xr-array-wrap > label {
  grid-column: 1;
  vertical-align: top;
}
&#10;.xr-preview {
  color: var(--xr-font-color3);
}
&#10;.xr-array-preview,
.xr-array-data {
  padding: 0 5px !important;
  grid-column: 2;
}
&#10;.xr-array-data,
.xr-array-in:checked ~ .xr-array-preview {
  display: none;
}
&#10;.xr-array-in:checked ~ .xr-array-data,
.xr-array-preview {
  display: inline-block;
}
&#10;.xr-dim-list {
  display: inline-block !important;
  list-style: none;
  padding: 0 !important;
  margin: 0;
}
&#10;.xr-dim-list li {
  display: inline-block;
  padding: 0;
  margin: 0;
}
&#10;.xr-dim-list:before {
  content: "(";
}
&#10;.xr-dim-list:after {
  content: ")";
}
&#10;.xr-dim-list li:not(:last-child):after {
  content: ",";
  padding-right: 5px;
}
&#10;.xr-has-index {
  font-weight: bold;
}
&#10;.xr-var-list,
.xr-var-item {
  display: contents;
}
&#10;.xr-var-item > div,
.xr-var-item label,
.xr-var-item > .xr-var-name span {
  background-color: var(--xr-background-color-row-even);
  border-color: var(--xr-background-color-row-odd);
  margin-bottom: 0;
  padding-top: 2px;
}
&#10;.xr-var-item > .xr-var-name:hover span {
  padding-right: 5px;
}
&#10;.xr-var-list > li:nth-child(odd) > div,
.xr-var-list > li:nth-child(odd) > label,
.xr-var-list > li:nth-child(odd) > .xr-var-name span {
  background-color: var(--xr-background-color-row-odd);
  border-color: var(--xr-background-color-row-even);
}
&#10;.xr-var-name {
  grid-column: 1;
}
&#10;.xr-var-dims {
  grid-column: 2;
}
&#10;.xr-var-dtype {
  grid-column: 3;
  text-align: right;
  color: var(--xr-font-color2);
}
&#10;.xr-var-preview {
  grid-column: 4;
}
&#10;.xr-index-preview {
  grid-column: 2 / 5;
  color: var(--xr-font-color2);
}
&#10;.xr-var-name,
.xr-var-dims,
.xr-var-dtype,
.xr-preview,
.xr-attrs dt {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 10px;
}
&#10;.xr-var-name:hover,
.xr-var-dims:hover,
.xr-var-dtype:hover,
.xr-attrs dt:hover {
  overflow: visible;
  width: auto;
  z-index: 1;
}
&#10;.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  display: none;
  border-top: 2px dotted var(--xr-background-color);
  padding-bottom: 20px !important;
  padding-top: 10px !important;
}
&#10;.xr-var-attrs-in + label,
.xr-var-data-in + label,
.xr-index-data-in + label {
  padding: 0 1px;
}
&#10;.xr-var-attrs-in:checked ~ .xr-var-attrs,
.xr-var-data-in:checked ~ .xr-var-data,
.xr-index-data-in:checked ~ .xr-index-data {
  display: block;
}
&#10;.xr-var-data > table {
  float: right;
}
&#10;.xr-var-data > pre,
.xr-index-data > pre,
.xr-var-data > table > tbody > tr {
  background-color: transparent !important;
}
&#10;.xr-var-name span,
.xr-var-data,
.xr-index-name div,
.xr-index-data,
.xr-attrs {
  padding-left: 25px !important;
}
&#10;.xr-attrs,
.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  grid-column: 1 / -1;
}
&#10;dl.xr-attrs {
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 125px auto;
}
&#10;.xr-attrs dt,
.xr-attrs dd {
  padding: 0;
  margin: 0;
  float: left;
  padding-right: 10px;
  width: auto;
}
&#10;.xr-attrs dt {
  font-weight: normal;
  grid-column: 1;
}
&#10;.xr-attrs dt:hover span {
  display: inline-block;
  background: var(--xr-background-color);
  padding-right: 10px;
}
&#10;.xr-attrs dd {
  grid-column: 2;
  white-space: pre-wrap;
  word-break: break-all;
}
&#10;.xr-icon-database,
.xr-icon-file-text2,
.xr-no-icon {
  display: inline-block;
  vertical-align: middle;
  width: 1em;
  height: 1.5em !important;
  stroke-width: 0;
  stroke: currentColor;
  fill: currentColor;
}
&#10;.xr-var-attrs-in:checked + label > .xr-icon-file-text2,
.xr-var-data-in:checked + label > .xr-icon-database,
.xr-index-data-in:checked + label > .xr-icon-database {
  color: var(--xr-font-color0);
  filter: drop-shadow(1px 1px 5px var(--xr-font-color2));
  stroke-width: 0.8px;
}
</style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt; Size: 2TB
Dimensions:         (latitude: 1440, longitude: 2880, time: 11902, nv: 2)
Coordinates:
  * latitude        (latitude) float32 6kB -89.94 -89.81 -89.69 ... 89.81 89.94
  * longitude       (longitude) float32 12kB -179.9 -179.8 ... 179.8 179.9
  * time            (time) float32 48kB 1.571e+04 1.571e+04 ... 2.761e+04
  * nv              (nv) int32 8B 0 1
Data variables: (12/13)
    adt             (time, latitude, longitude) int32 197GB dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;
    err_sla         (time, latitude, longitude) int32 197GB dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;
    err_ugosa       (time, latitude, longitude) int32 197GB dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;
    err_vgosa       (time, latitude, longitude) int32 197GB dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;
    flag_ice        (time, latitude, longitude) int32 197GB dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;
    lat_bnds        (latitude, nv) float32 12kB dask.array&lt;chunksize=(1440, 2), meta=np.ndarray&gt;
    ...              ...
    sla             (time, latitude, longitude) int32 197GB dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;
    tpa_correction  (time) int32 48kB dask.array&lt;chunksize=(1,), meta=np.ndarray&gt;
    ugos            (time, latitude, longitude) int32 197GB dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;
    ugosa           (time, latitude, longitude) int32 197GB dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;
    vgos            (time, latitude, longitude) int32 197GB dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;
    vgosa           (time, latitude, longitude) int32 197GB dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;
Attributes: (12/43)
    Conventions:                     CF-1.6
    Metadata_Conventions:            Unidata Dataset Discovery v1.0
    cdm_data_type:                   Grid
    comment:                         Sea Surface Height measured by Altimetry...
    contact:                         servicedesk.cmems@mercator-ocean.eu
    coordinates:                     lat_bnds lon_bnds
    ...                              ...
    summary:                         SSALTO/DUACS Delayed-Time Level-4 sea su...
    time_coverage_duration:          P1D
    time_coverage_end:               2023-12-31T12:00:00Z
    time_coverage_resolution:        P1D
    time_coverage_start:             2023-12-30T12:00:00Z
    title:                           DT merged all satellites Global Ocean Gr...</pre><div class='xr-wrap' style='display:none'><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-f8045985-4513-4a19-a786-f00d158a673a' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-f8045985-4513-4a19-a786-f00d158a673a' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span class='xr-has-index'>latitude</span>: 1440</li><li><span class='xr-has-index'>longitude</span>: 2880</li><li><span class='xr-has-index'>time</span>: 11902</li><li><span class='xr-has-index'>nv</span>: 2</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-d9ae7726-2f5f-4dc1-bdef-0f0ac8ca9535' class='xr-section-summary-in' type='checkbox'  checked><label for='section-d9ae7726-2f5f-4dc1-bdef-0f0ac8ca9535' class='xr-section-summary' >Coordinates: <span>(4)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>latitude</span></div><div class='xr-var-dims'>(latitude)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>-89.94 -89.81 ... 89.81 89.94</div><input id='attrs-ca60cd74-e3ab-499d-b1b9-d68cb6744cbf' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-ca60cd74-e3ab-499d-b1b9-d68cb6744cbf' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ce975dc7-e46b-443a-a242-b1b9d475345e' class='xr-var-data-in' type='checkbox'><label for='data-ce975dc7-e46b-443a-a242-b1b9d475345e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>axis :</span></dt><dd>Y</dd><dt><span>bounds :</span></dt><dd>lat_bnds</dd><dt><span>long_name :</span></dt><dd>Latitude</dd><dt><span>valid_max :</span></dt><dd>89.9375</dd><dt><span>valid_min :</span></dt><dd>-89.9375</dd></dl></div><div class='xr-var-data'><pre>array([-89.9375, -89.8125, -89.6875, ...,  89.6875,  89.8125,  89.9375],
      shape=(1440,), dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>longitude</span></div><div class='xr-var-dims'>(longitude)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>-179.9 -179.8 ... 179.8 179.9</div><input id='attrs-da4b0ba3-4b5d-48ef-acaf-acb25c7a777d' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-da4b0ba3-4b5d-48ef-acaf-acb25c7a777d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-0a3222cd-5a23-469a-b19a-e784c5c7b1c5' class='xr-var-data-in' type='checkbox'><label for='data-0a3222cd-5a23-469a-b19a-e784c5c7b1c5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>axis :</span></dt><dd>X</dd><dt><span>bounds :</span></dt><dd>lon_bnds</dd><dt><span>long_name :</span></dt><dd>Longitude</dd><dt><span>valid_max :</span></dt><dd>179.9375</dd><dt><span>valid_min :</span></dt><dd>-179.9375</dd></dl></div><div class='xr-var-data'><pre>array([-179.9375, -179.8125, -179.6875, ...,  179.6875,  179.8125,  179.9375],
      shape=(2880,), dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>1.571e+04 1.571e+04 ... 2.761e+04</div><input id='attrs-dbb79d1d-8eb0-4848-834b-3aa03bbec5f7' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-dbb79d1d-8eb0-4848-834b-3aa03bbec5f7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7d1bddef-68f6-4fbf-b941-1705a96d3845' class='xr-var-data-in' type='checkbox'><label for='data-7d1bddef-68f6-4fbf-b941-1705a96d3845' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>calendar :</span></dt><dd>gregorian</dd></dl></div><div class='xr-var-data'><pre>array([15706., 15707., 15708., ..., 27605., 27606., 27607.],
      shape=(11902,), dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>nv</span></div><div class='xr-var-dims'>(nv)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>0 1</div><input id='attrs-3703261c-25d5-4ef6-878e-ed26b5f6af96' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-3703261c-25d5-4ef6-878e-ed26b5f6af96' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-610d039a-8497-4432-982d-e27890a394ac' class='xr-var-data-in' type='checkbox'><label for='data-610d039a-8497-4432-982d-e27890a394ac' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>comment :</span></dt><dd>Vertex</dd><dt><span>long_name :</span></dt><dd>Number of cell vertices</dd></dl></div><div class='xr-var-data'><pre>array([0, 1], dtype=int32)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-dc6c13af-1a76-4f6d-9e09-cef4090b7982' class='xr-section-summary-in' type='checkbox'  checked><label for='section-dc6c13af-1a76-4f6d-9e09-cef4090b7982' class='xr-section-summary' >Data variables: <span>(13)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>adt</span></div><div class='xr-var-dims'>(time, latitude, longitude)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;</div><input id='attrs-f6f48cb2-0962-4528-bd3f-fc6627f6716b' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-f6f48cb2-0962-4528-bd3f-fc6627f6716b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a6ebb513-0f78-4ab6-827a-2a7b51b14566' class='xr-var-data-in' type='checkbox'><label for='data-a6ebb513-0f78-4ab6-827a-2a7b51b14566' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>comment :</span></dt><dd>The absolute dynamic topography is the sea surface height above geoid; the adt is obtained as follows: adt=sla+mdt where mdt is the mean dynamic topography; see the product user manual for details</dd><dt><span>coordinates :</span></dt><dd>longitude latitude</dd><dt><span>grid_mapping :</span></dt><dd>crs</dd><dt><span>long_name :</span></dt><dd>Absolute dynamic topography</dd><dt><span>standard_name :</span></dt><dd>sea_surface_height_above_geoid</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 183.88 GiB </td>
                        <td> 2.00 MiB </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (11902, 1440, 2880) </td>
                        <td> (1, 512, 1024) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 107118 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> int32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="173" height="160" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="10" y1="14" x2="80" y2="84" />
  <line x1="10" y1="28" x2="80" y2="98" />
  <line x1="10" y1="39" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="10" y2="39" style="stroke-width:2" />
  <line x1="13" y1="3" x2="13" y2="43" />
  <line x1="17" y1="7" x2="17" y2="47" />
  <line x1="21" y1="11" x2="21" y2="50" />
  <line x1="24" y1="14" x2="24" y2="54" />
  <line x1="28" y1="18" x2="28" y2="58" />
  <line x1="32" y1="22" x2="32" y2="61" />
  <line x1="36" y1="26" x2="36" y2="65" />
  <line x1="39" y1="29" x2="39" y2="69" />
  <line x1="43" y1="33" x2="43" y2="73" />
  <line x1="47" y1="37" x2="47" y2="76" />
  <line x1="50" y1="40" x2="50" y2="80" />
  <line x1="54" y1="44" x2="54" y2="84" />
  <line x1="58" y1="48" x2="58" y2="87" />
  <line x1="62" y1="52" x2="62" y2="91" />
  <line x1="65" y1="55" x2="65" y2="95" />
  <line x1="69" y1="59" x2="69" y2="99" />
  <line x1="73" y1="63" x2="73" y2="102" />
  <line x1="76" y1="66" x2="76" y2="106" />
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 80.58823529411765,70.58823529411765 80.58823529411765,110.21240153264056 10.0,39.6241662385229" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="52" y2="0" style="stroke-width:2" />
  <line x1="13" y1="3" x2="56" y2="3" />
  <line x1="17" y1="7" x2="60" y2="7" />
  <line x1="21" y1="11" x2="63" y2="11" />
  <line x1="24" y1="14" x2="67" y2="14" />
  <line x1="28" y1="18" x2="71" y2="18" />
  <line x1="32" y1="22" x2="75" y2="22" />
  <line x1="36" y1="26" x2="78" y2="26" />
  <line x1="39" y1="29" x2="82" y2="29" />
  <line x1="43" y1="33" x2="86" y2="33" />
  <line x1="47" y1="37" x2="89" y2="37" />
  <line x1="50" y1="40" x2="93" y2="40" />
  <line x1="54" y1="44" x2="97" y2="44" />
  <line x1="58" y1="48" x2="101" y2="48" />
  <line x1="62" y1="52" x2="104" y2="52" />
  <line x1="65" y1="55" x2="108" y2="55" />
  <line x1="69" y1="59" x2="112" y2="59" />
  <line x1="73" y1="63" x2="115" y2="63" />
  <line x1="76" y1="66" x2="119" y2="66" />
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="25" y1="0" x2="95" y2="70" />
  <line x1="40" y1="0" x2="111" y2="70" />
  <line x1="52" y1="0" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 52.775616481350575,0.0 123.36385177546822,70.58823529411765 80.58823529411765,70.58823529411765" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
  <line x1="80" y1="84" x2="123" y2="84" />
  <line x1="80" y1="98" x2="123" y2="98" />
  <line x1="80" y1="110" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
  <line x1="95" y1="70" x2="95" y2="110" />
  <line x1="111" y1="70" x2="111" y2="110" />
  <line x1="123" y1="70" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="80.58823529411765,70.58823529411765 123.36385177546822,70.58823529411765 123.36385177546822,110.21240153264056 80.58823529411765,110.21240153264056" style="fill:#ECB172A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="101.976044" y="130.212402" font-size="1.0rem" font-weight="100" text-anchor="middle" >2880</text>
  <text x="143.363852" y="90.400318" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,143.363852,90.400318)">1440</text>
  <text x="35.294118" y="94.918284" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(45,35.294118,94.918284)">11902</text>
</svg>
        </td>
    </tr>
</table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>err_sla</span></div><div class='xr-var-dims'>(time, latitude, longitude)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;</div><input id='attrs-26a51fb2-df14-4e05-b7d2-916b928ba32b' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-26a51fb2-df14-4e05-b7d2-916b928ba32b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e4f7d752-58a0-4c91-ad23-c042cccb4a78' class='xr-var-data-in' type='checkbox'><label for='data-e4f7d752-58a0-4c91-ad23-c042cccb4a78' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>comment :</span></dt><dd>The formal mapping error represents a purely theoretical mapping error. It mainly traduces errors induced by the constellation sampling capability and consistency with the spatial/temporal scales considered, as described in Le Traon et al (1998) or Ducet et al (2000)</dd><dt><span>coordinates :</span></dt><dd>longitude latitude</dd><dt><span>grid_mapping :</span></dt><dd>crs</dd><dt><span>long_name :</span></dt><dd>Formal mapping error</dd><dt><span>standard_name :</span></dt><dd>sea_surface_height_above_sea_level standard_error</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 183.88 GiB </td>
                        <td> 2.00 MiB </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (11902, 1440, 2880) </td>
                        <td> (1, 512, 1024) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 107118 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> int32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="173" height="160" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="10" y1="14" x2="80" y2="84" />
  <line x1="10" y1="28" x2="80" y2="98" />
  <line x1="10" y1="39" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="10" y2="39" style="stroke-width:2" />
  <line x1="13" y1="3" x2="13" y2="43" />
  <line x1="17" y1="7" x2="17" y2="47" />
  <line x1="21" y1="11" x2="21" y2="50" />
  <line x1="24" y1="14" x2="24" y2="54" />
  <line x1="28" y1="18" x2="28" y2="58" />
  <line x1="32" y1="22" x2="32" y2="61" />
  <line x1="36" y1="26" x2="36" y2="65" />
  <line x1="39" y1="29" x2="39" y2="69" />
  <line x1="43" y1="33" x2="43" y2="73" />
  <line x1="47" y1="37" x2="47" y2="76" />
  <line x1="50" y1="40" x2="50" y2="80" />
  <line x1="54" y1="44" x2="54" y2="84" />
  <line x1="58" y1="48" x2="58" y2="87" />
  <line x1="62" y1="52" x2="62" y2="91" />
  <line x1="65" y1="55" x2="65" y2="95" />
  <line x1="69" y1="59" x2="69" y2="99" />
  <line x1="73" y1="63" x2="73" y2="102" />
  <line x1="76" y1="66" x2="76" y2="106" />
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 80.58823529411765,70.58823529411765 80.58823529411765,110.21240153264056 10.0,39.6241662385229" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="52" y2="0" style="stroke-width:2" />
  <line x1="13" y1="3" x2="56" y2="3" />
  <line x1="17" y1="7" x2="60" y2="7" />
  <line x1="21" y1="11" x2="63" y2="11" />
  <line x1="24" y1="14" x2="67" y2="14" />
  <line x1="28" y1="18" x2="71" y2="18" />
  <line x1="32" y1="22" x2="75" y2="22" />
  <line x1="36" y1="26" x2="78" y2="26" />
  <line x1="39" y1="29" x2="82" y2="29" />
  <line x1="43" y1="33" x2="86" y2="33" />
  <line x1="47" y1="37" x2="89" y2="37" />
  <line x1="50" y1="40" x2="93" y2="40" />
  <line x1="54" y1="44" x2="97" y2="44" />
  <line x1="58" y1="48" x2="101" y2="48" />
  <line x1="62" y1="52" x2="104" y2="52" />
  <line x1="65" y1="55" x2="108" y2="55" />
  <line x1="69" y1="59" x2="112" y2="59" />
  <line x1="73" y1="63" x2="115" y2="63" />
  <line x1="76" y1="66" x2="119" y2="66" />
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="25" y1="0" x2="95" y2="70" />
  <line x1="40" y1="0" x2="111" y2="70" />
  <line x1="52" y1="0" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 52.775616481350575,0.0 123.36385177546822,70.58823529411765 80.58823529411765,70.58823529411765" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
  <line x1="80" y1="84" x2="123" y2="84" />
  <line x1="80" y1="98" x2="123" y2="98" />
  <line x1="80" y1="110" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
  <line x1="95" y1="70" x2="95" y2="110" />
  <line x1="111" y1="70" x2="111" y2="110" />
  <line x1="123" y1="70" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="80.58823529411765,70.58823529411765 123.36385177546822,70.58823529411765 123.36385177546822,110.21240153264056 80.58823529411765,110.21240153264056" style="fill:#ECB172A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="101.976044" y="130.212402" font-size="1.0rem" font-weight="100" text-anchor="middle" >2880</text>
  <text x="143.363852" y="90.400318" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,143.363852,90.400318)">1440</text>
  <text x="35.294118" y="94.918284" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(45,35.294118,94.918284)">11902</text>
</svg>
        </td>
    </tr>
</table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>err_ugosa</span></div><div class='xr-var-dims'>(time, latitude, longitude)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;</div><input id='attrs-34559bf1-3b23-4713-9950-c266ce3aeba1' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-34559bf1-3b23-4713-9950-c266ce3aeba1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-115012d9-8b18-47f8-bfa0-dad7ea86456b' class='xr-var-data-in' type='checkbox'><label for='data-115012d9-8b18-47f8-bfa0-dad7ea86456b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>comment :</span></dt><dd>The formal mapping error represents a purely theoretical mapping error. It mainly traduces errors induced by the constellation sampling capability and consistency with the spatial/temporal scales considered, as described in Le Traon et al (1998) or Ducet et al (2000)</dd><dt><span>coordinates :</span></dt><dd>longitude latitude</dd><dt><span>grid_mapping :</span></dt><dd>crs</dd><dt><span>long_name :</span></dt><dd>Formal mapping error on zonal geostrophic velocity anomalies</dd><dt><span>standard_name :</span></dt><dd>surface_geostrophic_eastward_sea_water_velocity_assuming_sea_level_for_geoid standard_error</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 183.88 GiB </td>
                        <td> 2.00 MiB </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (11902, 1440, 2880) </td>
                        <td> (1, 512, 1024) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 107118 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> int32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="173" height="160" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="10" y1="14" x2="80" y2="84" />
  <line x1="10" y1="28" x2="80" y2="98" />
  <line x1="10" y1="39" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="10" y2="39" style="stroke-width:2" />
  <line x1="13" y1="3" x2="13" y2="43" />
  <line x1="17" y1="7" x2="17" y2="47" />
  <line x1="21" y1="11" x2="21" y2="50" />
  <line x1="24" y1="14" x2="24" y2="54" />
  <line x1="28" y1="18" x2="28" y2="58" />
  <line x1="32" y1="22" x2="32" y2="61" />
  <line x1="36" y1="26" x2="36" y2="65" />
  <line x1="39" y1="29" x2="39" y2="69" />
  <line x1="43" y1="33" x2="43" y2="73" />
  <line x1="47" y1="37" x2="47" y2="76" />
  <line x1="50" y1="40" x2="50" y2="80" />
  <line x1="54" y1="44" x2="54" y2="84" />
  <line x1="58" y1="48" x2="58" y2="87" />
  <line x1="62" y1="52" x2="62" y2="91" />
  <line x1="65" y1="55" x2="65" y2="95" />
  <line x1="69" y1="59" x2="69" y2="99" />
  <line x1="73" y1="63" x2="73" y2="102" />
  <line x1="76" y1="66" x2="76" y2="106" />
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 80.58823529411765,70.58823529411765 80.58823529411765,110.21240153264056 10.0,39.6241662385229" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="52" y2="0" style="stroke-width:2" />
  <line x1="13" y1="3" x2="56" y2="3" />
  <line x1="17" y1="7" x2="60" y2="7" />
  <line x1="21" y1="11" x2="63" y2="11" />
  <line x1="24" y1="14" x2="67" y2="14" />
  <line x1="28" y1="18" x2="71" y2="18" />
  <line x1="32" y1="22" x2="75" y2="22" />
  <line x1="36" y1="26" x2="78" y2="26" />
  <line x1="39" y1="29" x2="82" y2="29" />
  <line x1="43" y1="33" x2="86" y2="33" />
  <line x1="47" y1="37" x2="89" y2="37" />
  <line x1="50" y1="40" x2="93" y2="40" />
  <line x1="54" y1="44" x2="97" y2="44" />
  <line x1="58" y1="48" x2="101" y2="48" />
  <line x1="62" y1="52" x2="104" y2="52" />
  <line x1="65" y1="55" x2="108" y2="55" />
  <line x1="69" y1="59" x2="112" y2="59" />
  <line x1="73" y1="63" x2="115" y2="63" />
  <line x1="76" y1="66" x2="119" y2="66" />
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="25" y1="0" x2="95" y2="70" />
  <line x1="40" y1="0" x2="111" y2="70" />
  <line x1="52" y1="0" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 52.775616481350575,0.0 123.36385177546822,70.58823529411765 80.58823529411765,70.58823529411765" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
  <line x1="80" y1="84" x2="123" y2="84" />
  <line x1="80" y1="98" x2="123" y2="98" />
  <line x1="80" y1="110" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
  <line x1="95" y1="70" x2="95" y2="110" />
  <line x1="111" y1="70" x2="111" y2="110" />
  <line x1="123" y1="70" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="80.58823529411765,70.58823529411765 123.36385177546822,70.58823529411765 123.36385177546822,110.21240153264056 80.58823529411765,110.21240153264056" style="fill:#ECB172A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="101.976044" y="130.212402" font-size="1.0rem" font-weight="100" text-anchor="middle" >2880</text>
  <text x="143.363852" y="90.400318" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,143.363852,90.400318)">1440</text>
  <text x="35.294118" y="94.918284" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(45,35.294118,94.918284)">11902</text>
</svg>
        </td>
    </tr>
</table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>err_vgosa</span></div><div class='xr-var-dims'>(time, latitude, longitude)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;</div><input id='attrs-4632fdd5-71a8-4299-a5df-3bc0c69dc34e' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-4632fdd5-71a8-4299-a5df-3bc0c69dc34e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c08848d8-3c05-4588-aa8e-e3cac6a70dcd' class='xr-var-data-in' type='checkbox'><label for='data-c08848d8-3c05-4588-aa8e-e3cac6a70dcd' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>comment :</span></dt><dd>The formal mapping error represents a purely theoretical mapping error. It mainly traduces errors induced by the constellation sampling capability and consistency with the spatial/temporal scales considered, as described in Le Traon et al (1998) or Ducet et al (2000)</dd><dt><span>coordinates :</span></dt><dd>longitude latitude</dd><dt><span>grid_mapping :</span></dt><dd>crs</dd><dt><span>long_name :</span></dt><dd>Formal mapping error on meridional geostrophic velocity anomalies</dd><dt><span>standard_name :</span></dt><dd>surface_geostrophic_northward_sea_water_velocity_assuming_sea_level_for_geoid standard_error</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 183.88 GiB </td>
                        <td> 2.00 MiB </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (11902, 1440, 2880) </td>
                        <td> (1, 512, 1024) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 107118 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> int32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="173" height="160" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="10" y1="14" x2="80" y2="84" />
  <line x1="10" y1="28" x2="80" y2="98" />
  <line x1="10" y1="39" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="10" y2="39" style="stroke-width:2" />
  <line x1="13" y1="3" x2="13" y2="43" />
  <line x1="17" y1="7" x2="17" y2="47" />
  <line x1="21" y1="11" x2="21" y2="50" />
  <line x1="24" y1="14" x2="24" y2="54" />
  <line x1="28" y1="18" x2="28" y2="58" />
  <line x1="32" y1="22" x2="32" y2="61" />
  <line x1="36" y1="26" x2="36" y2="65" />
  <line x1="39" y1="29" x2="39" y2="69" />
  <line x1="43" y1="33" x2="43" y2="73" />
  <line x1="47" y1="37" x2="47" y2="76" />
  <line x1="50" y1="40" x2="50" y2="80" />
  <line x1="54" y1="44" x2="54" y2="84" />
  <line x1="58" y1="48" x2="58" y2="87" />
  <line x1="62" y1="52" x2="62" y2="91" />
  <line x1="65" y1="55" x2="65" y2="95" />
  <line x1="69" y1="59" x2="69" y2="99" />
  <line x1="73" y1="63" x2="73" y2="102" />
  <line x1="76" y1="66" x2="76" y2="106" />
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 80.58823529411765,70.58823529411765 80.58823529411765,110.21240153264056 10.0,39.6241662385229" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="52" y2="0" style="stroke-width:2" />
  <line x1="13" y1="3" x2="56" y2="3" />
  <line x1="17" y1="7" x2="60" y2="7" />
  <line x1="21" y1="11" x2="63" y2="11" />
  <line x1="24" y1="14" x2="67" y2="14" />
  <line x1="28" y1="18" x2="71" y2="18" />
  <line x1="32" y1="22" x2="75" y2="22" />
  <line x1="36" y1="26" x2="78" y2="26" />
  <line x1="39" y1="29" x2="82" y2="29" />
  <line x1="43" y1="33" x2="86" y2="33" />
  <line x1="47" y1="37" x2="89" y2="37" />
  <line x1="50" y1="40" x2="93" y2="40" />
  <line x1="54" y1="44" x2="97" y2="44" />
  <line x1="58" y1="48" x2="101" y2="48" />
  <line x1="62" y1="52" x2="104" y2="52" />
  <line x1="65" y1="55" x2="108" y2="55" />
  <line x1="69" y1="59" x2="112" y2="59" />
  <line x1="73" y1="63" x2="115" y2="63" />
  <line x1="76" y1="66" x2="119" y2="66" />
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="25" y1="0" x2="95" y2="70" />
  <line x1="40" y1="0" x2="111" y2="70" />
  <line x1="52" y1="0" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 52.775616481350575,0.0 123.36385177546822,70.58823529411765 80.58823529411765,70.58823529411765" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
  <line x1="80" y1="84" x2="123" y2="84" />
  <line x1="80" y1="98" x2="123" y2="98" />
  <line x1="80" y1="110" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
  <line x1="95" y1="70" x2="95" y2="110" />
  <line x1="111" y1="70" x2="111" y2="110" />
  <line x1="123" y1="70" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="80.58823529411765,70.58823529411765 123.36385177546822,70.58823529411765 123.36385177546822,110.21240153264056 80.58823529411765,110.21240153264056" style="fill:#ECB172A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="101.976044" y="130.212402" font-size="1.0rem" font-weight="100" text-anchor="middle" >2880</text>
  <text x="143.363852" y="90.400318" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,143.363852,90.400318)">1440</text>
  <text x="35.294118" y="94.918284" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(45,35.294118,94.918284)">11902</text>
</svg>
        </td>
    </tr>
</table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>flag_ice</span></div><div class='xr-var-dims'>(time, latitude, longitude)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;</div><input id='attrs-44756d5b-0426-430a-83e7-72c327fd4fc9' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-44756d5b-0426-430a-83e7-72c327fd4fc9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e3a6629e-f381-4d4a-a080-ef8eb44e52f4' class='xr-var-data-in' type='checkbox'><label for='data-e3a6629e-f381-4d4a-a080-ef8eb44e52f4' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>comment :</span></dt><dd>Ice Flag based on CDR OSI SAF V3.0 products until 2020 (OSI-450_a), ICDR OSI SAF V3.0 (Interim products) from 2021 (OSI-430-a) (Lavergne et al., 2019). The flag corresponds to the 15% sea ice concentration.</dd><dt><span>coordinates :</span></dt><dd>longitude latitude</dd><dt><span>flag_meanings :</span></dt><dd>data_on_sea data_on_ice</dd><dt><span>flag_values :</span></dt><dd>(0, 1)</dd><dt><span>grid_mapping :</span></dt><dd>crs</dd><dt><span>long_name :</span></dt><dd>Ice Flag for a 15% criterion of ice concentration</dd><dt><span>standard_name :</span></dt><dd>status_flag</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 183.88 GiB </td>
                        <td> 2.00 MiB </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (11902, 1440, 2880) </td>
                        <td> (1, 512, 1024) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 107118 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> int32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="173" height="160" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="10" y1="14" x2="80" y2="84" />
  <line x1="10" y1="28" x2="80" y2="98" />
  <line x1="10" y1="39" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="10" y2="39" style="stroke-width:2" />
  <line x1="13" y1="3" x2="13" y2="43" />
  <line x1="17" y1="7" x2="17" y2="47" />
  <line x1="21" y1="11" x2="21" y2="50" />
  <line x1="24" y1="14" x2="24" y2="54" />
  <line x1="28" y1="18" x2="28" y2="58" />
  <line x1="32" y1="22" x2="32" y2="61" />
  <line x1="36" y1="26" x2="36" y2="65" />
  <line x1="39" y1="29" x2="39" y2="69" />
  <line x1="43" y1="33" x2="43" y2="73" />
  <line x1="47" y1="37" x2="47" y2="76" />
  <line x1="50" y1="40" x2="50" y2="80" />
  <line x1="54" y1="44" x2="54" y2="84" />
  <line x1="58" y1="48" x2="58" y2="87" />
  <line x1="62" y1="52" x2="62" y2="91" />
  <line x1="65" y1="55" x2="65" y2="95" />
  <line x1="69" y1="59" x2="69" y2="99" />
  <line x1="73" y1="63" x2="73" y2="102" />
  <line x1="76" y1="66" x2="76" y2="106" />
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 80.58823529411765,70.58823529411765 80.58823529411765,110.21240153264056 10.0,39.6241662385229" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="52" y2="0" style="stroke-width:2" />
  <line x1="13" y1="3" x2="56" y2="3" />
  <line x1="17" y1="7" x2="60" y2="7" />
  <line x1="21" y1="11" x2="63" y2="11" />
  <line x1="24" y1="14" x2="67" y2="14" />
  <line x1="28" y1="18" x2="71" y2="18" />
  <line x1="32" y1="22" x2="75" y2="22" />
  <line x1="36" y1="26" x2="78" y2="26" />
  <line x1="39" y1="29" x2="82" y2="29" />
  <line x1="43" y1="33" x2="86" y2="33" />
  <line x1="47" y1="37" x2="89" y2="37" />
  <line x1="50" y1="40" x2="93" y2="40" />
  <line x1="54" y1="44" x2="97" y2="44" />
  <line x1="58" y1="48" x2="101" y2="48" />
  <line x1="62" y1="52" x2="104" y2="52" />
  <line x1="65" y1="55" x2="108" y2="55" />
  <line x1="69" y1="59" x2="112" y2="59" />
  <line x1="73" y1="63" x2="115" y2="63" />
  <line x1="76" y1="66" x2="119" y2="66" />
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="25" y1="0" x2="95" y2="70" />
  <line x1="40" y1="0" x2="111" y2="70" />
  <line x1="52" y1="0" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 52.775616481350575,0.0 123.36385177546822,70.58823529411765 80.58823529411765,70.58823529411765" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
  <line x1="80" y1="84" x2="123" y2="84" />
  <line x1="80" y1="98" x2="123" y2="98" />
  <line x1="80" y1="110" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
  <line x1="95" y1="70" x2="95" y2="110" />
  <line x1="111" y1="70" x2="111" y2="110" />
  <line x1="123" y1="70" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="80.58823529411765,70.58823529411765 123.36385177546822,70.58823529411765 123.36385177546822,110.21240153264056 80.58823529411765,110.21240153264056" style="fill:#ECB172A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="101.976044" y="130.212402" font-size="1.0rem" font-weight="100" text-anchor="middle" >2880</text>
  <text x="143.363852" y="90.400318" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,143.363852,90.400318)">1440</text>
  <text x="35.294118" y="94.918284" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(45,35.294118,94.918284)">11902</text>
</svg>
        </td>
    </tr>
</table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>lat_bnds</span></div><div class='xr-var-dims'>(latitude, nv)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(1440, 2), meta=np.ndarray&gt;</div><input id='attrs-6371171a-0899-4e69-b627-c9bdc5de0c6c' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-6371171a-0899-4e69-b627-c9bdc5de0c6c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-acbe09bf-5d96-418c-8210-d4f33ad54b10' class='xr-var-data-in' type='checkbox'><label for='data-acbe09bf-5d96-418c-8210-d4f33ad54b10' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>comment :</span></dt><dd>latitude values at the north and south bounds of each pixel.</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 11.25 kiB </td>
                        <td> 11.25 kiB </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (1440, 2) </td>
                        <td> (1440, 2) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 1 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> float32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="75" height="170" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="0" y1="0" x2="25" y2="0" style="stroke-width:2" />
  <line x1="0" y1="120" x2="25" y2="120" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="0" y1="0" x2="0" y2="120" style="stroke-width:2" />
  <line x1="25" y1="0" x2="25" y2="120" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="0.0,0.0 25.412616514582485,0.0 25.412616514582485,120.0 0.0,120.0" style="fill:#ECB172A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="12.706308" y="140.000000" font-size="1.0rem" font-weight="100" text-anchor="middle" >2</text>
  <text x="45.412617" y="60.000000" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,45.412617,60.000000)">1440</text>
</svg>
        </td>
    </tr>
</table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>lon_bnds</span></div><div class='xr-var-dims'>(longitude, nv)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(2880, 2), meta=np.ndarray&gt;</div><input id='attrs-cf889fba-694a-48f6-a84c-90e0d8ac95cd' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-cf889fba-694a-48f6-a84c-90e0d8ac95cd' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ce04abfb-1158-48a0-8701-112cd110afe8' class='xr-var-data-in' type='checkbox'><label for='data-ce04abfb-1158-48a0-8701-112cd110afe8' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>comment :</span></dt><dd>longitude values at the west and east bounds of each pixel.</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 22.50 kiB </td>
                        <td> 22.50 kiB </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (2880, 2) </td>
                        <td> (2880, 2) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 1 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> float32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="75" height="170" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="0" y1="0" x2="25" y2="0" style="stroke-width:2" />
  <line x1="0" y1="120" x2="25" y2="120" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="0" y1="0" x2="0" y2="120" style="stroke-width:2" />
  <line x1="25" y1="0" x2="25" y2="120" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="0.0,0.0 25.412616514582485,0.0 25.412616514582485,120.0 0.0,120.0" style="fill:#ECB172A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="12.706308" y="140.000000" font-size="1.0rem" font-weight="100" text-anchor="middle" >2</text>
  <text x="45.412617" y="60.000000" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,45.412617,60.000000)">2880</text>
</svg>
        </td>
    </tr>
</table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>sla</span></div><div class='xr-var-dims'>(time, latitude, longitude)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;</div><input id='attrs-b46d6b40-ae35-4f32-a4b0-52d1832d8410' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-b46d6b40-ae35-4f32-a4b0-52d1832d8410' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5269612f-40b9-4715-b4e2-fceeadddda29' class='xr-var-data-in' type='checkbox'><label for='data-5269612f-40b9-4715-b4e2-fceeadddda29' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>ancillary_variables :</span></dt><dd>err_sla</dd><dt><span>comment :</span></dt><dd>The sea level anomaly is the sea surface height above mean sea surface; it is referenced to the [1993, 2012] period; see the product user manual for details</dd><dt><span>coordinates :</span></dt><dd>longitude latitude</dd><dt><span>grid_mapping :</span></dt><dd>crs</dd><dt><span>long_name :</span></dt><dd>Sea level anomaly</dd><dt><span>standard_name :</span></dt><dd>sea_surface_height_above_sea_level</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 183.88 GiB </td>
                        <td> 2.00 MiB </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (11902, 1440, 2880) </td>
                        <td> (1, 512, 1024) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 107118 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> int32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="173" height="160" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="10" y1="14" x2="80" y2="84" />
  <line x1="10" y1="28" x2="80" y2="98" />
  <line x1="10" y1="39" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="10" y2="39" style="stroke-width:2" />
  <line x1="13" y1="3" x2="13" y2="43" />
  <line x1="17" y1="7" x2="17" y2="47" />
  <line x1="21" y1="11" x2="21" y2="50" />
  <line x1="24" y1="14" x2="24" y2="54" />
  <line x1="28" y1="18" x2="28" y2="58" />
  <line x1="32" y1="22" x2="32" y2="61" />
  <line x1="36" y1="26" x2="36" y2="65" />
  <line x1="39" y1="29" x2="39" y2="69" />
  <line x1="43" y1="33" x2="43" y2="73" />
  <line x1="47" y1="37" x2="47" y2="76" />
  <line x1="50" y1="40" x2="50" y2="80" />
  <line x1="54" y1="44" x2="54" y2="84" />
  <line x1="58" y1="48" x2="58" y2="87" />
  <line x1="62" y1="52" x2="62" y2="91" />
  <line x1="65" y1="55" x2="65" y2="95" />
  <line x1="69" y1="59" x2="69" y2="99" />
  <line x1="73" y1="63" x2="73" y2="102" />
  <line x1="76" y1="66" x2="76" y2="106" />
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 80.58823529411765,70.58823529411765 80.58823529411765,110.21240153264056 10.0,39.6241662385229" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="52" y2="0" style="stroke-width:2" />
  <line x1="13" y1="3" x2="56" y2="3" />
  <line x1="17" y1="7" x2="60" y2="7" />
  <line x1="21" y1="11" x2="63" y2="11" />
  <line x1="24" y1="14" x2="67" y2="14" />
  <line x1="28" y1="18" x2="71" y2="18" />
  <line x1="32" y1="22" x2="75" y2="22" />
  <line x1="36" y1="26" x2="78" y2="26" />
  <line x1="39" y1="29" x2="82" y2="29" />
  <line x1="43" y1="33" x2="86" y2="33" />
  <line x1="47" y1="37" x2="89" y2="37" />
  <line x1="50" y1="40" x2="93" y2="40" />
  <line x1="54" y1="44" x2="97" y2="44" />
  <line x1="58" y1="48" x2="101" y2="48" />
  <line x1="62" y1="52" x2="104" y2="52" />
  <line x1="65" y1="55" x2="108" y2="55" />
  <line x1="69" y1="59" x2="112" y2="59" />
  <line x1="73" y1="63" x2="115" y2="63" />
  <line x1="76" y1="66" x2="119" y2="66" />
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="25" y1="0" x2="95" y2="70" />
  <line x1="40" y1="0" x2="111" y2="70" />
  <line x1="52" y1="0" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 52.775616481350575,0.0 123.36385177546822,70.58823529411765 80.58823529411765,70.58823529411765" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
  <line x1="80" y1="84" x2="123" y2="84" />
  <line x1="80" y1="98" x2="123" y2="98" />
  <line x1="80" y1="110" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
  <line x1="95" y1="70" x2="95" y2="110" />
  <line x1="111" y1="70" x2="111" y2="110" />
  <line x1="123" y1="70" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="80.58823529411765,70.58823529411765 123.36385177546822,70.58823529411765 123.36385177546822,110.21240153264056 80.58823529411765,110.21240153264056" style="fill:#ECB172A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="101.976044" y="130.212402" font-size="1.0rem" font-weight="100" text-anchor="middle" >2880</text>
  <text x="143.363852" y="90.400318" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,143.363852,90.400318)">1440</text>
  <text x="35.294118" y="94.918284" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(45,35.294118,94.918284)">11902</text>
</svg>
        </td>
    </tr>
</table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>tpa_correction</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(1,), meta=np.ndarray&gt;</div><input id='attrs-a2eecdac-7993-49a2-bf62-620a4f11286c' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-a2eecdac-7993-49a2-bf62-620a4f11286c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e6eb24bb-827b-4018-b21e-c90e276884b7' class='xr-var-data-in' type='checkbox'><label for='data-e6eb24bb-827b-4018-b21e-c90e276884b7' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>comment :</span></dt><dd>NOT IMPLEMENTED YET: This correction is not yet available for the current product version. This field will be updated once this correction is producted. This variable can be added to the gridded SLA to correct for the observed instrumental drift during the lifetime of the TOPEX-A mission (the correction is null after this period). This is a global correction to be added a posteriori (and not before) on the global mean sea level estimate derived from the gridded sea level map. It can be applied at regional or local scale as a best estimate (better than no correction, since the regional variation of the instrumental drift is unknown). See product manual for more details.</dd><dt><span>long_name :</span></dt><dd>TOPEX-A instrumental drift correction derived from altimetry and tide gauges global comparisons (WCRP Sea Level Budget Group, 2018)</dd><dt><span>standard_name :</span></dt><dd>sea_surface_height_above_sea_level</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 46.49 kiB </td>
                        <td> 4 B </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (11902,) </td>
                        <td> (1,) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 11902 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> int32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="170" height="75" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="0" y1="0" x2="120" y2="0" style="stroke-width:2" />
  <line x1="0" y1="25" x2="120" y2="25" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="0" y1="0" x2="0" y2="25" style="stroke-width:2" />
  <line x1="6" y1="0" x2="6" y2="25" />
  <line x1="12" y1="0" x2="12" y2="25" />
  <line x1="18" y1="0" x2="18" y2="25" />
  <line x1="25" y1="0" x2="25" y2="25" />
  <line x1="31" y1="0" x2="31" y2="25" />
  <line x1="37" y1="0" x2="37" y2="25" />
  <line x1="44" y1="0" x2="44" y2="25" />
  <line x1="50" y1="0" x2="50" y2="25" />
  <line x1="56" y1="0" x2="56" y2="25" />
  <line x1="63" y1="0" x2="63" y2="25" />
  <line x1="69" y1="0" x2="69" y2="25" />
  <line x1="75" y1="0" x2="75" y2="25" />
  <line x1="82" y1="0" x2="82" y2="25" />
  <line x1="88" y1="0" x2="88" y2="25" />
  <line x1="94" y1="0" x2="94" y2="25" />
  <line x1="101" y1="0" x2="101" y2="25" />
  <line x1="107" y1="0" x2="107" y2="25" />
  <line x1="113" y1="0" x2="113" y2="25" />
  <line x1="120" y1="0" x2="120" y2="25" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="0.0,0.0 120.0,0.0 120.0,25.412616514582485 0.0,25.412616514582485" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="60.000000" y="45.412617" font-size="1.0rem" font-weight="100" text-anchor="middle" >11902</text>
  <text x="140.000000" y="12.706308" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(0,140.000000,12.706308)">1</text>
</svg>
        </td>
    </tr>
</table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>ugos</span></div><div class='xr-var-dims'>(time, latitude, longitude)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;</div><input id='attrs-807df42d-61e9-40b1-8153-c53701661e13' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-807df42d-61e9-40b1-8153-c53701661e13' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7230e99e-301f-41cd-a839-f903bc18b7f3' class='xr-var-data-in' type='checkbox'><label for='data-7230e99e-301f-41cd-a839-f903bc18b7f3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>coordinates :</span></dt><dd>longitude latitude</dd><dt><span>grid_mapping :</span></dt><dd>crs</dd><dt><span>long_name :</span></dt><dd>Absolute geostrophic velocity: zonal component</dd><dt><span>standard_name :</span></dt><dd>surface_geostrophic_eastward_sea_water_velocity</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 183.88 GiB </td>
                        <td> 2.00 MiB </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (11902, 1440, 2880) </td>
                        <td> (1, 512, 1024) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 107118 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> int32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="173" height="160" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="10" y1="14" x2="80" y2="84" />
  <line x1="10" y1="28" x2="80" y2="98" />
  <line x1="10" y1="39" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="10" y2="39" style="stroke-width:2" />
  <line x1="13" y1="3" x2="13" y2="43" />
  <line x1="17" y1="7" x2="17" y2="47" />
  <line x1="21" y1="11" x2="21" y2="50" />
  <line x1="24" y1="14" x2="24" y2="54" />
  <line x1="28" y1="18" x2="28" y2="58" />
  <line x1="32" y1="22" x2="32" y2="61" />
  <line x1="36" y1="26" x2="36" y2="65" />
  <line x1="39" y1="29" x2="39" y2="69" />
  <line x1="43" y1="33" x2="43" y2="73" />
  <line x1="47" y1="37" x2="47" y2="76" />
  <line x1="50" y1="40" x2="50" y2="80" />
  <line x1="54" y1="44" x2="54" y2="84" />
  <line x1="58" y1="48" x2="58" y2="87" />
  <line x1="62" y1="52" x2="62" y2="91" />
  <line x1="65" y1="55" x2="65" y2="95" />
  <line x1="69" y1="59" x2="69" y2="99" />
  <line x1="73" y1="63" x2="73" y2="102" />
  <line x1="76" y1="66" x2="76" y2="106" />
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 80.58823529411765,70.58823529411765 80.58823529411765,110.21240153264056 10.0,39.6241662385229" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="52" y2="0" style="stroke-width:2" />
  <line x1="13" y1="3" x2="56" y2="3" />
  <line x1="17" y1="7" x2="60" y2="7" />
  <line x1="21" y1="11" x2="63" y2="11" />
  <line x1="24" y1="14" x2="67" y2="14" />
  <line x1="28" y1="18" x2="71" y2="18" />
  <line x1="32" y1="22" x2="75" y2="22" />
  <line x1="36" y1="26" x2="78" y2="26" />
  <line x1="39" y1="29" x2="82" y2="29" />
  <line x1="43" y1="33" x2="86" y2="33" />
  <line x1="47" y1="37" x2="89" y2="37" />
  <line x1="50" y1="40" x2="93" y2="40" />
  <line x1="54" y1="44" x2="97" y2="44" />
  <line x1="58" y1="48" x2="101" y2="48" />
  <line x1="62" y1="52" x2="104" y2="52" />
  <line x1="65" y1="55" x2="108" y2="55" />
  <line x1="69" y1="59" x2="112" y2="59" />
  <line x1="73" y1="63" x2="115" y2="63" />
  <line x1="76" y1="66" x2="119" y2="66" />
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="25" y1="0" x2="95" y2="70" />
  <line x1="40" y1="0" x2="111" y2="70" />
  <line x1="52" y1="0" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 52.775616481350575,0.0 123.36385177546822,70.58823529411765 80.58823529411765,70.58823529411765" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
  <line x1="80" y1="84" x2="123" y2="84" />
  <line x1="80" y1="98" x2="123" y2="98" />
  <line x1="80" y1="110" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
  <line x1="95" y1="70" x2="95" y2="110" />
  <line x1="111" y1="70" x2="111" y2="110" />
  <line x1="123" y1="70" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="80.58823529411765,70.58823529411765 123.36385177546822,70.58823529411765 123.36385177546822,110.21240153264056 80.58823529411765,110.21240153264056" style="fill:#ECB172A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="101.976044" y="130.212402" font-size="1.0rem" font-weight="100" text-anchor="middle" >2880</text>
  <text x="143.363852" y="90.400318" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,143.363852,90.400318)">1440</text>
  <text x="35.294118" y="94.918284" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(45,35.294118,94.918284)">11902</text>
</svg>
        </td>
    </tr>
</table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>ugosa</span></div><div class='xr-var-dims'>(time, latitude, longitude)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;</div><input id='attrs-972d1180-eded-4936-af56-e8dc4a5dc93c' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-972d1180-eded-4936-af56-e8dc4a5dc93c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fb072af3-8efe-4f18-ac93-8d9f1fbd5fba' class='xr-var-data-in' type='checkbox'><label for='data-fb072af3-8efe-4f18-ac93-8d9f1fbd5fba' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>ancillary_variables :</span></dt><dd>err_ugosa</dd><dt><span>comment :</span></dt><dd>The geostrophic velocity anomalies are referenced to the [1993, 2012] period</dd><dt><span>coordinates :</span></dt><dd>longitude latitude</dd><dt><span>grid_mapping :</span></dt><dd>crs</dd><dt><span>long_name :</span></dt><dd>Geostrophic velocity anomalies: zonal component</dd><dt><span>standard_name :</span></dt><dd>surface_geostrophic_eastward_sea_water_velocity_assuming_sea_level_for_geoid</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 183.88 GiB </td>
                        <td> 2.00 MiB </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (11902, 1440, 2880) </td>
                        <td> (1, 512, 1024) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 107118 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> int32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="173" height="160" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="10" y1="14" x2="80" y2="84" />
  <line x1="10" y1="28" x2="80" y2="98" />
  <line x1="10" y1="39" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="10" y2="39" style="stroke-width:2" />
  <line x1="13" y1="3" x2="13" y2="43" />
  <line x1="17" y1="7" x2="17" y2="47" />
  <line x1="21" y1="11" x2="21" y2="50" />
  <line x1="24" y1="14" x2="24" y2="54" />
  <line x1="28" y1="18" x2="28" y2="58" />
  <line x1="32" y1="22" x2="32" y2="61" />
  <line x1="36" y1="26" x2="36" y2="65" />
  <line x1="39" y1="29" x2="39" y2="69" />
  <line x1="43" y1="33" x2="43" y2="73" />
  <line x1="47" y1="37" x2="47" y2="76" />
  <line x1="50" y1="40" x2="50" y2="80" />
  <line x1="54" y1="44" x2="54" y2="84" />
  <line x1="58" y1="48" x2="58" y2="87" />
  <line x1="62" y1="52" x2="62" y2="91" />
  <line x1="65" y1="55" x2="65" y2="95" />
  <line x1="69" y1="59" x2="69" y2="99" />
  <line x1="73" y1="63" x2="73" y2="102" />
  <line x1="76" y1="66" x2="76" y2="106" />
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 80.58823529411765,70.58823529411765 80.58823529411765,110.21240153264056 10.0,39.6241662385229" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="52" y2="0" style="stroke-width:2" />
  <line x1="13" y1="3" x2="56" y2="3" />
  <line x1="17" y1="7" x2="60" y2="7" />
  <line x1="21" y1="11" x2="63" y2="11" />
  <line x1="24" y1="14" x2="67" y2="14" />
  <line x1="28" y1="18" x2="71" y2="18" />
  <line x1="32" y1="22" x2="75" y2="22" />
  <line x1="36" y1="26" x2="78" y2="26" />
  <line x1="39" y1="29" x2="82" y2="29" />
  <line x1="43" y1="33" x2="86" y2="33" />
  <line x1="47" y1="37" x2="89" y2="37" />
  <line x1="50" y1="40" x2="93" y2="40" />
  <line x1="54" y1="44" x2="97" y2="44" />
  <line x1="58" y1="48" x2="101" y2="48" />
  <line x1="62" y1="52" x2="104" y2="52" />
  <line x1="65" y1="55" x2="108" y2="55" />
  <line x1="69" y1="59" x2="112" y2="59" />
  <line x1="73" y1="63" x2="115" y2="63" />
  <line x1="76" y1="66" x2="119" y2="66" />
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="25" y1="0" x2="95" y2="70" />
  <line x1="40" y1="0" x2="111" y2="70" />
  <line x1="52" y1="0" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 52.775616481350575,0.0 123.36385177546822,70.58823529411765 80.58823529411765,70.58823529411765" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
  <line x1="80" y1="84" x2="123" y2="84" />
  <line x1="80" y1="98" x2="123" y2="98" />
  <line x1="80" y1="110" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
  <line x1="95" y1="70" x2="95" y2="110" />
  <line x1="111" y1="70" x2="111" y2="110" />
  <line x1="123" y1="70" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="80.58823529411765,70.58823529411765 123.36385177546822,70.58823529411765 123.36385177546822,110.21240153264056 80.58823529411765,110.21240153264056" style="fill:#ECB172A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="101.976044" y="130.212402" font-size="1.0rem" font-weight="100" text-anchor="middle" >2880</text>
  <text x="143.363852" y="90.400318" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,143.363852,90.400318)">1440</text>
  <text x="35.294118" y="94.918284" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(45,35.294118,94.918284)">11902</text>
</svg>
        </td>
    </tr>
</table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>vgos</span></div><div class='xr-var-dims'>(time, latitude, longitude)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;</div><input id='attrs-bef664ee-6b83-4be1-8b63-70a00619d431' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-bef664ee-6b83-4be1-8b63-70a00619d431' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c556b7cd-439c-4804-96ab-88b9b21a8c02' class='xr-var-data-in' type='checkbox'><label for='data-c556b7cd-439c-4804-96ab-88b9b21a8c02' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>coordinates :</span></dt><dd>longitude latitude</dd><dt><span>grid_mapping :</span></dt><dd>crs</dd><dt><span>long_name :</span></dt><dd>Absolute geostrophic velocity: meridian component</dd><dt><span>standard_name :</span></dt><dd>surface_geostrophic_northward_sea_water_velocity</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 183.88 GiB </td>
                        <td> 2.00 MiB </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (11902, 1440, 2880) </td>
                        <td> (1, 512, 1024) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 107118 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> int32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="173" height="160" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="10" y1="14" x2="80" y2="84" />
  <line x1="10" y1="28" x2="80" y2="98" />
  <line x1="10" y1="39" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="10" y2="39" style="stroke-width:2" />
  <line x1="13" y1="3" x2="13" y2="43" />
  <line x1="17" y1="7" x2="17" y2="47" />
  <line x1="21" y1="11" x2="21" y2="50" />
  <line x1="24" y1="14" x2="24" y2="54" />
  <line x1="28" y1="18" x2="28" y2="58" />
  <line x1="32" y1="22" x2="32" y2="61" />
  <line x1="36" y1="26" x2="36" y2="65" />
  <line x1="39" y1="29" x2="39" y2="69" />
  <line x1="43" y1="33" x2="43" y2="73" />
  <line x1="47" y1="37" x2="47" y2="76" />
  <line x1="50" y1="40" x2="50" y2="80" />
  <line x1="54" y1="44" x2="54" y2="84" />
  <line x1="58" y1="48" x2="58" y2="87" />
  <line x1="62" y1="52" x2="62" y2="91" />
  <line x1="65" y1="55" x2="65" y2="95" />
  <line x1="69" y1="59" x2="69" y2="99" />
  <line x1="73" y1="63" x2="73" y2="102" />
  <line x1="76" y1="66" x2="76" y2="106" />
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 80.58823529411765,70.58823529411765 80.58823529411765,110.21240153264056 10.0,39.6241662385229" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="52" y2="0" style="stroke-width:2" />
  <line x1="13" y1="3" x2="56" y2="3" />
  <line x1="17" y1="7" x2="60" y2="7" />
  <line x1="21" y1="11" x2="63" y2="11" />
  <line x1="24" y1="14" x2="67" y2="14" />
  <line x1="28" y1="18" x2="71" y2="18" />
  <line x1="32" y1="22" x2="75" y2="22" />
  <line x1="36" y1="26" x2="78" y2="26" />
  <line x1="39" y1="29" x2="82" y2="29" />
  <line x1="43" y1="33" x2="86" y2="33" />
  <line x1="47" y1="37" x2="89" y2="37" />
  <line x1="50" y1="40" x2="93" y2="40" />
  <line x1="54" y1="44" x2="97" y2="44" />
  <line x1="58" y1="48" x2="101" y2="48" />
  <line x1="62" y1="52" x2="104" y2="52" />
  <line x1="65" y1="55" x2="108" y2="55" />
  <line x1="69" y1="59" x2="112" y2="59" />
  <line x1="73" y1="63" x2="115" y2="63" />
  <line x1="76" y1="66" x2="119" y2="66" />
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="25" y1="0" x2="95" y2="70" />
  <line x1="40" y1="0" x2="111" y2="70" />
  <line x1="52" y1="0" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 52.775616481350575,0.0 123.36385177546822,70.58823529411765 80.58823529411765,70.58823529411765" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
  <line x1="80" y1="84" x2="123" y2="84" />
  <line x1="80" y1="98" x2="123" y2="98" />
  <line x1="80" y1="110" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
  <line x1="95" y1="70" x2="95" y2="110" />
  <line x1="111" y1="70" x2="111" y2="110" />
  <line x1="123" y1="70" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="80.58823529411765,70.58823529411765 123.36385177546822,70.58823529411765 123.36385177546822,110.21240153264056 80.58823529411765,110.21240153264056" style="fill:#ECB172A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="101.976044" y="130.212402" font-size="1.0rem" font-weight="100" text-anchor="middle" >2880</text>
  <text x="143.363852" y="90.400318" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,143.363852,90.400318)">1440</text>
  <text x="35.294118" y="94.918284" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(45,35.294118,94.918284)">11902</text>
</svg>
        </td>
    </tr>
</table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>vgosa</span></div><div class='xr-var-dims'>(time, latitude, longitude)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(1, 512, 1024), meta=np.ndarray&gt;</div><input id='attrs-28100b29-b72b-4df8-8853-aeda2dc11f46' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-28100b29-b72b-4df8-8853-aeda2dc11f46' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-de327b7d-d738-4680-8325-c7f38300b553' class='xr-var-data-in' type='checkbox'><label for='data-de327b7d-d738-4680-8325-c7f38300b553' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>ancillary_variables :</span></dt><dd>err_vgosa</dd><dt><span>comment :</span></dt><dd>The geostrophic velocity anomalies are referenced to the [1993, 2012] period</dd><dt><span>coordinates :</span></dt><dd>longitude latitude</dd><dt><span>grid_mapping :</span></dt><dd>crs</dd><dt><span>long_name :</span></dt><dd>Geostrophic velocity anomalies: meridian component</dd><dt><span>standard_name :</span></dt><dd>surface_geostrophic_northward_sea_water_velocity_assuming_sea_level_for_geoid</dd></dl></div><div class='xr-var-data'><table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    &#10;                    <tr>
                        <th> Bytes </th>
                        <td> 183.88 GiB </td>
                        <td> 2.00 MiB </td>
                    </tr>
                    &#10;                    <tr>
                        <th> Shape </th>
                        <td> (11902, 1440, 2880) </td>
                        <td> (1, 512, 1024) </td>
                    </tr>
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> 107118 chunks in 2 graph layers </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> int32 numpy.ndarray </td>
                    </tr>
                </tbody>
            </table>
        </td>
        <td>
        <svg width="173" height="160" style="stroke:rgb(0,0,0);stroke-width:1" >
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="10" y1="14" x2="80" y2="84" />
  <line x1="10" y1="28" x2="80" y2="98" />
  <line x1="10" y1="39" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="10" y2="39" style="stroke-width:2" />
  <line x1="13" y1="3" x2="13" y2="43" />
  <line x1="17" y1="7" x2="17" y2="47" />
  <line x1="21" y1="11" x2="21" y2="50" />
  <line x1="24" y1="14" x2="24" y2="54" />
  <line x1="28" y1="18" x2="28" y2="58" />
  <line x1="32" y1="22" x2="32" y2="61" />
  <line x1="36" y1="26" x2="36" y2="65" />
  <line x1="39" y1="29" x2="39" y2="69" />
  <line x1="43" y1="33" x2="43" y2="73" />
  <line x1="47" y1="37" x2="47" y2="76" />
  <line x1="50" y1="40" x2="50" y2="80" />
  <line x1="54" y1="44" x2="54" y2="84" />
  <line x1="58" y1="48" x2="58" y2="87" />
  <line x1="62" y1="52" x2="62" y2="91" />
  <line x1="65" y1="55" x2="65" y2="95" />
  <line x1="69" y1="59" x2="69" y2="99" />
  <line x1="73" y1="63" x2="73" y2="102" />
  <line x1="76" y1="66" x2="76" y2="106" />
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 80.58823529411765,70.58823529411765 80.58823529411765,110.21240153264056 10.0,39.6241662385229" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="10" y1="0" x2="52" y2="0" style="stroke-width:2" />
  <line x1="13" y1="3" x2="56" y2="3" />
  <line x1="17" y1="7" x2="60" y2="7" />
  <line x1="21" y1="11" x2="63" y2="11" />
  <line x1="24" y1="14" x2="67" y2="14" />
  <line x1="28" y1="18" x2="71" y2="18" />
  <line x1="32" y1="22" x2="75" y2="22" />
  <line x1="36" y1="26" x2="78" y2="26" />
  <line x1="39" y1="29" x2="82" y2="29" />
  <line x1="43" y1="33" x2="86" y2="33" />
  <line x1="47" y1="37" x2="89" y2="37" />
  <line x1="50" y1="40" x2="93" y2="40" />
  <line x1="54" y1="44" x2="97" y2="44" />
  <line x1="58" y1="48" x2="101" y2="48" />
  <line x1="62" y1="52" x2="104" y2="52" />
  <line x1="65" y1="55" x2="108" y2="55" />
  <line x1="69" y1="59" x2="112" y2="59" />
  <line x1="73" y1="63" x2="115" y2="63" />
  <line x1="76" y1="66" x2="119" y2="66" />
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="10" y1="0" x2="80" y2="70" style="stroke-width:2" />
  <line x1="25" y1="0" x2="95" y2="70" />
  <line x1="40" y1="0" x2="111" y2="70" />
  <line x1="52" y1="0" x2="123" y2="70" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="10.0,0.0 52.775616481350575,0.0 123.36385177546822,70.58823529411765 80.58823529411765,70.58823529411765" style="fill:#8B4903A0;stroke-width:0"/>
&#10;  <!-- Horizontal lines -->
  <line x1="80" y1="70" x2="123" y2="70" style="stroke-width:2" />
  <line x1="80" y1="84" x2="123" y2="84" />
  <line x1="80" y1="98" x2="123" y2="98" />
  <line x1="80" y1="110" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Vertical lines -->
  <line x1="80" y1="70" x2="80" y2="110" style="stroke-width:2" />
  <line x1="95" y1="70" x2="95" y2="110" />
  <line x1="111" y1="70" x2="111" y2="110" />
  <line x1="123" y1="70" x2="123" y2="110" style="stroke-width:2" />
&#10;  <!-- Colored Rectangle -->
  <polygon points="80.58823529411765,70.58823529411765 123.36385177546822,70.58823529411765 123.36385177546822,110.21240153264056 80.58823529411765,110.21240153264056" style="fill:#ECB172A0;stroke-width:0"/>
&#10;  <!-- Text -->
  <text x="101.976044" y="130.212402" font-size="1.0rem" font-weight="100" text-anchor="middle" >2880</text>
  <text x="143.363852" y="90.400318" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,143.363852,90.400318)">1440</text>
  <text x="35.294118" y="94.918284" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(45,35.294118,94.918284)">11902</text>
</svg>
        </td>
    </tr>
</table></div></li></ul></div></li><li class='xr-section-item'><input id='section-9eab115f-7105-45d0-8d1a-587fc21491cc' class='xr-section-summary-in' type='checkbox'  ><label for='section-9eab115f-7105-45d0-8d1a-587fc21491cc' class='xr-section-summary' >Indexes: <span>(4)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-index-name'><div>latitude</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-d1538ce9-e4cf-4046-a843-dd19944b6030' class='xr-index-data-in' type='checkbox'/><label for='index-d1538ce9-e4cf-4046-a843-dd19944b6030' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([-89.9375, -89.8125, -89.6875, -89.5625, -89.4375, -89.3125, -89.1875,
       -89.0625, -88.9375, -88.8125,
       ...
        88.8125,  88.9375,  89.0625,  89.1875,  89.3125,  89.4375,  89.5625,
        89.6875,  89.8125,  89.9375],
      dtype=&#x27;float32&#x27;, name=&#x27;latitude&#x27;, length=1440))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>longitude</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-0a0256df-ad64-459d-8a18-b83092ae405b' class='xr-index-data-in' type='checkbox'/><label for='index-0a0256df-ad64-459d-8a18-b83092ae405b' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([-179.9375, -179.8125, -179.6875, -179.5625, -179.4375, -179.3125,
       -179.1875, -179.0625, -178.9375, -178.8125,
       ...
        178.8125,  178.9375,  179.0625,  179.1875,  179.3125,  179.4375,
        179.5625,  179.6875,  179.8125,  179.9375],
      dtype=&#x27;float32&#x27;, name=&#x27;longitude&#x27;, length=2880))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>time</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-fe8481d2-8d2b-459f-8139-467e9d34a925' class='xr-index-data-in' type='checkbox'/><label for='index-fe8481d2-8d2b-459f-8139-467e9d34a925' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([15706.0, 15707.0, 15708.0, 15709.0, 15710.0, 15711.0, 15712.0, 15713.0,
       15714.0, 15715.0,
       ...
       27598.0, 27599.0, 27600.0, 27601.0, 27602.0, 27603.0, 27604.0, 27605.0,
       27606.0, 27607.0],
      dtype=&#x27;float32&#x27;, name=&#x27;time&#x27;, length=11902))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>nv</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-c7ec9434-3e9b-4e9e-830a-0e1be6b0458c' class='xr-index-data-in' type='checkbox'/><label for='index-c7ec9434-3e9b-4e9e-830a-0e1be6b0458c' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([0, 1], dtype=&#x27;int32&#x27;, name=&#x27;nv&#x27;))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-f32e7d14-8893-4c61-a739-2dbf25daed51' class='xr-section-summary-in' type='checkbox'  ><label for='section-f32e7d14-8893-4c61-a739-2dbf25daed51' class='xr-section-summary' >Attributes: <span>(43)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'><dt><span>Conventions :</span></dt><dd>CF-1.6</dd><dt><span>Metadata_Conventions :</span></dt><dd>Unidata Dataset Discovery v1.0</dd><dt><span>cdm_data_type :</span></dt><dd>Grid</dd><dt><span>comment :</span></dt><dd>Sea Surface Height measured by Altimetry and derived variables</dd><dt><span>contact :</span></dt><dd>servicedesk.cmems@mercator-ocean.eu</dd><dt><span>coordinates :</span></dt><dd>lat_bnds lon_bnds</dd><dt><span>creator_email :</span></dt><dd>servicedesk.cmems@mercator-ocean.eu</dd><dt><span>creator_name :</span></dt><dd>CMEMS - Sea Level Thematic Assembly Center</dd><dt><span>creator_url :</span></dt><dd>http://marine.copernicus.eu</dd><dt><span>date_created :</span></dt><dd>2024-10-23T12:55:06Z</dd><dt><span>geospatial_lat_max :</span></dt><dd>89.9375</dd><dt><span>geospatial_lat_min :</span></dt><dd>-89.9375</dd><dt><span>geospatial_lat_resolution :</span></dt><dd>0.125</dd><dt><span>geospatial_lat_units :</span></dt><dd>degrees_north</dd><dt><span>geospatial_lon_max :</span></dt><dd>179.9375</dd><dt><span>geospatial_lon_min :</span></dt><dd>-179.9375</dd><dt><span>geospatial_lon_resolution :</span></dt><dd>0.125</dd><dt><span>geospatial_lon_units :</span></dt><dd>degrees_east</dd><dt><span>geospatial_vertical_max :</span></dt><dd>0.0</dd><dt><span>geospatial_vertical_min :</span></dt><dd>0.0</dd><dt><span>geospatial_vertical_positive :</span></dt><dd>down</dd><dt><span>geospatial_vertical_resolution :</span></dt><dd>point</dd><dt><span>geospatial_vertical_units :</span></dt><dd>m</dd><dt><span>history :</span></dt><dd>2024-10-23 12:55:06Z: Creation</dd><dt><span>institution :</span></dt><dd>CLS, CNES</dd><dt><span>keywords :</span></dt><dd>Oceans &gt; Ocean Topography &gt; Sea Surface Height</dd><dt><span>keywords_vocabulary :</span></dt><dd>NetCDF COARDS Climate and Forecast Standard Names</dd><dt><span>license :</span></dt><dd>http://marine.copernicus.eu/web/27-service-commitments-and-licence.php</dd><dt><span>platform :</span></dt><dd>Cryosat-2 New Orbit, SWOT Nadir science, Sentinel-3B, Altika Drifting Phase, Sentinel-6A, Haiyang-2B, Sentinel-3A, Jason-3 Interleaved</dd><dt><span>processing_level :</span></dt><dd>L4</dd><dt><span>product_version :</span></dt><dd>vNov2024</dd><dt><span>project :</span></dt><dd>COPERNICUS MARINE ENVIRONMENT MONITORING SERVICE (CMEMS)</dd><dt><span>references :</span></dt><dd>http://marine.copernicus.eu</dd><dt><span>software_version :</span></dt><dd>8.0_MIOST_DT2024_baseline</dd><dt><span>source :</span></dt><dd>Altimetry measurements</dd><dt><span>ssalto_duacs_comment :</span></dt><dd>The reference mission used for the altimeter inter-calibration processing is Topex/Poseidon between 1993-01-01 and 2002-04-23, Jason-1 between 2002-04-24 and 2008-10-18, OSTM/Jason-2 between 2008-10-19 and 2016-06-25, Jason-3 since 2016-06-25.</dd><dt><span>standard_name_vocabulary :</span></dt><dd>NetCDF Climate and Forecast (CF) Metadata Convention Standard Name Table v37</dd><dt><span>summary :</span></dt><dd>SSALTO/DUACS Delayed-Time Level-4 sea surface height and derived variables measured by multi-satellite altimetry observations over Global Ocean.</dd><dt><span>time_coverage_duration :</span></dt><dd>P1D</dd><dt><span>time_coverage_end :</span></dt><dd>2023-12-31T12:00:00Z</dd><dt><span>time_coverage_resolution :</span></dt><dd>P1D</dd><dt><span>time_coverage_start :</span></dt><dd>2023-12-30T12:00:00Z</dd><dt><span>title :</span></dt><dd>DT merged all satellites Global Ocean Gridded SSALTO/DUACS Sea Surface Height L4 product and derived variables</dd></dl></div></li></ul></div></div>

This example is a virtualized mosaic of NetCDF in multidim VRT.

``` python
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

### A grib example

What a joy to simply be able to use GDAL for what it is good at without
intermediate layers.

``` python
from gdx import GDALBackendEntrypoint
backend = GDALBackendEntrypoint()
backend.open_dataset("/vsicurl/https://noaa-nbm-grib2-pds.s3.amazonaws.com/blend.20251031/16/core/blend.t16z.core.f260.co.grib2", multidim = False, chunks = None)
```

    <xarray.Dataset> Size: 989MB
    Dimensions:                                                                           (
                                                                                           y: 1597,
                                                                                           x: 2345)
    Coordinates:
      * x                                                                                 (x) float64 19kB ...
      * y                                                                                 (y) float64 13kB ...
      * crs                                                                               int64 8B ...
    Data variables: (12/33)
        APTMP:2 m above ground:260 hour fcst                                              (y, x) float64 30MB ...
        CAPE:surface:260 hour fcst                                                        (y, x) float64 30MB ...
        CWASP:surface:260 hour fcst                                                       (y, x) float64 30MB ...
        DPT:2 m above ground:260 hour fcst                                                (y, x) float64 30MB ...
        DSWRF:surface:260 hour fcst                                                       (y, x) float64 30MB ...
        FICEAC:surface:254-260 hour acc fcst                                              (y, x) float64 30MB ...
        ...                                                                                ...
        WDIR:80 m above ground:260 hour fcst                                              (y, x) float64 30MB ...
        WDIR:10 m above ground:260 hour fcst                                              (y, x) float64 30MB ...
        GUST:10 m above ground:260 hour fcst                                              (y, x) float64 30MB ...
        WIND:30 m above ground:260 hour fcst                                              (y, x) float64 30MB ...
        WIND:80 m above ground:260 hour fcst                                              (y, x) float64 30MB ...
        WIND:10 m above ground:260 hour fcst                                              (y, x) float64 30MB ...
    Indexes:
      ┌ x        RasterIndex
      └ y
        crs      CRSIndex (crs=PROJCS["unnamed",GEOGCS["Coordinate System imported from GRIB file" ...)

There’s a lot more to do, scaling works but I turned that off to test
for now. .

Template a list of netcdf files and mosaic them to VRT, then open with
this xarray backend. (Note this requires GDAL\>=3.12.0 ).

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
