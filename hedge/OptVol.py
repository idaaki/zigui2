#!/usr/bin/python3
# coding: utf-8

from __future__ import print_function

import codecs
import csv
import datetime
import io
import json
import numpy as np
import os
from os import listdir
import re
import requests
import shutil
from time import sleep
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
import sys
from bs4 import BeautifulSoup


FUTURE = "FUT"
OPT_PUT  = "PUT"
OPT_CALL = "CAL"

BASE_URL = "https://www.jpx.co.jp"
VOLUME_URI = "/markets/derivatives/participant-volume/index.html"

DATA_DIR = "./voldata/"


class Trader:
   def __init__(self, cd, ja, en):
      self.cd = cd
      self.ja = ja
      self.en = en

   def getCd(self):
      return self.cd

   def getJa(self):
      return self.ja

   def getEn(self):
      return self.en


class Target:
   def __init__(self, jpxCd, instrument, vol):
      self.jpxCd = jpxCd
      self.instrument = instrument
      self.vol = vol

   def getJpxCd(self):
      return self.jpxCd

   def getInstrument(self):
      return self.instrument

   def getVol(self):
      return self.vol


class Instrument:
   def __init__(self, type, target, end, kp):
      self.type   = type
      self.target = target
      self.end    = end
      self.kp     = kp

   def getType(self):
      return self.type

   def getTarget(self):
      return self.target

   def getEnd(self):
      return self.end

   def getKp(self):
      return self.kp


def default_method(item):
    if isinstance(item, object) and hasattr(item, '__dict__'):
        return item.__dict__
    else:
        raise TypeError


class TargetEncoder(json.JSONEncoder):
   def default(self, obj):
      if isinstance(obj, Target) and hasattr(obj, '__dict__'):
         return obj.__dict__
      return super(TargetEncoder, self).default(obj) # 他の型はdefaultのエンコード方式を使用


def loadJsonData(path):
   jsonData = {}

   if os.path.exists(path):
      # Relative Path
      with open(path, 'r', encoding='utf-8') as infile:
         jsonData = json.load(infile)

   return jsonData


def createInstrument(row):
   kp = 0
   items = row.split(',')[1].split('_')

   if items[0].strip().upper() != FUTURE:
      kp = int(items[3])

   return Instrument(items[0], items[1], int(items[2]), kp)


def crawler():
   csvs = []

   # existing volume csv files by date
   volcsvs = list(set([ volcsv.split('_')[0] for volcsv in listdir(DATA_DIR) if volcsv.endswith("csv") ]))

   headers = requests.utils.default_headers()
   headers.update({
      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
      # 'Referer': t.getRef()
   })

   try:
      r = requests.get(BASE_URL + VOLUME_URI, headers=headers, verify=False) #requestsを使って、webから取得
      # print(r.headers['Set-Cookie'])
      soup = BeautifulSoup(r.text, 'lxml')                        #要素を抽出 (lxml)

      # csv file uri: a要素を全て取得
      allcsv = []
      for table in soup.find_all('table'):
         for tr in table.find_all('tr'):
            allcsv.extend([a['href'] for a in tr.find_all('a', href=True) if a['href'].endswith('.csv')])

      # download and rename saving
      for csv in allcsv:
         csvfile = csv.split('/')[-1]
         if csvfile.split('_')[0] not in volcsvs: # not downloaded yet
            print("sleeping 2s ...: " + BASE_URL + csv)
            sleep(2)
            response = requests.get(BASE_URL + csv)

            if response.ok:
               csvpath = DATA_DIR + csvfile
               csvs.append(csvpath)
               with open(csvpath, mode='wb+') as f:   # write, binary, allow creation
                  f.write(response.content)

      return csvs

   except Exception as e:
      print("error: {0}".format(e), file=sys.stderr)
      exitCode = 2


def convCsv2Json(csv):
   jsonfile = os.path.splitext(csv)[0] + '.json'

   # load traders' info
   traders = []

   # Relative Path, depends on OS utf-8 -> sjis
   with open(DATA_DIR + 'traders.json', encoding='utf-8') as f:
      traders = json.load(f)

   # initial data of [date].json
   jsonData = {}
   jsonDataFile = ''

   # read csv line-by-line (BOM of UTF-8)
   with io.open(csv, 'rt', encoding='utf_8_sig') as f:
      # one target starts
      data  = {}
      start = False
      num   = 0

      # data part
      date = 0
      info = []

      target = {}
      jpxCd = ''
      instrument = {}
      vol = []

      for row in f:
         r = row.strip()

         # data["date"]
         if 'Trade Date' in r:
            date = int([d for d in r.split(',') if '20' in d][0].strip())
            # print(date)
            continue

         if r == '' in r:
            if start:
               start = False

            continue

         if 'JPX Code' in r:
            # to create ONE target
            if num != 0:
               target = Target(jpxCd, instrument, vol)
               data['info'].append(target)

               # new target re-init
               target = {}
               jpxCd = ''
               instrument = {}
               vol = []
            else:
               data['date'] = date
               data['info'] = info
               '''
               basedir = os.path.dirname(path)
               if not os.path.exists(basedir):
                  os.makedirs(basedir)
               '''
               jsonDataFile = DATA_DIR + str(date) + '.json'
               jsonData = loadJsonData(jsonDataFile)

            num = num + 1
            start = True

            # data["info"]["jpxCd"]
            jpxCd = r.split(',')[1].strip()
            continue

         if start:
            # data["info"]["instrument"]
            if 'Instrument' in r:
               instrument = createInstrument(r)

            # data["info"]["vol"]
            else:
               items = list(map(str.strip, r.split(',')))

               # seller
               codes = np.array(traders)[:, 0].tolist()
               scd  = "0"
               svol = 0
               if items[0] != '-' and items[1] != '-' and items[2] != '-':
                  scd  = items[0]
                  svol = int(items[3])
                  if scd not in codes:
                     traders.append([scd, items[1], items[2]])

               # buyer
               codes = np.array(traders)[:, 0].tolist()
               bcd  = "0"
               bvol = 0
               if items[-4] != '-' and items[-3] != '-' and items[-2] != '-':
                  bcd  = items[-4]
                  bvol = int(items[-1])
                  if bcd not in codes:
                     traders.append([bcd, items[-3], items[-2]])

               # volume info
               vol.append([scd, svol, bcd, bvol])

      # to create LAST target
      if num != 0:
         target = Target(jpxCd, instrument, vol)
         data['info'].append(target)

   # write all data
   with codecs.open(jsonfile, 'w','utf-8') as f:
      f.write(json.dumps(data, default=default_method, ensure_ascii=False, indent=2, sort_keys=False, separators=(',', ': '))) # JPN utf-8, cls=TargetEncoder?

   # write all traders
   # [x.encode('utf-8') for x in traders]
   with codecs.open(DATA_DIR + 'traders.json','w','utf-8') as f:
      f.write(json.dumps(traders, ensure_ascii=False, indent=2, sort_keys=False, separators=(',', ': ')))

   # over-written all [date].json
   jsonData = data
   with codecs.open(jsonDataFile, 'w','utf-8') as f:
      f.write(json.dumps(jsonData, default=default_method, ensure_ascii=False, indent=2, sort_keys=False, separators=(',', ': '))) # JPN utf-8, cls=TargetEncoder?


def main(argv):

   # convert each csv into json
   list(map(convCsv2Json, crawler()))


if __name__ == "__main__":
   main(sys.argv[1:])

