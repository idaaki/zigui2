#!/usr/bin/python3
# coding: utf-8

from __future__ import print_function

import sys
import requests
import re
from bs4 import BeautifulSoup

target_url = 'https://stocks.finance.yahoo.co.jp/stocks/detail/?code=1301'
try:
    r = requests.get(target_url)            #requests���g���āAweb����擾
    soup = BeautifulSoup(r.text, 'lxml')    #�v�f�𒊏o (lxml)

    stoksPrice = soup.find('td', class_='stoksPrice')
    stoksPrice = stoksPrice.find_next_sibling('td').text
    stoksPrice = float(re.sub('[,]', '', stoksPrice))
    print(stoksPrice)

    cnt = 0
    for dd in soup.find_all('dd', class_='ymuiEditLink mar0'):
        stng = dd.find('strong').text
        stng = float(re.sub('[,]', '', stng))
        print(stng)
        cnt += 1
        if cnt > 5:
            break


    # Debug
    '''
    for td in soup.find_all('td'):
        print(td.text.encode('cp932', 'ignore'))
        print(td.get('class'))
    '''

    #�����N��\�� (lxml)
    '''
    for a in soup.find_all('a'):
        print(a.get('href'))
    '''

except Exception as e:
    print("error: {0}".format(e), file=sys.stderr)
    exitCode = 2

### output
'''
3095.0
3005.0
3025.0
3105.0
3025.0
26000.0
79571.0
'''
