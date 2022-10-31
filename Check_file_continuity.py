import os
import re

def check_continuity(folder):
    print("Checking folder {}".format(folder))
    file_list = []
    #for file in os.listdir(folder):
    # for subdirs, dirs, files in os.walk(folder):
    for subdirs, dirs, files in os.walk(folder):
        for file in files:
            if str(file).endswith(".ARW"):
                file_list.append(os.path.join(subdirs, file))

    if len(file_list) > 0:
        min_file = min(file_list)
        max_file = max(file_list)
        print(min_file, max_file)


        regex = r"\d+"

        min_file_int = int(re.findall(regex, min_file, re.MULTILINE)[0])

        max_file_int = int(re.findall(regex, max_file, re.MULTILINE)[0])

        file_dif = (max_file_int-min_file_int)
        print("There should be {} files".format(max_file_int - min_file_int))

        file_count = -1
        for file in file_list:
            file_count+=1
        print(str(file_count) + " files counted")

    if file_count != file_dif:
        i = 0
        old_file=str()
        new_file=str()
        for file in sorted(file_list):
            file_int = int(re.findall(regex, file, re.MULTILINE)[0])
            new_file = file_int
            if i > 0:
                if new_file != old_file+1:
                    print("File missing between {} and {}".format(old_file, new_file))
            i+=1
            old_file=file_int
        print("\n")
    else:
        print('No problem, Sir!\n')
    #print("File counting done\n")




if __name__ == "__main__":

    watch_folders = ["/Volumes/WdSSD", "/Volumes/SandiskSSD"]
    for folder in watch_folders:
        check_continuity(folder)