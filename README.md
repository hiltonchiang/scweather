---
title: [nc2csv](https://github.com/hiltonchiang/scweather)
---

nc2csv is a Python program to convert Netcdf file (extension .nc) into a csv file. The key Python library used is named netCDF4 (version 4).

Usage:
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

