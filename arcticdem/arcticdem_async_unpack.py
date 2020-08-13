from __future__ import print_function

__copyright__ = """
    Copyright 2019 Samapriya Roy
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

import requests
import asyncio
import os
import json
import glob
import progressbar
import sys
import time
import tarfile
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
from retrying import retry


def unpack(inpath, outfolder):
    t = tarfile.open(inpath, "r")
    for member in t.getmembers():
        if member.name.startswith("index"):
            try:
                fpath = outfolder
                if not os.path.exists(
                    os.path.join(fpath, os.path.basename(member.name))
                ):
                    print(
                        "Processing: {} and Extracting: {}".format(
                            os.path.basename(inpath), os.path.basename(member.name)
                        )
                    )
                    t.extract(member, fpath)
                else:
                    print(
                        "File already exists SKIPPING: {}".format(
                            os.path.basename(member.name)
                        )
                    )
            except Exception as e:
                print(e)
        elif member.name.endswith("dem.tif"):
            try:
                fpath = os.path.join(outfolder, "dem")
                if not os.path.exists(
                    os.path.join(fpath, os.path.basename(member.name))
                ):
                    print(
                        "Processing: {} and Extracting: {}".format(
                            os.path.basename(inpath), os.path.basename(member.name)
                        )
                    )
                    t.extract(member, fpath)
                else:
                    print(
                        "File already exists SKIPPING: {}".format(
                            os.path.basename(member.name)
                        )
                    )
            except Exception as e:
                print(e)
        elif member.name.endswith("matchtag.tif"):
            try:
                fpath = os.path.join(outfolder, "matchtag")
                if not os.path.exists(
                    os.path.join(fpath, os.path.basename(member.name))
                ):
                    print(
                        "Processing: {} and Extracting: {}".format(
                            os.path.basename(inpath), os.path.basename(member.name)
                        )
                    )
                    t.extract(member, fpath)
                else:
                    print(
                        "File already exists SKIPPING: {}".format(
                            os.path.basename(member.name)
                        )
                    )
            except Exception as e:
                print(e)
        elif member.name.endswith("browse.tif"):
            try:
                fpath = os.path.join(outfolder, "browse")
                if not os.path.exists(
                    os.path.join(fpath, os.path.basename(member.name))
                ):
                    print(
                        "Processing: {} and Extracting: {}".format(
                            os.path.basename(inpath), os.path.basename(member.name)
                        )
                    )
                    t.extract(member, fpath)
                else:
                    print(
                        "File already exists SKIPPING: {}".format(
                            os.path.basename(member.name)
                        )
                    )
            except Exception as e:
                print(e)
        elif member.name.endswith("mdf.txt"):
            try:
                fpath = os.path.join(outfolder, "mdf")
                if not os.path.exists(
                    os.path.join(fpath, os.path.basename(member.name))
                ):
                    print(
                        "Processing: {} and Extracting: {}".format(
                            os.path.basename(inpath), os.path.basename(member.name)
                        )
                    )
                    t.extract(member, fpath)
                else:
                    print(
                        "File already exists SKIPPING: {}".format(
                            os.path.basename(member.name)
                        )
                    )
            except Exception as e:
                print(e)


START_TIME = default_timer()


def fetch(url, final):
    inpath = url.split("|")[0]
    outfolder = url.split("|")[1]
    unpack(inpath, outfolder)


flist = []


def funct(folder, final):
    for files in os.listdir(folder):
        if files.endswith(".tar.gz"):
            flist.append(os.path.join(folder, files) + "|" + final)
    print("Processing a total of " + str(len(flist)) + " tar.gz files")
    print("\n")
    return flist


async def get_data_asynchronous(folder, final):
    urllist = funct(folder, final)
    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() - 1) as executor:
        loop = asyncio.get_event_loop()
        START_TIME = default_timer()
        tasks = [
            loop.run_in_executor(
                executor,
                fetch,
                *(url, final)  # Allows us to pass in multiple arguments to `fetch`
            )
            for url in urllist
        ]
        for response in await asyncio.gather(*tasks):
            pass


def unpacker(folder, final):
    if not os.path.exists(final):
        os.makedirs(final)
    if not os.path.exists(os.path.join(final, "dem")):
        os.makedirs(os.path.join(final, "dem"))
    if not os.path.exists(os.path.join(final, "matchtag")):
        os.makedirs(os.path.join(final, "matchtag"))
    if not os.path.exists(os.path.join(final, "mdf")):
        os.makedirs(os.path.join(final, "mdf"))
    if not os.path.exists(os.path.join(final, "browse")):
        os.makedirs(os.path.join(final, "browse"))
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(folder, final))
    loop.run_until_complete(future)


# downloader(folder=r'C:\planet_demo\px\arctic',final=r'C:\planet_demo\px\extract')
