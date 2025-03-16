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

