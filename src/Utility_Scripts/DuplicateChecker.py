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