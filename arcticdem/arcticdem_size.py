import os
import csv
import random
import requests
from .arcticdem_extract import selection
from requests.packages.urllib3.poolmanager import PoolManager

suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]


def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "{}  {}".format(f, suffixes[i])


def demsize(ftype, infile):
    choicelist = [
        "Go grab some tea.....",
        "Go Stretch.....",
        "Go take a walk.....",
        "Go grab some coffee.....",
    ]  # adding something fun
    print("This might take sometime. {}".format(random.choice(choicelist)))
    summation = []
    try:
        if infile.endswith(".csv"):
            with open(infile, "r") as csvfile:
                reader = csv.reader(csvfile)
                ulist = [row[0] for row in reader]
        elif infile.endswith(".shp") and ftype is not None:
            ulist = selection(ftype, infile, extract_file=None)
        elif infile.endswith(".shp") and ftype is None:
            sys.exit("Pass an ftype: Strip or Tile")
        print("Processing a total of {} objects in File URL list".format(len(ulist)))
        for download_url in ulist:
            pool = PoolManager()
            response = pool.request("GET", download_url, preload_content=False)
            max_bytes = 1000000000000
            content_bytes = response.headers.get("Content-Length")
            summation.append(float(content_bytes))
            print(
                "Estimated Total Size: {}".format(humansize(sum(summation))), end="\r"
            )
    except KeyError:
        print("Could not check size")
    print("\n" + "Total Download Size: {}".format(humansize(sum(summation))))
