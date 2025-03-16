---
title: nc2csv
---

## nc2csv

[nc2csv](https://github.com/hiltonchiang/scweather) is a Python program to convert Netcdf file (extension .nc) into a csv file. The key Python library used is named xarray which uses netCDF4 (version 4) and pandas modules.

## Usage:
```bash
Usage: python nc2csv.py fname.nc

```
It takes longer to build csv file if input file is very large and generated csv files size are huge.

## Python modules 

The Python libraries used:
```python
import sys
import os
import xarray as xr
```

You can use pip to install all of those Python modules.
## Source Code

The source code of nc2csv.py can be found in this repo, or you can download directly; see [here](#Download).

An old version source code is shown here for reference only, theo content may not be the latest one.

```python
# -*- coding: utf-8 -*-

############# load packages ###############
import sys
import os
import xarray as xr

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'


def usage():
   print(bcolors.HEADER+"Usage: python nc2csv.py fname.nc"+bcolors.ENDC)


if len(sys.argv) != 2:
    usage()
    quit()

f = sys.argv[1]
print("fname ",f)
############# read netCDF file ###############
fn = os.path.basename(f)
if (fn.split('.')[0] != fn.split('.')[-1]):
    fn = fn.replace('.'+fn.split('.')[-1],'')
print("base file name : ", fn)
print("Now reading file : " + bcolors.WARNING + os.path.basename(f) + bcolors.ENDC)
print("open dataset")

ds = xr.open_dataset(f, engine='netcdf4')
### print Infos
print("dataset Info:")
print(bcolors.WARNING+"ds.dims:"+bcolors.ENDC,ds.dims)
print(bcolors.WARNING+"ds.sizes:"+bcolors.ENDC,ds.sizes)
print(bcolors.WARNING+"ds.dtypes:"+bcolors.ENDC,ds.dtypes)
print(bcolors.WARNING+"ds.data_vars:"+bcolors.ENDC,ds.data_vars)
print(bcolors.WARNING+"ds.data_vars keys:"+bcolors.ENDC,list(ds.data_vars.keys()))
print(bcolors.WARNING+"ds.coords:"+bcolors.ENDC,ds.coords)
print(bcolors.WARNING+"ds.coords keys:"+bcolors.ENDC,list(ds.coords.keys()))
print(bcolors.WARNING+"ds.attrs:"+bcolors.ENDC,ds.attrs)
print(bcolors.WARNING+"ds.encoding:"+bcolors.ENDC,ds.encoding)
print(bcolors.WARNING+"ds.indexes:"+bcolors.ENDC,ds.indexes)
print(bcolors.WARNING+"ds.chunks:"+bcolors.ENDC,ds.chunks)
print(bcolors.WARNING+"ds.chunksizes:"+bcolors.ENDC,ds.chunksizes)
print(bcolors.WARNING+"ds.nbytes:"+bcolors.ENDC,ds.nbytes)

###
dsVars=list(ds.data_vars.keys())

for v in dsVars:
    print(bcolors.WARNING+"ds.data_vars ["+ v + "] DataArray:" + bcolors.ENDC)
    df = ds.data_vars[v].to_dataframe().dropna(how='any', axis=0).reset_index()
    print("dataFrame:")
    print(df)
    n = fn+'-' + v + '.csv'
    print(bcolors.WARNING+"Now generating csv file : " + n + bcolors.ENDC)
    df.to_csv(n, index=True)

```


## Output:

The original netCDF (.nc) file may contain several variables. The number of generated csv files depends on how many variables found in the original netCDF file.

For example, the console output while running nc2csv
```bash 

$python nc2csv.py test.nc

fname  test.nc
base file name :  test
Now reading file : test.nc
...
...
ds.data_vars: Data variables:
    mean_wspeed  (time, latitude, longitude) float32 43MB ...
    mean_cur     (time, k, latitude, longitude) float32 724MB ...
    eta          (time, latitude, longitude) float32 43MB ...
    salt         (time, k, latitude, longitude) float32 724MB ...
    temp         (time, k, latitude, longitude) float32 724MB ...
    wspeed_u     (time, latitude, longitude) float32 43MB ...
    wspeed_v     (time, latitude, longitude) float32 43MB ...
    u            (time, k, latitude, longitude) float32 724MB ...
    v            (time, k, latitude, longitude) float32 724MB ...
ds.data_vars keys: ['mean_wspeed', 'mean_cur', 'eta', 'salt', 'temp', 'wspeed_u', 'wspeed_v', 'u', 'v']

```
The test.nc contains nine Data variables, so totally it will generate nine csv files with names like :

    test-mean_wspeed.csv
    test-mean_cur.csv
    test-eta.csv
    test-salt.csv
    test-temp.csv
    test-wspeed_u.csv
    test-wspeed_v.csv
    test-u.csv
    test-v.csv

## Download

A [scweather-main.zip](https://github.com/hiltonchiang/scweather/archive/refs/heads/main.zip) is available in github for downloading.

