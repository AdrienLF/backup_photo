# coding: utf-8
import sys
sys.path.insert(1, "/Users/adrienlefalher/Dropbox/PYCHARM/")
import os
import shutil
from datetime import datetime
import hashlib
from Photo_Folder_Date import Check_file_continuity
from multiprocessing import Process
import time
import traceback
import concurrent.futures
from pathlib import Path
from pprint import pprint
sd_card = "/Volumes/Untitled"

filetypes = [".arw", ".mp4", ".xml", ".mov", ".dng"]
#filetypes = [".mp4", ".xml"]
i = 0

errors_dict = {}
error_count = 0
filecount = 0
files_done = []

def file_as_bytes(file):
	with file:
		return file.read()


test_mode = False
full_check = False
watch_folders = ["/Volumes/WdSSD", "/Volumes/SandiskSSD"]

created_folders = []

def backup_files(watch_folder, error_count, errors_dict, filecount, files_done):

	# Pas sur pour les global... A voir si ça compte pas en double.
	for dirs, subdirs, files in os.walk(sd_card):

		files_to_move = len(files)
		watch_folders = [watch_folder]


		filecount = 0

		for file in files:
			starttime = time.time()

			try:
				if any(str(ext).capitalize() in str(file).capitalize() for ext in filetypes) and not "MEDIAPRO" in str(file):
					print(str(filecount) + "/" + str(files_to_move))
					print(file)
					fullfilepath = Path(dirs).joinpath(file)
					creation_time = datetime.fromtimestamp(os.stat(fullfilepath).st_mtime)
					#print(hashlib.md5(file_as_bytes(open(fullfilepath,'rb'))).hexdigest())
					#print(creation_time)
					#print("\n")
					created_folders.append(str(watch_folder + os.sep + str(creation_time)).split(" ")[0]+os.sep)


					folder_date_format = f"{creation_time.year}-{creation_time.month}-{creation_time.day}"
					date_folder = Path(watch_folder).joinpath(folder_date_format)

					os.makedirs(date_folder, exist_ok=True)


					for watch_folder in watch_folders:
						#print("Watch folders : " + str(watch_folders))
						#print(f"Ligne 69 : watch folder is {watch_folder}")

						folder = str(watch_folder) + os.sep + str(creation_time).split(" ")[0]
						moved_file = folder + os.sep + file
						print(moved_file)
						if test_mode == True:
							original_hash = hashlib.md5(file_as_bytes(open(fullfilepath, 'rb'))).hexdigest()
							moved_file_hash = hashlib.md5(file_as_bytes(open(moved_file, 'rb'))).hexdigest()
							print("Original hash is {} and new hash is {}".format(original_hash, moved_file_hash))

						if not os.path.isfile(moved_file):
							try:
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
							except Exception as e:
								print(traceback.print_exc())
								error_count += 1
								errors_dict[moved_file] = e

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
							print("A file exists with that name. Checking...")

							# original_hash = hashlib.md5(file_as_bytes(open(fullfilepath, 'rb'))).hexdigest()
							# moved_file_hash = hashlib.md5(file_as_bytes(open(moved_file, 'rb'))).hexdigest()
							# if original_hash !=moved_file_hash:
							#     now = str(time.time()).split(".")[0]
							#     unique_filename = file.split(".")[-2]+str("_")+str(now)+"."+str(file.split(".")[-1])
							#     fullfilepath = dirs + os.sep + unique_filename
							#     shutil.copy2(fullfilepath, moved_file)
							#     original_hash = hashlib.md5(file_as_bytes(open(fullfilepath, 'rb'))).hexdigest()
							#     moved_file_hash = hashlib.md5(file_as_bytes(open(moved_file, 'rb'))).hexdigest()
							#
							#     print(
							#         "Original hash is {} and new hash is {}".format(original_hash, moved_file_hash))
							#     if original_hash == moved_file_hash:
							#         print("Move complete")
							# else:
							#     print("File already exists")






						print("Error count is {}".format(error_count))
						endtime = time.time()
						completetime = endtime - starttime
						print('Completed in ' + str(completetime))

						print(f"{completetime=}")
						print(f"{files_to_move=}")
						print(f"{filecount=}")
						restant = int(completetime) * (int(files_to_move)-int(filecount)) /60
						print("{} minutes restantes".format(restant))
						print("\n")


				files_done.append(file)

			except Exception as e:
				print(e)
				traceback.print_exc()
				error_count +=1
				errors_dict[file] = e
			filecount += 1
	return created_folders, error_count, errors_dict, filecount, files_done

if __name__ == '__main__':

	disk_list = ["/Volumes/WdSSD", "/Volumes/SandiskSSD"]

	for disk in disk_list:
		if not Path(disk).is_dir():
			disk_list.remove(disk)

	# We can use a with statement to ensure threads are cleaned up promptly
	with concurrent.futures.ThreadPoolExecutor() as executor:
		# Start the load operations and mark each future with its URL
		future_to_disk = {executor.submit(backup_files, disk, error_count, errors_dict, filecount, files_done): disk for disk in disk_list}
		for future in concurrent.futures.as_completed(future_to_disk):
			disk = future_to_disk[future]

			created_folders, error_count, errors_dict, filecount, files_done = future.result()
			print(f"{set(created_folders)}")
			print(f"{error_count} errors in {disk}")

			errors = errors_dict.values()
			print(len(errors))

			if error_count == 0:
				os.system(f"""say "Et voilà, j'ai fait du bon boulot. Il y a {error_count} erreurs dans le disque {disk}" """)
			else:
				os.system(
					f"""say "Holala. C'est n'importe quoi. Il y a {error_count} erreurs dans le disque {disk}" """)
			pprint(errors_dict)

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
		for folder in set(created_folders):
			#print(folder)
			try:
				Check_file_continuity.check_continuity(folder)
			except Exception as e:
				print(e)


