# Purpose:
# This file checks NFTRecord for duplicate NFT DNA and returns any found in the console.

# Note - This file is provided for transparency, it is impossible for duplicates to be made with the current code in
# DNA_Generator.py.

import bpy
import os
import sys
import json
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src import config

importlib.reload(config)

class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR

def checkIfBatchDup():
    file_name = os.path.join(config.save_path, "NFTRecord.json")
    DataDictionary = json.load(open(file_name))
    DNAList = DataDictionary["DNAList"]

    def countDups(thelist):
        numOfDupDNA = 0
        seen = set()
        for x in thelist:
            if x in seen:
                print(x)
                numOfDupDNA += 1
            seen.add(x)
        return numOfDupDNA
    duplicates = countDups(DNAList)
    return duplicates

def checkDups():
    print("NFTRecord.json contains " + str(checkIfBatchDup()) + " duplicate NFT DNA.")

if __name__ == '__main__':
    checkDups()
