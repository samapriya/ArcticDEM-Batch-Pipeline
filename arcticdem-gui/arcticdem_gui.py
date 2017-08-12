#! /usr/bin/env python

import argparse,logging,os,sys
import subprocess,getpass,csv,re
import time,shutil
from ee_setsm_clip2aoi import demaoi
from setsm_size import demsize
from ee_setsm_dfshp import demdownload
from ee_targz_ext_extract import demextract
from ee_setsm_meta2file import demmeta

from os.path import expanduser
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def demaoi_from_parser(args):
    demaoi(source=args.source,target=args.target,output=args.output)
def demsize_from_parser(args):
    demsize(path=args.path,infile=args.infile)
def demdownload_from_parser(args):
    demdownload(infile=args.subset,destination=args.destination)
def demextract_from_parser(args):
    demextract(directory=args.folder,destination=args.destination,delete=args.action)
def demmeta_from_parser(args):
    demmeta(folder=args.folder,mfile=args.metadata,errorlog=args.error)

spacing="                               "
from gooey import Gooey, GooeyParser
@Gooey(dump_build_config=True, program_name="ArcticDEM Batch Download & Processing Tools")
def main(args=None):
    parser = GooeyParser(description='ArcticDEM Batch Download & Processing Tools')

    subparsers = parser.add_subparsers()
    nonbuffered_stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdout = nonbuffered_stdout
    
    parser_demaoi = subparsers.add_parser('demaoi', help='Allows user to subset Master ArcticDEM to their AOI')
    parser_demaoi.add_argument('--source', help='Choose location of your AOI shapefile',default=None,widget="MultiFileChooser")
    parser_demaoi.add_argument('--target', help='Choose the location of the master ArcticDEM strip file',default=None,widget="MultiFileChooser")
    parser_demaoi.add_argument('--output', help='Choose the location of the output shapefile based on your AOI',default=None,widget="MultiFileChooser")
    parser_demaoi.set_defaults(func=demaoi_from_parser)

    parser_demsize=subparsers.add_parser('demsize',help='Allows users to estimate total download size and space left in your destination folder')
    parser_demsize.add_argument('--infile', help='Choose the clipped aoi file you clipped from demaoi tool[This is the subset of the master ArcticDEM Strip]',widget="MultiFileChooser")
    parser_demsize.add_argument('--path', help='Choose the destination folder where you want your dem files to be saved[This checks available disk space]',widget="MultiDirChooser")
    parser_demsize.set_defaults(func=demsize_from_parser)

    parser_demdownload=subparsers.add_parser('demdownload',help='Allows users to batch download ArcticDEM Strips using aoi shapefile')
    parser_demdownload.add_argument('--subset', help='Choose the location of the output shapefile based on your AOI[You got this from demaoi tool]',widget="MultiFileChooser")
    parser_demdownload.add_argument('--desination', help='Choose the destination where you want to download your files',widget="MultiDirChooser")
    parser_demdownload.set_defaults(func=demdownload_from_parser)

    parser_demextract=subparsers.add_parser('demextract',help='Allows users to extract both image and metadata files from the zipped tar files')
    parser_demextract.add_argument('--folder', help='Choose the download file where you downloaded your tar zipped files',widget="MultiDirChooser")
    parser_demextract.add_argument('--destination', help='Choose the destination folder where you want your images and metadata files to be extracted',widget="MultiDirChooser")
    parser_demextract.add_argument('--action', default="no",choices=['yes','no'],help='Choose if you want your zipped files to be deleted post extraction "yes"|"no"')
    parser_demextract.set_defaults(func=demextract_from_parser)

    parser_demmeta=subparsers.add_parser('demmeta',help='Tool to process metadata files into CSV for all strips[For use with Google Earth Engine]')
    parser_demmeta.add_argument('--folder', help='Choose where you unzipped and extracted your DEM and metadata files',widget="MultiDirChooser")
    parser_demmeta.add_argument('--metadata', help='Choose a path to the metadata file "example: users/desktop/metadata.csv"',widget="MultiFileChooser")
    parser_demmeta.add_argument('--error',help='Choose a path to the errorlog file "example: users/desktop/errorlog.csv"',widget="MultiFileChooser")
    parser_demmeta.set_defaults(func=demmeta_from_parser)

    args = parser.parse_args()


    args.func(args)

if __name__ == '__main__':
    main()
