import os
import sys
import shutil
import zipfile
import requests
import fiona
import urllib.request
import glob
from shutil import move
from bs4 import BeautifulSoup

lpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(lpath)

## Index list
def indices():
    r = requests.get("http://data.pgc.umn.edu/elev/dem/setsm/ArcticDEM/indexes/")
    item_list = []
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        td_list = soup.find_all("td")
        for items in td_list:
            try:
                if items.a.get("href").endswith(".zip"):
                    item_list.append(items.a.get("href"))
            except:
                pass
        return item_list
    else:
        print("Request failed with status {}".format(r.status_code))


## Reformat Shapefile
def reformat():
    # set base folder names and paths
    folder_name = "ArcticDEM-Base"
    pth = os.path.join(lpath, folder_name)
    fpth = os.path.join(lpath, "ArcticDEM-Index")
    if not os.path.exists(fpth):
        os.makedirs(fpth)
    filelist = glob.glob(pth + "/*.shp")
    for files in filelist:
        src = fiona.open(files)
        keep_columns = ["fileurl"]  # Keeping only File URLs

        # create the output schema from the input
        output_schema = src.schema.copy()
        # create new properties schema without the columns we don't want
        output_schema["properties"] = {
            column_name: typ
            for column_name, typ in output_schema["properties"].items()
            if column_name in keep_columns
        }
        # # Open output file
        outfile = os.path.join(fpth, os.path.basename(files))
        print("Writing {}".format(os.path.basename(files)))
        sink = fiona.open(
            outfile, "w", driver="ESRI Shapefile", schema=output_schema, crs=src.crs
        )
        for feature in src:
            feature["properties"] = {
                column_name: value
                for column_name, value in feature["properties"].items()
                if column_name in keep_columns
            }
            sink.write(feature)


def search_index():
    # get os type
    name = os.name

    # set base folder names and paths
    folder_name = "ArcticDEM-Base"
    pth = os.path.join(lpath, folder_name)
    fpth = os.path.join(lpath, "ArcticDEM-Index")
    index_filenames = indices()
    base_filenames = [file.split(".")[0] for file in index_filenames]
    existing_files = []
    if os.path.exists(pth):
        for f in os.listdir(pth):
            if f.endswith(".shp"):
                existing_files.append(f.split(".")[0])
    difference = set(base_filenames) - set(existing_files)
    if len(difference) == 0:
        for files in base_filenames:
            print("Using release version: {}".format(files))
        print("")
        sys.exit("No changes to existing version")
    if len(difference) > 0:
        if os.path.exists(pth):
            if name == "nt":
                os.system("rmdir " + '"' + pth + '" /s /q')
                os.system("rmdir " + '"' + fpth + '" /s /q')
            elif name == "posix":
                try:
                    shutil.rmtree(pth)
                    shutil.rmtree(fpth)
                except:
                    print("Try using sudo privileges")
        for f in os.listdir(lpath):
            if f.endswith(".zip"):
                try:
                    os.unlink(os.path.join(lpath, f))
                except WindowsError:
                    with open(os.path.join(lpath, f), mode="w") as outfile:
                        outfile.close()
        for filename in index_filenames:
            try:
                if "Strip" in filename:
                    out_file_path = os.path.join(lpath, "strip.zip")
                    urllib.request.urlretrieve(
                        "http://data.pgc.umn.edu/elev/dem/setsm/ArcticDEM/indexes/"
                        + filename,
                        out_file_path,
                    )
                    zip_ref = zipfile.ZipFile(out_file_path)
                    for file in zip_ref.namelist():
                        if zip_ref.getinfo(file).filename.endswith(".shp"):
                            print(
                                "Using release version for Strip: {}".format(
                                    file.split(".")[0]
                                )
                            )
                    for file in zip_ref.namelist():
                        zip_ref.extract(file, pth)
                elif "Tile" in filename:
                    out_file_path = os.path.join(lpath, "tile.zip")
                    urllib.request.urlretrieve(
                        "http://data.pgc.umn.edu/elev/dem/setsm/ArcticDEM/indexes/"
                        + filename,
                        out_file_path,
                    )
                    zip_ref = zipfile.ZipFile(out_file_path)
                    for file in zip_ref.namelist():
                        if zip_ref.getinfo(file).filename.endswith(".shp"):
                            print(
                                "Using release version for Tile: {}".format(
                                    file.split(".")[0]
                                )
                            )
                    for file in zip_ref.namelist():
                        zip_ref.extract(file, pth)
            except Exception as e:
                print(
                    "The URL is invalid. Please double check the URL or error. {}".format(
                        e
                    )
                )
    reformat()


# search_index()
