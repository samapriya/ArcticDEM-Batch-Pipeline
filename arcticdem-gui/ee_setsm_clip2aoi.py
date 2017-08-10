import os
import csv
import subprocess
from pySmartDL import SmartDL
import fiona
from shapely.geometry import shape, mapping
def demaoi(source=None,target=None,output=None):
    subprocess.call('ogr2ogr -f "ESRI Shapefile" -clipsrc '+source+" "+output+" "+target+" -skipfailures")
    print("Clip Completed")
