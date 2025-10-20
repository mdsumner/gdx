
<!-- README.md is generated from README.Rmd. Please edit that file -->

# gdx

<!-- badges: start -->

<!-- badges: end -->

The goal of gdx is to integrate GDAL with xarray, especially for the
multidimensional API which is still relatively underutilized.

Here’s a basic example, in time this could be registred as an xarray
backend.

``` python
from gdx import GDALBackendEntrypoint
backend = GDALBackendEntrypoint()
dsn =  "/vsicurl/https://projects.pawsey.org.au/idea-sealevel-glo-phy-l4-nrt-008-046/data.marine.copernicus.eu/SEALEVEL_GLO_PHY_L4_NRT_008_046/cmems_obs-sl_glo_phy-ssh_nrt_allsat-l4-duacs-0.125deg_P1D_202506/2025/08/nrt_global_allsat_phy_l4_20250825_20250825.nc"
ds = backend.open_dataset(f'vrt://{dsn}?sd_name=vgos')
ds.band_1.isel(x = 0)
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
</style><pre class='xr-text-repr-fallback'>&lt;xarray.DataArray &#x27;band_1&#x27; (y: 1440)&gt; Size: 6kB
array([-2147483647, -2147483647, -2147483647, ..., -2147483647,
       -2147483647, -2147483647], shape=(1440,), dtype=int32)
Coordinates:
    x        float64 8B -180.0
  * y        (y) float64 12kB 90.0 89.88 89.75 89.62 ... -89.62 -89.75 -89.88
Attributes:
    nodata:   -2147483647.0
    scale:    0.0001
    offset:   0.0</pre><div class='xr-wrap' style='display:none'><div class='xr-header'><div class='xr-obj-type'>xarray.DataArray</div><div class='xr-array-name'>'band_1'</div><ul class='xr-dim-list'><li><span class='xr-has-index'>y</span>: 1440</li></ul></div><ul class='xr-sections'><li class='xr-section-item'><div class='xr-array-wrap'><input id='section-58d2cef0-a662-4b63-a603-25e725f80a8f' class='xr-array-in' type='checkbox' checked><label for='section-58d2cef0-a662-4b63-a603-25e725f80a8f' title='Show/hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-array-preview xr-preview'><span>-2147483647 -2147483647 -2147483647 ... -2147483647 -2147483647</span></div><div class='xr-array-data'><pre>array([-2147483647, -2147483647, -2147483647, ..., -2147483647,
       -2147483647, -2147483647], shape=(1440,), dtype=int32)</pre></div></div></li><li class='xr-section-item'><input id='section-126a8da7-1e0f-4682-b325-b247f0feb170' class='xr-section-summary-in' type='checkbox'  checked><label for='section-126a8da7-1e0f-4682-b325-b247f0feb170' class='xr-section-summary' >Coordinates: <span>(2)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>x</span></div><div class='xr-var-dims'>()</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>-180.0</div><input id='attrs-aecb3dcc-72a2-4aa6-854f-d5f7eff8026d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-aecb3dcc-72a2-4aa6-854f-d5f7eff8026d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d6738ff0-6f92-4a73-bb47-fa42f855a487' class='xr-var-data-in' type='checkbox'><label for='data-d6738ff0-6f92-4a73-bb47-fa42f855a487' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array(-180.)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>y</span></div><div class='xr-var-dims'>(y)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>90.0 89.88 89.75 ... -89.75 -89.88</div><input id='attrs-70ff3797-1b33-4002-a9bc-c4bbe0d76326' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-70ff3797-1b33-4002-a9bc-c4bbe0d76326' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-bd47357a-3229-4771-9a1f-177dc59615cf' class='xr-var-data-in' type='checkbox'><label for='data-bd47357a-3229-4771-9a1f-177dc59615cf' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([ 90.   ,  89.875,  89.75 , ..., -89.625, -89.75 , -89.875],
      shape=(1440,))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-5aed8f11-d3cf-453a-8584-d52a4c19d12e' class='xr-section-summary-in' type='checkbox'  ><label for='section-5aed8f11-d3cf-453a-8584-d52a4c19d12e' class='xr-section-summary' >Indexes: <span>(1)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-index-name'><div>y</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-2c4ca6a3-dc78-41bb-9bd6-56186e612371' class='xr-index-data-in' type='checkbox'/><label for='index-2c4ca6a3-dc78-41bb-9bd6-56186e612371' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([   90.0,  89.875,   89.75,  89.625,    89.5,  89.375,   89.25,  89.125,
          89.0,  88.875,
       ...
        -88.75, -88.875,   -89.0, -89.125,  -89.25, -89.375,   -89.5, -89.625,
        -89.75, -89.875],
      dtype=&#x27;float64&#x27;, name=&#x27;y&#x27;, length=1440))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-dde7c950-be56-4273-9aee-8add0ed24965' class='xr-section-summary-in' type='checkbox'  checked><label for='section-dde7c950-be56-4273-9aee-8add0ed24965' class='xr-section-summary' >Attributes: <span>(3)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'><dt><span>nodata :</span></dt><dd>-2147483647.0</dd><dt><span>scale :</span></dt><dd>0.0001</dd><dt><span>offset :</span></dt><dd>0.0</dd></dl></div></li></ul></div></div>

``` python
## the raw values for now
ds.band_1.sel(x = 100, y = -50).values
#> array(441, dtype=int32)

