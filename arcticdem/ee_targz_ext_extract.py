import tarfile,sys,os
from glob import glob
import shutil
from glob import iglob
def demextract(directory=None,destination=None,delete=None):
    files=os.listdir(directory)
    if not os.path.exists(destination):
        os.makedirs(destination)
        os.makedirs(os.path.join(destination,"pgcdem"))
        os.makedirs(os.path.join(destination,"pgcmeta"))
        os.makedirs(os.path.join(destination,"pgcmt"))
    else:
        if not os.path.exists(os.path.join(destination,"pgcdem")):
            os.makedirs(os.path.join(destination,"pgcdem"))
        if not os.path.exists(os.path.join(destination,"pgcmeta")):
            os.makedirs(os.path.join(destination,"pgcmeta"))
        if not os.path.exists(os.path.join(destination,"pgcmt")):
            os.makedirs(os.path.join(destination,"pgcmt"))
    filesdem = os.listdir(os.path.join(destination,"pgcdem"))
    for fdem in filesdem:
        #print(os.path.join(destination,"pgcdem",fdem))
        os.remove(os.path.join(destination,"pgcdem",fdem))
    filesmeta = os.listdir(os.path.join(destination,"pgcmeta"))
    for fm in filesmeta:
        #print(os.path.join(destination,"pgcmeta",fm))
        os.remove(os.path.join(destination,"pgcmeta",fm))
    filesmt = os.listdir(os.path.join(destination,"pgcmt"))
    for fmt in filesmt:
        #print(os.path.join(destination,"pgcmeta",fm))
        os.remove(os.path.join(destination,"pgcmt",fmt))
    for fname in files:
        filepath=os.path.join(directory,fname)
        if (filepath.endswith("tar.gz")):
            tar = tarfile.open(filepath,'r:*')
            tar.extractall(destination)
            tar.close()
            print("Extracted in Current Directory")
        elif (filepath.endswith("tar")):
            tar=tarfile.open(filepath,'r:*')
            tar.extractall(destination)
            tar.close()
        else:
            print("Not a tar.gz file: '%s '")
    jp= [y for x in os.walk(destination) for y in glob(os.path.join(x[0], '*.tif'))]
    mf= [y for x in os.walk(destination) for y in glob(os.path.join(x[0], '*.txt'))]
    for mfd in mf:
        if mfd.count("mdf")!=1:
            os.unlink(mfd)
    tifcount= [y for x in os.walk(destination) for y in glob(os.path.join(x[0], '*.tif'))]
    mfcount= [y for x in os.walk(destination) for y in glob(os.path.join(x[0], '*.txt'))]
    indexfold=os.path.join(destination,"index")
    if os.path.exists(indexfold):
        shutil.rmtree(indexfold)
    for tifffile in tifcount:
        if tifffile.endswith("dem.tif"):
            basetif=os.path.basename(tifffile)
            shutil.move(tifffile, os.path.join(destination,"pgcdem",basetif))
    for tifffile in tifcount:
        if tifffile.endswith("matchtag.tif"):
            basetif=os.path.basename(tifffile)
            shutil.move(tifffile, os.path.join(destination,"pgcmt",basetif))
    for textfile in mfcount:
        basemeta=os.path.basename(textfile)
        shutil.move(textfile, os.path.join(destination,"pgcmeta",basemeta))
    if delete=="yes":
        tarcount=[y for x in os.walk(directory) for y in glob(os.path.join(x[0], '*.tar'))]+[y for x in os.walk(directory) for y in glob(os.path.join(x[0], '*.tar.gz'))]
        for tar in tarcount:
            os.unlink(tar)
    else:
        print("Extract Completed & Tar files not deleted")

if __name__ == '__main__':
    main() 
