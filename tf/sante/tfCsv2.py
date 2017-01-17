#!/usr/bin/python

from __future__ import division

import sys
import pandas as pd
import os, glob
import random as rd

def main(argv):
   srcDir = "."
   if len(argv) != 0:
      srcDir = argv[0]

   # Specify datasets saved location/path
   os.chdir(srcDir)

   df = pd.read_csv('data.csv')

   sz = len(df.index)
   tstsz = int(round(sz * 0.2))
   trnsz = sz - tstsz
   dim = 40

   rows = rd.sample(df.index, tstsz)
   df_20 = df.ix[rows]
   df_20.columns.values[0] = tstsz
   df_20.columns.values[1] = dim
   df_20.to_csv('iris_test.csv', index=False)

   df_other = df.drop(rows)
   df_other.columns.values[0] = trnsz
   df_other.columns.values[1] = dim
   df_other.to_csv('iris_training.csv', index=False)

if __name__ == "__main__":
   main(sys.argv[1:])

# Ref:
## http://pandas.pydata.org/pandas-docs/stable/genindex.html
## http://stackoverflow.com/questions/33642673/convert-csv-to-json-in-specific-format-using-python
## http://www.nephridium-labs.com/blog/converting-between-json-and-csv-using-pandas/
## https://github.com/nephridium/csv2json/blob/master/csv2json.py

# $ pip install -U pandas --upgrade --proxy=http://id:pw@proxy.global.net:8080
