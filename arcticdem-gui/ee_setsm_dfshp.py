import os
import csv
from pySmartDL import SmartDL
from shapely.geometry import shape, mapping
import fiona
def demdownload(infile=None,destination=None):
    with fiona.open(infile) as input:
        for pol in input:
            reader= pol['properties']['fileurl']
            print reader
            url = reader
            dest = destination
            obj = SmartDL(url, dest)
            obj.start()
            path=obj.get_dest()
