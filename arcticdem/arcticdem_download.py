import os
import csv
import time
import requests
from .arcticdem_extract import selection


def download(ftype,infile,path):
    i=1
    try:
        if infile.endswith('.csv'):
            with open(infile, 'r') as csvfile:
                reader = csv.reader(csvfile)
                ulist= [row[0] for row in reader]
        elif infile.endswith('.shp') and ftype is not None:
            ulist = selection(ftype,infile,extract_file=None)
        elif infile.endswith('.shp') and ftype is None:
            sys.exit('Pass an ftype: Strip or Tile')
        print('')
        for url in ulist:
            if not os.path.exists(os.path.join(path,os.path.basename(url))):
                print('Downloading {} of {} : {}'.format(i,len(ulist),os.path.basename(url)))
                result=requests.get(url)
                if result.status_code==200:
                    try:
                        f = open(os.path.join(path,os.path.basename(url)), 'wb')
                        for chunk in result.iter_content(chunk_size=512 * 1024):
                            if chunk:
                                f.write(chunk)
                        f.close()
                        i=i+1
                    except Exception as e:
                        print(e)
                        i=i+1
                else:
                    print('Download from serve failed with status {}'.format(result.status_code))
                    i=i+1
            else:
                print('File already exists SKIPPING: {}'.format(os.path.basename(url)))
                i=i+1
    except Exception as e:
        print(e)
