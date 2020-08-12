#! /usr/bin/env python

__copyright__ = """

    Copyright 2020 Samapriya Roy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

import os
import sys
import time
import argparse
import subprocess
import csv
import requests
import platform
from os.path import expanduser
if str(platform.system().lower()) == "windows":
    # Get python runtime version
    version =sys.version_info[0]
    try:
        import pipwin
        if pipwin.__version__=='0.5.0':
            pass
        else:
            a=subprocess.call('{} -m pip install pipwin==0.5.0'.format(sys.executable), shell=True,stdout=subprocess.PIPE)
            subprocess.call('pipwin refresh', shell=True)
        '''Check if the pipwin cache is old: useful if you are upgrading porder on windows
        [This section looks if the pipwin cache is older than two weeks]
        '''
        home_dir = expanduser("~")
        fullpath=os.path.join(home_dir, ".pipwin")
        file_mod_time = os.stat(fullpath).st_mtime
        if int((time.time() - file_mod_time) / 60) > 20160:
            print('Refreshing your pipwin cache')
            subprocess.call('pipwin refresh', shell=True)
    except ImportError:
        a=subprocess.call('{} -m pip install pipwin==0.5.0'.format(sys.executable), shell=True,stdout=subprocess.PIPE)
        subprocess.call('pipwin refresh', shell=True)
    except Exception as e:
        print(e)
    try:
        import gdal
    except ImportError:
        subprocess.call('pipwin install gdal', shell=True)
    except Exception as e:
        print(e)
    try:
        import pyproj
    except ImportError:
        subprocess.call('pipwin install pyproj', shell=True)
    except Exception as e:
        print(e)
    try:
        import shapely
    except ImportError:
        subprocess.call('pipwin install shapely', shell=True)
    except Exception as e:
        print(e)
    try:
        import fiona
    except ImportError:
        subprocess.call('pipwin install fiona', shell=True)
    except Exception as e:
        print(e)
    try:
        import geopandas
    except ImportError:
        subprocess.call('pipwin install geopandas', shell=True)
    except Exception as e:
        print(e)
    try:
        import rtree
    except ImportError:
        subprocess.call('pipwin install rtree', shell=True)
    except Exception as e:
        print(e)
from bs4 import BeautifulSoup
from .arcticdem_init import search_index
from .arcticdem_extract import selection
from .arcticdem_size import demsize
from .arcticdem_download import download
from .arcticdem_async_unpack import unpacker
lpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(lpath)

# Get package version
def arcticdem_version():
    url = "https://pypi.org/project/arcticdem/"
    source = requests.get(url)
    html_content = source.text
    soup = BeautifulSoup(html_content, "html.parser")
    company = soup.find("h1")
    if (
        not pkg_resources.get_distribution("arcticdem").version
        == company.string.strip().split(" ")[-1]
    ):
        print(
            "\n"
            + "========================================================================="
        )
        print(
            "Current version of articdem is {} upgrade to lastest version: {}".format(
                pkg_resources.get_distribution("geeadd").version,
                company.string.strip().split(" ")[-1],
            )
        )
        print(
            "========================================================================="
        )


#arcticdem_version()

def init_from_parser(args):
    search_index()

def extract_from_parser(args):
    selection(ftype=args.ftype, final=args.aoi,extract_file=args.outfile)

def size_from_parser(args):
    demsize(ftype=args.ftype, infile=args.infile)

def download_from_parser(args):
    download(ftype=args.ftype, infile=args.infile,path=args.path)

def unpacker_from_parser(args):
    unpacker(folder=args.input, final=args.output)

def main(args=None):
    parser = argparse.ArgumentParser(
        description="ArcticDEM Simple Command Line Interface"
    )
    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser("init", help="Get Strip and Tile Shapefiles and setup from ArcticDEM")
    parser_init.set_defaults(func=init_from_parser)

    parser_extract = subparsers.add_parser("extract", help="Extract AOI based File URL list")
    required_named = parser_extract.add_argument_group("Required named arguments.")
    required_named.add_argument("--ftype",help="Search type: Tile or Strip",required=True)
    required_named.add_argument("--aoi",help="Input shapefile of AOI",required=True)
    required_named.add_argument("--outfile",help="Full path to extracted CSV file",required=True)
    parser_extract.set_defaults(func=extract_from_parser)

    parser_size = subparsers.add_parser("size", help="Generate estimated download size of DEM files for AOI")
    required_named = parser_size.add_argument_group("Required named arguments.")
    required_named.add_argument("--infile",help="Input shapefile of AOI or extracted CSV file",required=True)
    optional_named = parser_size.add_argument_group("Optional named arguments")
    optional_named.add_argument("--ftype",help="Search type: Tile or Strip", default=None)
    parser_size.set_defaults(func=size_from_parser)

    parser_download = subparsers.add_parser("download", help="Download DEM files for AOI")
    required_named = parser_download.add_argument_group("Required named arguments.")
    required_named.add_argument("--infile",help="Input shapefile of AOI or extracted CSV file",required=True)
    required_named.add_argument("--path",help="Output folder to save files",required=True)
    optional_named = parser_download.add_argument_group("Optional named arguments")
    optional_named.add_argument("--ftype",help="Search type: Tile or Strip", default=None)
    parser_download.set_defaults(func=download_from_parser)

    parser_unpacker = subparsers.add_parser("unpacker", help="Unpack downloaded tar.gz DEM files")
    required_named = parser_unpacker.add_argument_group("Required named arguments.")
    required_named.add_argument("--input",help="Input folder with downloaded tar.gz files",required=True)
    required_named.add_argument("--output",help="Output folder where files are unzipped",required=True)
    parser_unpacker.set_defaults(func=unpacker_from_parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
