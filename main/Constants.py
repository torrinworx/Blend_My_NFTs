# Purpose:
# This file is for storing or updating constant values that may need to be changes depending on system requirements and
# different usecases.
import os


removeList = [".gitignore", ".DS_Store", "desktop.ini", ".ini"]

def remove_file_by_extension(dirlist):
    """
    Checks if a given directory list contains any of the files or file extensions listed above, if so, remove them from
    list and return a clean dir list. These files interfer with BMNFTs operations and should be removed whenever dealing
    with directories.
    """

    return_dirs = []
    for directory in dirlist:
        if not str(os.path.splitext(directory)[1]) in removeList:
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

