---
title: nc2csv
---

## nc2csv

[nc2csv](https://github.com/hiltonchiang/scweather) is a Python program to convert Netcdf file (extension .nc) into a csv file. The key Python library used is named netCDF4 (version 4).

## Usage:
```bash
Usage: nc2csv fname.nc [-d|--develop]

```
It takes longer to build csv file if input file is very large; for development purpose, add `-d` or `--develop` at the end of the command line to build partial parts of the entire file.

## Python modules 

The Python libraries used:
```python
import numpy as np
from netCDF4 import Dataset
import sys
import os
import math
import pandas as pd
import inspect
```

You can use pip to install all of those Python modules.
## Source Code

The source code of nc2csv.py can be found in this repo, or you can download directly; see [here](#Download)

An old version source code is show here for reference only, may not be the latest one.

```python
# -*- coding: utf-8 -*-

############# load packages ###############
import numpy as np
from netCDF4 import Dataset
import sys
import getopt
import os
import math
import pandas as pd
import inspect

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

f = None
develop = False

def usage():
   print(bcolors.HEADER+"Usage: nc2csv fname.nc [-d|--develop]"+bcolors.ENDC)

argv = sys.argv[1:]

try:
  opts, args = getopt.getopt(argv, "d:",["develop"])
except:
  usage()
  quit()

for arg in args:
  if arg in ['-d', '--develop']:
    develop = True
  else:
    f = arg

print("fname ",f)
print("develop ", develop)
############# read netCDF file ###############
fn = os.path.basename(f)
if (fn.split('.')[0] != fn.split('.')[-1]):
    fn = fn.replace('.'+fn.split('.')[-1],'')
print("base file name : ", fn)
print("Now reading file : " + bcolors.WARNING + os.path.basename(f) + bcolors.ENDC)
fn_nc=Dataset(f)

############ file info and variables ##############
print('The ' +bcolors.WARNING + os.path.basename(f) + bcolors.ENDC + ' has groups : ')
print("\t",fn_nc.groups)
print('The ' +bcolors.WARNING + os.path.basename(f) + bcolors.ENDC + ' has dimensions : ')
print("\t",fn_nc.dimensions)
print('The ' +bcolors.WARNING + os.path.basename(f) + bcolors.ENDC + ' has following variables  : ')
vars_nc = list(fn_nc.variables.keys())
print("\t",vars_nc)
D = {}
T = {}
for v in vars_nc:
  shp = fn_nc.variables[v].shape
  dms = fn_nc.variables[v].dimensions
  print("varialbe " + bcolors.WARNING + v + bcolors.ENDC)
  print("shape : ", shp)
  print("max shpe : ", max(shp))
  #print("shape type : ", type(shp))
  #print("shape tuple length : ", len(shp))
  print("dimensios : ", dms)
  #print("dimensions type : ", type(dms))
  #print("dimensions tuple length : ", len(dms))
  print("Attributes:")
  for i in inspect.getmembers(fn_nc.variables[v]):
    if not i[0].startswith('_'):
      if not inspect.ismethod(i[1]):
        print("\t",i)

  if (len(shp) == 1): ##1D variable
    T[v] = fn_nc.variables[v][:]
    D = T | D
  else: ## geo-2d
    AA=[]
    BD={}
    CA=[]
    for i in range(len(dms)):
      for u in vars_nc:
        dd = fn_nc.variables[u].dimensions
        if len(dd) == 1 and dms[i] == dd[0]:
          AA.append(u)
          BD[u]=[]

    cnt = 0
    print(AA)
    print(BD)
    ### find NaN value and build new Arraya wiht elements indexed by
    ### idx
    for idx, x in np.ndenumerate(fn_nc.variables[v]):
      if (math.isnan(x) == False):
        for i in range(len(dms)):
          BD[AA[i]].append(fn_nc.variables[AA[i]][idx[i]].data.item())
        CA.append(x)
    ### to save time for test only
    ### comment out following three lines for
    ### production.
    ### !!! !!!
        if develop == True:
          cnt = cnt + 1
          if cnt == 10000:
            break
    for i in range(len(AA)):
      n = v + '.' + AA[i]
      D[n] = BD[AA[i]]
    D[v] = CA[:]

##############

# Extract data
variable_name = vars_nc[3]  # Replace with the actual variable name
print("converting " + bcolors.WARNING + fn +bcolors.ENDC)
# data = fn_nc.variables[variable_name][:]
# Create a pandas DataFrame
#print('D = ...')
#print(D)
df = pd.DataFrame.from_dict(D, orient='index', dtype='object')
df = df.transpose()
# Save to CSV
csvfn=fn + ".csv"
df.to_csv(csvfn, index=False)
print("csv file saved : " + bcolors.WARNING + csvfn + bcolors.ENDC)
# Close the file
fn_nc.close()


```


## Output:

The converted csv file is named by replacing original extension '.nc' with '.csv'. The keys of the converted csv file are based on original NetCDF variables names. For 1D type variables like 'time', 'level', 'latitude' or 'longitude', those names are not changed. For Geo2D type variables, extra columns with keys named by suffixing names found in NetCDF varialbe's dimensions. For example, variable 'A' with dimensions ('B', 'C', 'D') will generate 3 columnes with keys 'A.B', 'A.C' and 'A.D'
plus A's own data column.

example
```vim
zc,time,latitude,longitude,mean_wspeed.time,mean_wspeed.latitude,mean_wspeed.longitude,mean_wspeed
 -145.0,7548.0,-28.696022,142.168788,7548.0,-28.696022,153.598788,7.988132,7548.0,-145.0
```

Variable mean_wspeed has dimensions('time', 'latidute', 'longitude'), so there are 3 + 1 columns with keys ('mean_wspeed.time', 'mean_wspeed.latitude', 'mean_wspeed.longitude', 'mean_wspeed') are generated.

## Download

A [scweather-main.zip](https://github.com/hiltonchiang/scweather/archive/refs/heads/main.zip) is available in github for downloading.

