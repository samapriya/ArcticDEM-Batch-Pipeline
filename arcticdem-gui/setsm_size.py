from __future__ import print_function
import argparse
import os,requests,json,sys,csv
import urllib3,psutil,logging,fiona
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings()

def demsize(path, infile):
    results = []
    summation=0
    spc=psutil.disk_usage(path).free
    remain=float(spc)/1073741824
    # now start downloading each file
    try:
        with fiona.open(infile) as input:
            for pol in input:
                reader= pol['properties']['fileurl']
                download_url = reader
                pool = PoolManager()
                response = pool.request("GET", download_url, preload_content=False)
                max_bytes = 100000000000
                content_bytes = response.headers.get("Content-Length")
                summary=float(content_bytes)/1073741824
                summation=summation+summary
                print(format(float(summation),'.2f'),"GB", end='\r')
            else:
                result = False
    except KeyError:
        print('Could not check size')

        #print(remain,"MB")
    print("Remaining Space in GB",format(float(remain),'.2f'))
    print ("Total Download Size in GB",format(float(summation),'.2f'))