ds = backend.open_dataset(dsn, multidim = True) 
ds.sla.isel(longitude = 0, latitude = 1000).values
#> array([2404], dtype=int32)

big_virtual_mdim = "/vsicurl/https://gist.githubusercontent.com/mdsumner/18c5d302d00b9a456bb73d30ac758764/raw/f26e1b2e202f759d6aace4d7deb3e04ea3c85f15/mdim.vrt"

backend.open_dataset(big_virtual_mdim, multidim = True)
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
</style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt; Size: 3TB
Dimensions:   (Time: 5479, st_ocean: 51, yt_ocean: 1500, xt_ocean: 3600)
Coordinates:
  * Time      (Time) float64 44kB 1.132e+04 1.132e+04 ... 1.68e+04 1.68e+04
  * st_ocean  (st_ocean) float64 408B 2.5 7.5 12.5 ... 3.603e+03 4.509e+03
  * yt_ocean  (yt_ocean) float64 12kB -74.95 -74.85 -74.75 ... 74.75 74.85 74.95
  * xt_ocean  (xt_ocean) float64 29kB 0.05 0.15 0.25 0.35 ... 359.8 359.9 360.0
Data variables:
    temp      (Time, st_ocean, yt_ocean, xt_ocean) int16 3TB ...</pre><div class='xr-wrap' style='display:none'><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-b915a228-0ed9-4019-a1e4-9fcad30be0b2' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-b915a228-0ed9-4019-a1e4-9fcad30be0b2' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span class='xr-has-index'>Time</span>: 5479</li><li><span class='xr-has-index'>st_ocean</span>: 51</li><li><span class='xr-has-index'>yt_ocean</span>: 1500</li><li><span class='xr-has-index'>xt_ocean</span>: 3600</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-0b41f81b-479b-4fa8-8096-372b58fef177' class='xr-section-summary-in' type='checkbox'  checked><label for='section-0b41f81b-479b-4fa8-8096-372b58fef177' class='xr-section-summary' >Coordinates: <span>(4)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>Time</span></div><div class='xr-var-dims'>(Time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.132e+04 1.132e+04 ... 1.68e+04</div><input id='attrs-901dda52-68dc-4e74-90a4-e07781b66450' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-901dda52-68dc-4e74-90a4-e07781b66450' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-550d728a-fcc9-4dba-b5a0-e5910f8cd5dc' class='xr-var-data-in' type='checkbox'><label for='data-550d728a-fcc9-4dba-b5a0-e5910f8cd5dc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>bounds :</span></dt><dd>Time_bnds</dd><dt><span>calendar :</span></dt><dd>GREGORIAN</dd><dt><span>calendar_type :</span></dt><dd>GREGORIAN</dd><dt><span>cartesian_axis :</span></dt><dd>T</dd><dt><span>cell_methods :</span></dt><dd>Time: mean</dd><dt><span>long_name :</span></dt><dd>Time</dd></dl></div><div class='xr-var-data'><pre>array([11323.5, 11324.5, 11325.5, ..., 16799.5, 16800.5, 16801.5],
      shape=(5479,))</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>st_ocean</span></div><div class='xr-var-dims'>(st_ocean)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>2.5 7.5 ... 3.603e+03 4.509e+03</div><input id='attrs-abc87566-d28e-4378-b59d-ef82ebf6139a' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-abc87566-d28e-4378-b59d-ef82ebf6139a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-0e95096e-6464-4936-a770-7b0f63f236b1' class='xr-var-data-in' type='checkbox'><label for='data-0e95096e-6464-4936-a770-7b0f63f236b1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>cartesian_axis :</span></dt><dd>Z</dd><dt><span>edges :</span></dt><dd>st_edges_ocean</dd><dt><span>long_name :</span></dt><dd>tcell zstar depth</dd><dt><span>positive :</span></dt><dd>down</dd></dl></div><div class='xr-var-data'><pre>array([2.500000e+00, 7.500000e+00, 1.250000e+01, 1.751539e+01, 2.266702e+01,
       2.816938e+01, 3.421801e+01, 4.095498e+01, 4.845498e+01, 5.671801e+01,
       6.566938e+01, 7.516702e+01, 8.501539e+01, 9.500000e+01, 1.050000e+02,
       1.150000e+02, 1.250000e+02, 1.350000e+02, 1.450000e+02, 1.550000e+02,
       1.650000e+02, 1.750000e+02, 1.850000e+02, 1.950000e+02, 2.051899e+02,
       2.170545e+02, 2.331943e+02, 2.558842e+02, 2.866090e+02, 3.258842e+02,
       3.731943e+02, 4.270545e+02, 4.851899e+02, 5.455111e+02, 6.104156e+02,
       6.859268e+02, 7.759268e+02, 8.804156e+02, 9.955111e+02, 1.115313e+03,
       1.238354e+03, 1.368157e+03, 1.507734e+03, 1.658157e+03, 1.818354e+03,
       1.985313e+03, 2.165180e+03, 2.431101e+03, 2.894842e+03, 3.603101e+03,
       4.509180e+03])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>yt_ocean</span></div><div class='xr-var-dims'>(yt_ocean)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>-74.95 -74.85 ... 74.85 74.95</div><input id='attrs-9dd73fef-8881-4416-b7ed-05543f3df059' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-9dd73fef-8881-4416-b7ed-05543f3df059' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-cb2318db-aeaf-45ad-b34b-3569086f2613' class='xr-var-data-in' type='checkbox'><label for='data-cb2318db-aeaf-45ad-b34b-3569086f2613' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>cartesian_axis :</span></dt><dd>Y</dd><dt><span>domain_decomposition :</span></dt><dd>(1, 1500, 1, 150)</dd><dt><span>long_name :</span></dt><dd>tcell latitude</dd></dl></div><div class='xr-var-data'><pre>array([-74.949997, -74.849997, -74.749997, ...,  74.75    ,  74.85    ,
        74.95    ], shape=(1500,))</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>xt_ocean</span></div><div class='xr-var-dims'>(xt_ocean)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.05 0.15 0.25 ... 359.9 360.0</div><input id='attrs-a4ec1296-f5bf-4e10-9463-0c55e0587f4b' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-a4ec1296-f5bf-4e10-9463-0c55e0587f4b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8a44bd60-a2c1-4a71-8513-51a40d1953eb' class='xr-var-data-in' type='checkbox'><label for='data-8a44bd60-a2c1-4a71-8513-51a40d1953eb' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>cartesian_axis :</span></dt><dd>X</dd><dt><span>domain_decomposition :</span></dt><dd>(1, 3600, 1, 1800)</dd><dt><span>long_name :</span></dt><dd>tcell longitude</dd></dl></div><div class='xr-var-data'><pre>array([5.0000e-02, 1.5000e-01, 2.5000e-01, ..., 3.5975e+02, 3.5985e+02,
       3.5995e+02], shape=(3600,))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-0c55fd5a-6d48-49d3-8f9c-912688264040' class='xr-section-summary-in' type='checkbox'  checked><label for='section-0c55fd5a-6d48-49d3-8f9c-912688264040' class='xr-section-summary' >Data variables: <span>(1)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>temp</span></div><div class='xr-var-dims'>(Time, st_ocean, yt_ocean, xt_ocean)</div><div class='xr-var-dtype'>int16</div><div class='xr-var-preview xr-preview'>...</div><input id='attrs-0c31982f-0710-41f0-a4d8-d12c02211e23' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-0c31982f-0710-41f0-a4d8-d12c02211e23' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-72eb9379-f041-4dea-b168-68f2b295f165' class='xr-var-data-in' type='checkbox'><label for='data-72eb9379-f041-4dea-b168-68f2b295f165' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>cell_methods :</span></dt><dd>time: mean Time: mean</dd><dt><span>coordinates :</span></dt><dd>geolon_t geolat_t</dd><dt><span>long_name :</span></dt><dd>Potential temperature</dd><dt><span>packing :</span></dt><dd>4</dd><dt><span>standard_name :</span></dt><dd>sea_water_potential_temperature</dd><dt><span>time_avg_info :</span></dt><dd>average_T1,average_T2,average_DT</dd><dt><span>valid_range :</span></dt><dd>(-32767, 32767)</dd></dl></div><div class='xr-var-data'><pre>[1508916600000 values with dtype=int16]</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-29d3bc4f-9bb3-44a9-abb8-d783b2673f0f' class='xr-section-summary-in' type='checkbox'  ><label for='section-29d3bc4f-9bb3-44a9-abb8-d783b2673f0f' class='xr-section-summary' >Indexes: <span>(4)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-index-name'><div>Time</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-23d3e448-8185-4622-8deb-f107c0231841' class='xr-index-data-in' type='checkbox'/><label for='index-23d3e448-8185-4622-8deb-f107c0231841' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([11323.5, 11324.5, 11325.5, 11326.5, 11327.5, 11328.5, 11329.5, 11330.5,
       11331.5, 11332.5,
       ...
       16792.5, 16793.5, 16794.5, 16795.5, 16796.5, 16797.5, 16798.5, 16799.5,
       16800.5, 16801.5],
      dtype=&#x27;float64&#x27;, name=&#x27;Time&#x27;, length=5479))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>st_ocean</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-41dcc812-340a-4221-a229-b8216e690ee9' class='xr-index-data-in' type='checkbox'/><label for='index-41dcc812-340a-4221-a229-b8216e690ee9' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([               2.5,                7.5,               12.5,
       17.515390396118164, 22.667020797729492,  28.16938018798828,
         34.2180061340332,  40.95497512817383,  48.45497512817383,
         56.7180061340332,  65.66938018798828,  75.16702270507812,
        85.01538848876953,               95.0,              105.0,
                    115.0,              125.0,              135.0,
                    145.0,              155.0,              165.0,
                    175.0,              185.0,              195.0,
        205.1898956298828,  217.0544891357422, 233.19432067871094,
        255.8842315673828,  286.6089782714844, 325.88421630859375,
           373.1943359375,  427.0544738769531,  485.1899108886719,
        545.5111083984375,  610.4156494140625,     685.9267578125,
           775.9267578125,  880.4156494140625,  995.5111083984375,
       1115.3133544921875, 1238.3538818359375,  1368.157470703125,
         1507.73388671875,  1658.157470703125, 1818.3538818359375,
       1985.3133544921875,   2165.18017578125,   2431.10107421875,
           2894.841796875,   3603.10107421875,   4509.18017578125],
      dtype=&#x27;float64&#x27;, name=&#x27;st_ocean&#x27;))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>yt_ocean</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-c23bed0a-48a6-48b2-879a-d2218bc4320f' class='xr-index-data-in' type='checkbox'/><label for='index-c23bed0a-48a6-48b2-879a-d2218bc4320f' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([-74.94999694824219, -74.84999695015112, -74.74999695206007,
       -74.64999695396901, -74.54999695587794, -74.44999695778688,
       -74.34999695969583, -74.24999696160477,  -74.1499969635137,
       -74.04999696542264,
       ...
        74.05000020743807,  74.15000020552915,   74.2500002036202,
        74.35000020171125,  74.45000019980233,  74.55000019789338,
        74.65000019598443,  74.75000019407551,  74.85000019216656,
        74.95000019025761],
      dtype=&#x27;float64&#x27;, name=&#x27;yt_ocean&#x27;, length=1500))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>xt_ocean</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-a9cbe6c0-5d6a-41cc-b896-438ce386e92c' class='xr-index-data-in' type='checkbox'/><label for='index-a9cbe6c0-5d6a-41cc-b896-438ce386e92c' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([0.05000000074505806, 0.15000000444505387,  0.2500000081450497,
        0.3500000118450455,  0.4500000155450413,  0.5500000192450372,
        0.6500000229450329,  0.7500000266450287,  0.8500000303450246,
        0.9500000340450204,
       ...
        359.05001328373004,  359.15001328743006,     359.25001329113,
        359.35001329483003,     359.45001329853,     359.55001330223,
        359.65001330593003,     359.75001330963,     359.85001331333,
        359.95001331702997],
      dtype=&#x27;float64&#x27;, name=&#x27;xt_ocean&#x27;, length=3600))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-67c89502-853b-42f8-8d88-a41d3c81c70c' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-67c89502-853b-42f8-8d88-a41d3c81c70c' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>

``` python


#ds.sel(xt_ocean = slice(140, 150))
# import xarray
# xarray.open_dataset(dsn, engine = "gdal")
```

Lots to do, make sure read is really lazy, convert from mdim mosaic to
xarray, …

## Code of Conduct

Please note that the gdx project is released with a [Contributor Code of
Conduct](https://contributor-covenant.org/version/2/1/CODE_OF_CONDUCT.html).
By contributing to this project, you agree to abide by its terms.
