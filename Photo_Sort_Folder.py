import os
import shutil

from datetime import datetime

watch_folders = ["/Volumes/BackUp1", "/Volumes/BackUp2"]
filetypes = [".arw", ".mp4", ".xml"]
i = 0

for watch_folder in watch_folders:
    for dirs, subdirs, files in sorted(os.walk(watch_folder)):
        if "2018" not in str(dirs):
            for file in sorted(files):
                    for filetype in filetypes:
                        try:
                            if str(filetype).capitalize() in str(file).capitalize():
                                print(file)
                                fullfilepath = dirs+os.sep+file
                                print(fullfilepath)
                                creation_time = datetime.fromtimestamp(os.stat(fullfilepath).st_mtime)
                                print(creation_time)

                                try:
                                    os.mkdir(str(watch_folder+ os.sep+str(creation_time)).split(" ")[0])
                                except Exception as e:
                                    print(e)
                                    pass
                                folder = watch_folder+ os.sep+str(creation_time).split(" ")[0]
                                print(folder+os.sep+file)
                                shutil.move(fullfilepath,folder+os.sep+file)
                        except Exception as e:
                            print(e)
                            pass


