import bpy
import os
import sys
import json
import platform
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src.main import config
importlib.reload(config)

listBatchFolder = os.listdir(config.batch_save_path)
numInBatchFolder = len(listBatchFolder)

removeList = [".gitignore", ".DS_Store", "Script_Ignore_Folder"]
batchList = [x for x in listBatchFolder if (x not in removeList)]


def checkIfBatchDup(i):
    file_name = os.path.join(config.batch_save_path, i)
    DataDictionary = json.load(open(file_name))

    nftsInBatch = DataDictionary["NFTs_in_Batch"]
    hierarchy = DataDictionary["hierarchy"]
    DNAList = DataDictionary["BatchDNAList"]



    def countDups(thelist):
        numOfDupDNA = 0
        seen = set()
        for x in thelist:
            if x in seen: numOfDupDNA += 1
            seen.add(x)
        return numOfDupDNA

    duplicates = countDups(DNAList)

    return duplicates


for i in batchList:
    print("\nThis is the duplication result for " + i + ":")
    print(checkIfBatchDup(i))
    print("\n")
