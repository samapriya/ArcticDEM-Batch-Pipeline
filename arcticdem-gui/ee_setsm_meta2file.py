import csv
from itertools import islice
import os
from glob import glob
import time
def demmeta(folder,mfile,errorlog):
    metasource = [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.txt'))]
    with open(mfile,'wb') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "platform", "catId1","catId2", "noDataValue", "releaseVersion", "srcImg1","srcImg2","setsmVersion","resolution","bitdepth","acqDate","minelv","maxelv","units"], delimiter=',')
        writer.writeheader()
    with open(errorlog,'wb') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
        writer.writeheader()
    for files in metasource:
        print(files)
        with open(files,'r') as myfile:
            a=myfile.readlines()
            try:
                demid=str(a).split('stripDemId = "')[1].split('v2.0";')[0]+"v20_dem"
                platform=str(a).split('platform = "')[1].split('";')[0]
                catId1 = str(a).split('catId1 = "')[1].split('";')[0]
                catId2 = str(a).split('catId2 = "')[1].split('";')[0]
                noDataValue = str(a).split('noDataValue = ')[1].split(';')[0]
                date_time = str(a).split('stripCreationTime = ')[1].split('T')[0]
                rls=str(a).split('releaseVersion = "')[1].split('";')[0]
                sim=str(a).split('sourceImage1 = "')[1].split('";')[0]
                sim2=str(a).split('sourceImage2 = "')[1].split('";')[0]
                setv=str(a).split('setsmVersion = ')[1].split(';')[0]
                rs=str(a).split('outputResolution = ')[1].split(';')[0]
                bp=str(a).split('bitsPerPixel = ')[1].split(';')[0]
                acq=str(a).split('acqDate = ')[1].split(';')[0]
                minelv=str(a).split('minElevValue = ')[1].split(';')[0]
                maxelv=str(a).split('maxElevValue = ')[1].split(';')[0]
                units=str(a).split('horizontalCoordSysUnits = "')[1].split('";')[0]
                pattern = '%Y-%m-%d'
                epoch = int(time.mktime(time.strptime(date_time, pattern)))*1000
                acqtime=int(time.mktime(time.strptime(acq, pattern)))*1000
                print("DEM ID",demid)
                print("Platform",platform)
                print("Acquisition Time",acqtime)
                print("Strip Creation Time",epoch)
                print('CatID1',catId1)
                print('CatID2',catId2)
                print("noDataValue",noDataValue)
                print("Release Version",rls)
                print("SourceImage 1",sim)
                print('SourceImage 2',sim2)
                print('SETSM Version',setv)
                print("BitsPerPixel",bp)
                print("Unit",units)
                print("Minimum Elevation",format(float(minelv),'.2f'))
                print("Maximum Elevation",format(float(maxelv),'.2f'))
                print("Output Resolution",format(float(rs),'.2f'))
                with open(mfile,'a') as csvfile:
                    writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                    writer.writerow([demid,epoch,platform,catId1,catId2,noDataValue,rls,sim,sim2,setv,format(float(rs),'.2f'),bp,acqtime,format(float(minelv),'.2f'),format(float(maxelv),'.2f'),units])
                csvfile.close()
            except Exception:
                print(infilename)
                with open(errorlog,'a') as csvfile:
                    writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                    writer.writerow([infilename])
                csvfile.close()

if __name__ == '__main__':
    main()
