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
## fn=r'/home/hiltonchiang/Downloads/rhum.2003.nc'
##fn=r'/home/hiltonchiang/opt/webDesign/apps/netcdf/python-netCDF/rhum4.2003.nc'
# f=sys.argv[1]
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

