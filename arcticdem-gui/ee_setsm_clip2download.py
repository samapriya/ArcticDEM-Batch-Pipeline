import os
import csv
from pySmartDL import SmartDL
from shapely.geometry import shape, mapping
import fiona
def pgcaoi(source=None,target=None,output=None,destination=None):
    os.system('ogr2ogr -f "ESRI Shapefile" -clipsrc '+source+" "+output+" "+target+" -skipfailures")
    print("Clip Completed")
    target=infile
    with fiona.open(infile) as input:
        for pol in input:
            reader= pol['properties']['fileurl']
            print reader
            url = reader
            dest = destination
            obj = SmartDL(url, dest)
            obj.start()
            path=obj.get_dest()
