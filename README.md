---
title: nc2csv
---

nc2csv is a Python program to convert Netcdf file (extension .nc) into a csv file. The key Python library used is named netCDF4 (version 4).

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

The source code can be found on nc2csv.py

```python
import numpy as np
from netCDF4 import Dataset
import sys
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

def usage():
   print(bcolors.HEADER+"Usage: netcdf2cvs fname.nc"+bcolors.ENDC)

if len(sys.argv) <= 1:
   print(bcolors.FAIL+"You need to input a file name!"+bcolors.ENDC)
   usage()
   quit()

if len(sys.argv) != 2:
   print(bcolors.FAIL+"You only need to input a file name!"+bcolors.ENDC)
   usage()
   quit()

############# read netCDF file ###############
f=sys.argv[1]
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
  print("dimensios : ", dms)
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
      print(idx)
      if (math.isnan(x) == False):
        for i in range(len(dms)):
          BD[AA[i]].append(fn_nc.variables[AA[i]][idx[i]].data.item())
        CA.append(x)
    ### to save time for test only
    ### comment out following three lines for
    ### production.
    ### !!! !!!
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
# Create a pandas DataFrame
df = pd.DataFrame.from_dict(D, orient='index', dtype='object')
df = df.transpose()
# Save to CSV
csvfn=fn + ".csv"
df.to_csv(csvfn, index=False)
print("csv file saved : " + bcolors.WARNING + csvfn + bcolors.ENDC)
# Close the file
fn_nc.close()


```
