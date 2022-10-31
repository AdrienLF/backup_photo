import os
import time
from datetime import datetime


filetypes = [".arw", ".mp4", ".xml"]
base_folder = "/Volumes/BackUp1/"

foldermode = True
if foldermode==True:
    for dirs, subdirs, files in os.walk(base_folder):
        for file in files:
            fileLocation = dirs + os.sep + file
            try:
                mois = fileLocation.split(os.sep)[3].split("-")[-2]
                if mois == "09" :
                    jour = fileLocation.split(os.sep)[3].split("-")[-1]
                    #print(jour)
                    if int(jour) < 23:
                        try:
                            if str(file).endswith(".ARW"):
                                print(fileLocation)

                                creation_time = datetime.fromtimestamp(os.stat(fileLocation).st_mtime)
                                print(creation_time)
                                creation_time = datetime.fromtimestamp(os.stat(fileLocation).st_ctime)
                                print(creation_time)
                                #creation_time = datetime.fromtimestamp(int(os.stat(fileLocation).st_mtime)+8*60*60)
                                #print(creation_time)
                                print('\n')

                                modTime = time.mktime(creation_time.timetuple())
                                #os.utime(fileLocation, (modTime, modTime))
                        except Exception as e:
                            print(e)
            except Exception as e:
                print(e)
else:
    for dirs, subdirs, files in os.walk("/Volumes/BackUp1/2018-09-23"):
        for file in sorted(files):
            if "DSC" in str(file):
                print(int(file.split(".")[0].replace("DSC", "")))
                if int(file.split(".")[0].replace("DSC", "")) < 7663 :

                    fileLocation = dirs + os.sep + file
                    try:

                        try:
                            if any(str(ext).capitalize() in str(file).capitalize() for ext in
                                   filetypes) and not "MEDIAPRO" in str(file):
                                print(fileLocation)

                                creation_time = datetime.fromtimestamp(os.stat(fileLocation).st_mtime)
                                print(creation_time)
                                creation_time = datetime.fromtimestamp(
                                    int(os.stat(fileLocation).st_mtime) + 8 * 60 * 60)
                                print(creation_time)
                                print('\n')

                                modTime = time.mktime(creation_time.timetuple())
                                #os.utime(fileLocation, (modTime, modTime))
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)