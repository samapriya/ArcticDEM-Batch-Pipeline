from __future__ import print_function
import os
import csv
from pySmartDL import SmartDL
from shapely.geometry import shape, mapping
import fiona

def demdownload(infile=None,destination=None):
    with fiona.open(infile) as input:
        for pol in input:
            reader= pol['properties']['fileurl']
            fname= os.path.basename(reader)
            fpath=os.path.join(destination,fname)
            if not os.path.exists(fpath):
                url=reader
                dest=destination
                obj=SmartDL(url,dest)
                obj.start()
                path=obj.get_dest()
            else:
                print("Skipping...."+str(fname), end='\r')
        print("Download Completed")
            
