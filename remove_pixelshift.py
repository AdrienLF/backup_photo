import os
i= 0
for subdirs, dirs, files in os.walk("/Volumes/BackUp1"):

    for file in files:
        print(i)
        i += 1
        if "pixelshift".upper() in file.upper():
            print(subdirs+os.sep+file)
            os.remove(subdirs+os.sep+file)
