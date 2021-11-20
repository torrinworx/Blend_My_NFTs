import bpy
import os
import sys
import json
import platform
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src import config
importlib.reload(config)

def checkIfBatchDup(i):
    file_name = os.path.join(config.batch_save_path, i)
    DataDictionary = json.load(open(file_name))
    DNAList = DataDictionary["BatchDNAList"]

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
    listBatchFolder = os.listdir(config.batch_save_path)
    removeList = [".gitignore", ".DS_Store", "Script_Ignore_Folder"]
    batchList = [x for x in listBatchFolder if (x not in removeList)]

    for i in batchList:
        print( i + " has " + str(checkIfBatchDup(i)) + " duplicate NFT DNA.")

if __name__ == '__main__':
    checkDups()
