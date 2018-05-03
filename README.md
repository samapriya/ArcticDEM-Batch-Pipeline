# ArcticDEM Batch Download & Processing Tools
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.842056.svg)](https://doi.org/10.5281/zenodo.842056)
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
* [Getting started](#getting-started)
* [Usage examples](#usage-examples)
	* [Subset to AOI](#subset-to-aoi)
    * [Estimate Download Size](#estimate-download-size)
    * [Download DEM](#download-dem)
    * [Extract DEM](#extract-dem)
    * [Metadata Parsing for GEE](#metadata-parsing-for-gee)

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

## Getting started
To obtain help for a specific functionality, simply call it with _help_
switch, e.g.: `arcticdem demextract -h`. If you didn't install arcticdem, then you
can run it just by going to _arcticdem-cli_ directory and running `python
arcticdem.py [arguments go here]`

As usual, to print help  `arcticdem -h`:
```
ArcticDEM Batch Download & Processing Tools
positional arguments:
  { ,demaoi,demsize,demdownload,demextract,demmeta}
                        ---------------------------------------
                        -----Choose from ArcticDEM-Download Tools Below-----
                        ---------------------------------------
    demaoi              Allows user to subset Master ArcticDEM to their AOI
    demsize             Allows users to estimate total download size and space
                        left in your destination folder
    demdownload         Allows users to batch download ArcticDEM Strips using
                        aoi shapefile
    demextract          Allows users to extract both image and metadata files
                        from the zipped tar files
    demmeta             Tool to process metadata files into CSV for all
                        strips[For use with Google Earth Engine]

optional arguments:
  -h, --help            show this help message and exit
```

## Subset to AOI
The script clips the master ArcticDEM strip file to a smaller subset usgin an area of interest shapefile. This allows to get the strip DEM(s) for only the area of interest and to use that to download these files. The subset allows the user to limit the total amount of strips to be downloaded and processed. The script will create a new shapefile with the clipped subset of the master ArcticDEM strip file. 

**Make sure you reproject your aoi shapefile to the same projection as the ArcticDEM strip file** 

```
usage: arcticdem.py demaoi [-h] [--source SOURCE] [--target TARGET]
                           [--output OUTPUT]

optional arguments:
  -h, --help       show this help message and exit
  --source SOURCE  Choose location of your AOI shapefile
  --target TARGET  Choose the location of the master ArcticDEM strip file
  --output OUTPUT  Choose the location of the output shapefile based on your
                   AOI
```
An example setup would be
```
arcticdem demaoi --source "C:\users\aoi.shp" --target "C:\users\masterdem.shp" --output "C:\users\master_aoi.shp"
```

### Estimate Download Size
One of the most common things you want to do is to know if the destination where you want to save these files has enough space before you begin the download process. This script allows you to query the total download size for your area of interest and the destination drive where you want to save the compressed files. It also recursively updates overall download size on the screen and print total size needed along with total download size in GB.

```
usage: arcticdem.py demsize [-h] [--infile INFILE] [--path PATH]

optional arguments:
  -h, --help       show this help message and exit
  --infile INFILE  Choose the clipped aoi file you clipped from demaoi
                   tool[This is the subset of the master ArcticDEM Strip]
  --path PATH      Choose the destination folder where you want your dem files
                   to be saved[This checks available disk space]
```
An example setup would be
```
arcticdem demsize --infile "C:\users\master_aoi.shp" --path "C:\users\ArcticDEM"
```
The program might misbehave if the area of interest is extremely large or be sluggish in nature.


## Download DEM
What we were mainly interested after we know that we have enough space to download is to download the files. The script used a multi part download library to download the files quicker and in a more managed style to the destination given by the user.

```
usage: arcticdem.py demdownload [-h] [--subset SUBSET]
                                [--desination DESINATION]

optional arguments:
  -h, --help            show this help message and exit
  --subset SUBSET       Choose the location of the output shapefile based on
                        your AOI[You got this from demaoi tool]
  --destination DESINATION
                        Choose the destination where you want to download your
                        files
```
An example setup would be
```
arcticdem demdownload --subset "C:\users\master_aoi.shp" --destination "C:\users\ArcticDEM"
```
 
## Extract DEM
This downloaded DEM files are tar or tar gz files and need to be extracted. The important thing to note is that the script retains the dem file, the matchtag file and the metadata text files in separate directories within the destination directory. 

```
usage: arcticdem.py demextract [-h] [--folder FOLDER]
                               [--destination DESTINATION] [--action ACTION]

optional arguments:
  -h, --help            show this help message and exit
  --folder FOLDER       Choose the download file where you downloaded your tar
                        zipped files
  --destination DESTINATION
                        Choose the destination folder where you want your
                        images and metadata files to be extracted
  --action ACTION       Choose if you want your zipped files to be deleted
                        post extraction "yes"|"no"
```
An example setup would be
```
arcticdem demdextract --folder "C:\users\ArcticDEM" --destination "C:\users\ArcticDEM\Extract" --action "yes"
```

## Metadata Parsing for GEE
One of my key interest in working on the ArcticDEM parsing was to be able to upload this to Google Earth Engine(GEE). The metadata parser script allows you to parse all metadata into a combined csv file to be used to upload images to GEE. The manifest and upload tools are separate from this package tool and included in my gee_asset_manager_addon.

```
usage: arcticdem.py demmeta [-h] [--folder FOLDER] [--metadata METADATA]
                            [--error ERROR]

optional arguments:
  -h, --help           show this help message and exit
  --folder FOLDER      Choose where you unzipped and extracted your DEM and
                       metadata files
  --metadata METADATA  Choose a path to the metadata file "example:
                       users/desktop/metadata.csv"
  --error ERROR        Choose a path to the errorlog file "example:
                       users/desktop/errorlog.csv"
```
An example setup would be
```
arcticdem demmeta --folder "C:\users\ArcticDEM\Extract\pgcmeta" --metadata "C:\users\arcticdem_metadata.csv" --error "C:\users\arcticdem_errorlog.csv"
```

## Changelog
### [0.1.2] - 2018-05-03
- Python 3 and linux compatibility

### [0.1.1] - 2017-08-12
### Added
- Can now handle ogr input and includes instruction to project aoi in same projection as DEM strip.
- Added the capability of skipping over already downloaded files and continues with left over downloads.
- Completed recompiling executable to include changes.
