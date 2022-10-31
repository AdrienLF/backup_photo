import os
import shutil
from datetime import datetime
import hashlib
import Check_file_continuity
import time


sd_card = "/Volumes/Untitled"

filetypes = [".arw", ".mp4", ".xml"]
#filetypes = [".mp4", ".xml"]
i = 0

error_count = 0
filecount = 0
files_done = []

def file_as_bytes(file):
    with file:
        return file.read()


test_mode = False
full_check = False
watch_folders = ["/Volumes/BackUp1", "/Volumes/BackUp2"]

created_folders = []
for dirs, subdirs, files in os.walk(sd_card):
    files_to_move = len(files)
    watch_folders = ["/Volumes/BackUp1", "/Volumes/BackUp2"]


    for directory in dirs:
        filecount = 0

        for file in files:

            try:
                if any(str(ext).capitalize() in str(file).capitalize() for ext in filetypes) and not "MEDIAPRO" in str(file):
                    print(str(filecount) + "/" + str(files_to_move))
                    print(file)
                    fullfilepath = dirs + os.sep + file
                    creation_time = datetime.fromtimestamp(os.stat(fullfilepath).st_mtime)
                    #print(hashlib.md5(file_as_bytes(open(fullfilepath,'rb'))).hexdigest())
                    #print(creation_time)
                    #print("\n")
                    created_folders.append(str("/Volumes/BackUp1" + os.sep + str(creation_time)).split(" ")[0]+os.sep)
                    created_folders.append(str("/Volumes/BackUp2" + os.sep + str(creation_time)).split(" ")[0]+os.sep)

                    try:
                        os.mkdir(str("/Volumes/BackUp1" + os.sep + str(creation_time)).split(" ")[0])
                        os.mkdir(str("/Volumes/BackUp2" + os.sep + str(creation_time)).split(" ")[0])

                    except Exception as e:

                        pass

                    for watch_folder in watch_folders:
                        folder = watch_folder + os.sep + str(creation_time).split(" ")[0]
                        moved_file = folder + os.sep + file
                        print(moved_file)
                        if test_mode == True:
                            original_hash = hashlib.md5(file_as_bytes(open(fullfilepath, 'rb'))).hexdigest()
                            moved_file_hash = hashlib.md5(file_as_bytes(open(moved_file, 'rb'))).hexdigest()
                            print("Original hash is {} and new hash is {}".format(original_hash, moved_file_hash))

                        if not os.path.isfile(moved_file):

                            shutil.copy2(fullfilepath, moved_file)
                            original_hash = hashlib.md5(file_as_bytes(open(fullfilepath, 'rb'))).hexdigest()
                            moved_file_hash = hashlib.md5(file_as_bytes(open(moved_file, 'rb'))).hexdigest()

                            print("Original hash is {} and new hash is {}".format(original_hash, moved_file_hash))
                            if original_hash == moved_file_hash:
                                print("Move complete")
                            else:
                                print("Error on move")
                                error_count += 1
                                with open(watch_folder + os.sep + "Error_log.txt", "a") as error_log_file:
                                    error_log_file.write(
                                        str(datetime.now()) + " " + "Original hash is {} and new hash is {} \n".format(
                                            original_hash, moved_file_hash))
                                    error_log_file.write(str(file) + "\n")

                                ####### CORRECTION DU FICHIER CORROMPU
                                print('Trying to correct things')
                                print(moved_file)
                                os.remove(moved_file)
                                shutil.copy2(fullfilepath, moved_file)

                                print("Original hash is {} and new hash is {}".format(original_hash, moved_file_hash))
                                if original_hash == moved_file_hash:
                                    print("Move complete")
                                else:
                                    print("Error AGAIN on move")
                                    error_count += 1
                                    with open(watch_folder + os.sep + "Error_log.txt", "a") as error_log_file:
                                        error_log_file.write(
                                            str(
                                                datetime.now()) + " " + "Original hash is {} and new hash is {} \n".format(
                                                original_hash, moved_file_hash))
                                        error_log_file.write(str(file) + "\n")
                        else:
                            print("File already exists")



                        print("Error count is {}".format(error_count))
                        print("\n")
                files_done.append(file)

            except Exception as e:
                print(e)
            filecount += 1

created_folders = list(set(created_folders))
print(created_folders)
print("\n")
if full_check == True:
    for watch_folder in watch_folders:
        for dirs, subdirs, files in os.walk(watch_folder):
            for directory in subdirs:
                if '2018' in str(directory):
                    print(directory)
                    try:
                        Check_file_continuity.check_continuity(watch_folder+os.sep+directory)
                    except Exception as e:
                        print(e)
else:
    for folder in created_folders:
        print(folder)
        try:
            Check_file_continuity.check_continuity(folder)
        except Exception as e:
            print(e)