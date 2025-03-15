---
title: nc2csv
---
<br>
[nc2csv](https://github.com/hiltonchiang/scweather) is a Python program to convert Netcdf file (extension .nc) into a csv file. The key Python library used is named netCDF4 (version 4).

## Usage:
```bash
Usage: nc2csv fname.nc [-d|--develop]

```
It takes longer to build csv file if input file is very large; for development purpose, add `-d` or `--develop` at the end of the command line to build partial parts of the entire file.

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

