# ArcticDEM Batch Download & Processing Tools
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1240456.svg)](https://doi.org/10.5281/zenodo.1240456)
![CI arcticdem](https://github.com/samapriya/ArcticDEM-Batch-Pipeline/workflows/CI%20arcticdem/badge.svg)
[![PGC](https://img.shields.io/badge/PGC-BootCamp%202017-green.svg)](https://www.pgc.umn.edu/)


ArcticDEM project was a joint project supported by both the National Geospatial-Intelligence Agency(NGA) and the National Science Foundation(NSF) with the idea of creating a high resolution and high quality digital surface model(DSM). The product is distributed free of cost as time-dependent DEM strips and is hosted as https links that a user can use to download each strip. As per their policy

*The seamless terrain mosaic can be distributed without restriction.*

The created product is a 2-by-2 meter elevation cells over an over of over 20 million square kilometers and uses digital globe stereo imagery to create these high resolution DSM. The method used for the 2m derivate is Surface Extraction with TIN-based Search-space Minimization(SETSM).

Based on their acknowledgements requests you can use
*Acknowledging PGC services(including data access)*

* Geospatial support for this work provided by the Polar Geospatial Center under NSF OPP awards 1043681 & 1559691.

*Acknowledging DEMS created from the ArcticDEM project*

* DEMs provided by the Polar Geospatial Center under NSF OPP awards 1043681, 1559691 and 1542736.

You can find details on the background, scope and methods among other details [here](https://www.pgc.umn.edu/guides/arcticdem/introduction-to-arcticdem/?print=pdf)
A detailed acknowledgement link can be found [here](https://www.pgc.umn.edu/guides/user-services/acknowledgement-policy/)

With this in mind and with the potential applications of using these toolsets there was a need to batch download the DEM files for your area of interest and to be able to extract, clean and process metadata. In all fairness this tool has a motive of extending this as an input to Google Earth Engine and hence the last tool which is the metadata parser is designed to create a metadata manifest in a csv file which GEE can understand and associate during asset upload.

## Table of contents
* [Installation](#installation)
* [Windows Setup](#windows-setup)
* [Getting started](#getting-started)
* [Usage examples](#usage-examples)
    * [ArcticDEM init](#subset-to-aoi)
    * [ArcticDEM extract](#arcticdem-extract)
    * [ArcticDEM size](#arcticdem-size)
    * [ArcticDEM download](#arcticdem-download)
    * [ArcticDEM unpacker](#arcticdem-unpacker)

## Installation
We assume that you have installed the requirements files to install all the necessary packages and libraries required to use this tool. To install packages from the requirements.txt file you can simply use
```pip install -r requirements.txt```. Remember that installation is an optional step and you can run this program by simply browsing to the pgcdem-cli file and typing ```python arcticdem.py```. One of the only other requirement for this tool is the Master Shapefile for all DEM footprints(make sure to use the most updated version which can be found [here](https://www.pgc.umn.edu/data/arcticdem/))

**This toolbox also uses some functionality from GDAL**
For installing GDAL in Ubuntu
```
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get install gdal-bin
```
For Windows I found this [guide](https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows) from UCLA

To install **ArcticDEM Batch Download & Processing Tools:**
```
git clone https://github.com/samapriya/ArcticDEM-Batch-Pipeline.git
cd ArcticDEM-Batch-Pipeline && pip install .
```
This release also contains a windows installer which bypasses the need for you to have admin permission, it does however require you to have python in the system path meaning when you open up command prompt you should be able to type python and start it within the command prompt window. Post installation using the installer you can just call ppipe using the command prompt similar to calling python. Give it a go post installation type
```
arcticdem -h
```
The advantage of having it installed is being able to execute ppipe as any command line tool. I recommend installation within virtual environment. As a extra addon feature I have wrapped the cli into a Graphical User Interface(GUI) so some people will find it easier to use.

To install run
```
python setup.py develop or python setup.py install

In a linux distribution
sudo python setup.py develop or sudo python setup.py install
```

## Windows Setup
Shapely and a few other libraries are notoriously difficult to install on windows machines so follow the steps mentioned here **before installing arcticdem**. You can download and install shapely and other libraries from the [Unofficial Wheel files from here](https://www.lfd.uci.edu/~gohlke/pythonlibs) download depending on the python version you have. **Do this only once you have install GDAL**. I would recommend the steps mentioned above to get the GDAL properly installed. However I am including instructions to using a precompiled version of GDAL similar to the other libraries on windows. You can test to see if you have gdal by simply running

```gdalinfo```

in your command prompt. If you get a read out and not an error message you are good to go. If you don't have gdal try Option 1,2 or 3 in that order and that will install gdal along with the other libraries

#### Option 1:
Starting from arcticdem v0.2.0 onwards:

Simply run ```arcticdem -h``` after installation. This should go fetch the extra libraries you need and install them. Once installation is complete, the arcticdem help page will show up. This should save you from the few steps below.

#### Option 2:
If this does not work or you get an unexpected error try the following commands. You can also use these commands if you simply want to update these libraries.

```
pipwin refresh
pipwin install gdal
pipwin install pyproj
pipwin install shapely
pipwin install fiona
pipwin install geopandas
pipwin install rtree
```

#### Option 3
For windows first thing you need to figure out is your Python version and whether it is 32 bit or 64 bit. You can do this by going to your command prompt and typing python.

![windows_cmd_python](https://user-images.githubusercontent.com/6677629/63856293-3dfc2b80-c96f-11e9-978d-d2c1a01cfe36.PNG)

For my windows machine, I have both 32-bit python 2.7.16 and 64-bit Python 3.6.6. You can get the python version at the beginning of the highlighted lines and the 32 or 64 bit within the Intel or AMD64 within the square brackets. Your default python is the one you get by just typing python in the command line. Then download the following packages based on the information we collect about our python type in the earlier step. We use unofficial binaries to install these. This step is only needed if you are on a windows machine if you are using a setup manager like anaconda you **might** be able to avoid this setup completely

At this stage **if you were unable to install gdal then download the gdal binaries first**, install that before everything else

gdal: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)

Then follow along the following libraries
* pyproj: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyproj](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyproj)
* shapely: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)
* fiona: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona)
* geopandas: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#geopandas](https://www.lfd.uci.edu/~gohlke/pythonlibs/#geopandas)
* rtree: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#rtree](https://www.lfd.uci.edu/~gohlke/pythonlibs/#rtree)

To choose the version that is correct for you use the python information you collected earlier
For example for my python 3.6.6 and AMD 64 if I was installing shapely I would choose the following, here 36 means python 3.6 and amd64 refers to the 64bit we were talking about.

```Shapely‑1.6.4.post2‑cp36‑cp36m‑win_amd64.whl```

You will get a wheel file or a file ending with .whl. You can now simply browse to the folder or migrate to it in your command prompt. Once there if I am installing for my python 3.6 the command was. At this point we will make use of our trusted package installer that comes with python called pip. Note the choice of pip or pip3 depends on your python version usually you can get the pip to use with your python by typing


```pip3 -V```

you get a readout like this

```pip 18.1 from c:\python3\lib\site-packages\pip (python 3.6)```

if you have pip just replace that with ```pip -V```

Then simply install the wheel files you downloaded using the following setup

```
pip3 install full path to Shapely‑1.6.4.post2‑cp36‑cp36m‑win_amd64.whl

in my case that would be

pip3 install "C:\Users\samapriya\Downloads\Shapely‑1.6.4.post2‑cp36‑cp36m‑win_amd64.whl"
```

Or you can use [anaconda to install](https://conda-forge.github.io/). Again, both of these options are mentioned on [Shapely’s Official PyPI page](https://pypi.org/project/Shapely/).

## Getting started
To obtain help for a specific functionality, simply call it with _help_ switch, e.g.: `arcticdem unpacker -h`.

As usual, to print help  `arcticdem -h`:
```
usage: arcticdem [-h] {init,extract,size,download,unpacker} ...

ArcticDEM Simple Command Line Interface

positional arguments:
  {init,extract,size,download,unpacker}
    init                Get Strip and Tile Shapefiles and setup from ArcticDEM
    extract             Extract AOI based File URL list
    size                Generate estimated download size of DEM files for AOI
    download            Download DEM files for AOI
    unpacker            Unpack downloaded tar.gz DEM files

optional arguments:
  -h, --help            show this help message and exit
```

## ArcticDEM init
This tool fetches the index files for both ArcticDEM Strip and Tile and makes sure you have the most updated copy of the index shapefiles as provided by the Polar Geospatial Center. Since the most relevant columns are the geometry and the file URL column these are the only two that are retained and this allows for the index files to be read into geopandas much quicker and for performing faster overlay analysis. This tool takes no arguments.

```
usage: arcticdem init [-h]

optional arguments:
  -h, --help  show this help message and exit
```
An example setup would be
```
arcticdem init
```

### ArcticDEM extract
While this tool is optional it speeds up your download process because it creates a subset CSV containing the download URLs provided your AOI as a shapefile for now. The tool tries to auto reproject your shapefile so they are in the same projection system. The argument allows you to pass whether you want to use Tiles or Strips to create the extract and the full path to the extracted CSV file with file URLs to be written out.

```
arcticdem extract -h
usage: arcticdem extract [-h] --ftype FTYPE --aoi AOI --outfile OUTFILE

optional arguments:
  -h, --help         show this help message and exit

Required named arguments.:
  --ftype FTYPE      Search type: Tile or Strip
  --aoi AOI          Input shapefile of AOI
  --outfile OUTFILE  Full path to extracted CSV file
```

An example setup would be
```
arcticdem extract --ftype Strip --aoi "full path to aoi.shp" --outfile "full path to extract.csv"
```

### ArcticDEM size
One of the most common things you want to do is to know if the destination where you want to save these files has enough space before you begin the download process. This script allows you to query the total download size for your area of interest using either your AOI as shapefile or the extracted CSV file which you might have created earlier. If you use the shapefile as infile you have to provide index type while using the extracted CSV will be faster in returning results.

```
arcticdem size -h
usage: arcticdem size [-h] --infile INFILE [--ftype FTYPE]

optional arguments:
  -h, --help       show this help message and exit

Required named arguments.:
  --infile INFILE  Input shapefile of AOI or extracted CSV file

Optional named arguments:
  --ftype FTYPE    Search type: Tile or Strip
```
An example setup would be
```
arcticdem size --infile "full path to aoi.shp" --ftype Strip

or

arcticdem size --infile "full path to extract.csv"
```

The program might misbehave if the area of interest is extremely large or be sluggish in nature.


## ArcticDEM download
What we were mainly interested after we know that we have enough space to download is to download the files. The download takes into consideration that the server might reject too many calls and tries to download using the extracted CSV file or the AOI shapefile and the index type (Strip or Tile). As expected an output folder is also needed.

```
arcticdem download -h
usage: arcticdem download [-h] --infile INFILE --path PATH [--ftype FTYPE]

optional arguments:
  -h, --help       show this help message and exit

Required named arguments.:
  --infile INFILE  Input shapefile of AOI or extracted CSV file
  --path PATH      Output folder to save files

Optional named arguments:
  --ftype FTYPE    Search type: Tile or Strip
```
An example setup would be
```
arcticdem download --infile "Full path to aoi.shp" --path "Full folder path to download" --ftype Strip

or

arcticdem download --infile "Full path to extract.csv" --path "Full folder path to download"
```

## ArcticDEM unpacker
This is a rapid async unzip tool that extracts and places the final files into predefined folders. In this case these are predefined for my purpose and creates the following folders

* Index
* matchtag
* dem
* mdf
* browse

  The script retains the file names and is designed to unpack these files faster. The choice of folder pertains to my need to parsing through the ArcticDEM strips and extracting files as I need them and can be modified to be a more general downloader to extract everything without sort.

```
arcticdem unpacker -h
usage: arcticdem unpacker [-h] --input INPUT --output OUTPUT

optional arguments:
  -h, --help       show this help message and exit

Required named arguments.:
  --input INPUT    Input folder with downloaded tar.gz files
  --output OUTPUT  Output folder where files are unzipped
```
An example setup would be
```
arcticdem unpacker --input "Full path to input folder with tar.gz files" --output "Full path to folder with extracted files"
```


## Changelog

### v0.2.0
- Major overhaul of underlying program
- Most functions have been rewritten and optimized to meet Python3 standards
- Async unpacker has been included for faster extraction of files
- Overall estimation of size tool as well as geometry functions have been Optimized
- Auto installation of libraries for windows has been enabled using pipwin
- Autochecks for updated version on PyPI and informs the user

### [0.1.2] - 2018-05-03
- Python 3 and linux compatibility

### [0.1.1] - 2017-08-12
### Added
- Can now handle ogr input and includes instruction to project aoi in same projection as DEM strip.
- Added the capability of skipping over already downloaded files and continues with left over downloads.
- Completed recompiling executable to include changes.
