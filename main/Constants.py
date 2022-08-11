# Purpose:
# This file is for storing or updating constant values that may need to be changes depending on system requirements and
# different usecases.
import os
import json
import platform

removeList = [".gitignore", ".DS_Store", "desktop.ini", ".ini"]

def remove_file_by_extension(dirlist):
   """
   Checks if a given directory list contains any of the files or file extensions listed above, if so, remove them from
   list and return a clean dir list. These files interfer with BMNFTs operations and should be removed whenever dealing
   with directories.
   """

   if str(type(dirlist)) == "<class 'list'>":
       dirlist = list(dirlist)  # converts single string path to list if dir pasted as string

   return_dirs = []
   for directory in dirlist:
       if not str(os.path.split(directory)[1]) in removeList:
           return_dirs.append(directory)

   return return_dirs


class bcolors:
    """
    The colour of console messages.
    """

    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    ERROR = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR

def save_result(result):
    """
    Saves json result to json file at the specified path.
    """
    file_name =  "log.json"
    if platform.system() == "Linux" or platform.system() == "Darwin":
        path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop', file_name)

    if platform.system() == "Windows":
        path = os.path.join(os.environ["HOMEPATH"], "Desktop", file_name)

    data = json.dumps(result, indent=1, ensure_ascii=True)
    with open(path, 'w') as outfile:
        outfile.write(data + '\n')
