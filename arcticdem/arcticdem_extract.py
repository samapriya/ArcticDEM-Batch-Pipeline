from __future__ import print_function
import geopandas as gpd
import os
import sys
import csv
from requests.packages.urllib3.poolmanager import PoolManager
from geopandas import GeoDataFrame
lpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(lpath)

def clip_extent(gdf, poly):
    gdf_sub = gdf.iloc[gdf.sindex.query(poly, predicate="intersects")]
    if isinstance(gdf_sub, GeoDataFrame):
        clipped = gdf_sub.copy()
        clipped["geometry"] = gdf_sub.intersection(poly)
    else:
        clipped = gdf_sub.intersection(poly)
    return clipped

def selection(ftype,final,extract_file):
    print('Now running spatial extract....')
    folder_name = "ArcticDEM-Index"
    pth = os.path.join(lpath, folder_name)
    if os.path.exists(pth):
        for files in os.listdir(pth):
            if files.endswith('.shp') and ftype in files:
                initial= os.path.join(pth,files)
    else:
        sys.exit('Try acrticdem init')

    try:
        df = gpd.read_file(initial)
        df2 = gpd.read_file(final,encoding='utf-8')
        df2=df2.to_crs(df.crs)
        poly = df2.geometry.unary_union
        geom_intersection = clip_extent(df,poly)
        print('Number of rows that intersect AOI {}'.format(geom_intersection.shape[0]))

        if int(geom_intersection.shape[0])>0:
            url_list = geom_intersection['fileurl'].values.tolist()
            if extract_file is not None:
                writer=csv.writer(open(extract_file,'w'),lineterminator="\n")
                for item in url_list:
                    writer.writerow([item,])
        else:
            print('No intersecting features found')
        return url_list
    except Exception as e:
        print(e)

#selection(ftype="Tile",final=r'C:\Users\samapriya\Downloads\arctic_small\POLYGON.shp',extract_file=r'C:\planet_demo\extract_tile.csv')

# suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]


# def humansize(nbytes):
#     i = 0
#     while nbytes >= 1024 and i < len(suffixes) - 1:
#         nbytes /= 1024.0
#         i += 1
#     f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
#     return "{}  {}".format(f, suffixes[i])


# def demsize(ftype, infile):
#     summation=[]
#     try:
#         if infile.endswith('.csv'):
#             with open(infile, 'r') as csvfile:
#                 reader = csv.reader(csvfile)
#                 ulist= [row[0] for row in reader]
#         elif infile.endswith('.shp'):
#             ulist = selection(ftype,infile,extract_file=None)
#         print('Processing a total of {} objects in File URL list'.format(len(ulist)))
#         for download_url in ulist:
#             pool = PoolManager()
#             response = pool.request("GET", download_url, preload_content=False)
#             max_bytes = 1000000000000
#             content_bytes = response.headers.get("Content-Length")
#             summation.append(float(content_bytes))
#             print('Estimated Total Size: {}'.format(humansize(sum(summation))), end='\r')
#     except KeyError:
#         print('Could not check size')
#     print ('\n'+"Total Download Size: {}".format(humansize(sum(summation))))

# demsize(ftype="Strip",infile=r'C:\Users\samapriya\Downloads\arctic_large\POLYGON.shp')
