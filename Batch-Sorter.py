import bpy
import os
import sys

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)

import time
import json
import random
import conFig
import importlib
importlib.reload(conFig)
from conFig import *

time_start = time.time()

dnaPerBatch = 10

file_name = os.path.join(save_path, "NFTRecord.json")
ledger = json.load(open(file_name))

DataDictionary = ledger["1"]

numNFTsGenerated = DataDictionary["numNFTsGenerated"]
variantMetaData = DataDictionary["variantMetaData"]
DNAList = DataDictionary["DNAList"]
hierarchy = DataDictionary["hierarchy"]

remainder = numNFTsGenerated % dnaPerBatch
Number_Of_Possible_Batches = (numNFTsGenerated - remainder)/dnaPerBatch

print("To generate batches of " + str(dnaPerBatch) + " DNA sequences per batch, with a total of " +
      str(numNFTsGenerated) + " possible NFT DNA sequences, the number of batches generated will be " + str(Number_Of_Possible_Batches))
print("The number of remaining NFTs will be " + str(remainder) + " and total number accross all batches will be " + str(Number_Of_Possible_Batches*dnaPerBatch))

i = 0
while i < Number_Of_Possible_Batches:
      batchDictionary = {}
      BatchDNAList = []

      j = 0
      while j < dnaPerBatch:
            oneDNA = random.choice(DNAList)
            BatchDNAList.append(oneDNA)
            DNAList.remove(oneDNA)
            j += 1

      batchDictionary["NFTs_in_Batch"] = int(len(BatchDNAList))
      batchDictionary["hierarchy"] = hierarchy
      batchDictionary["variantMetaData"] = variantMetaData
      batchDictionary["BatchDNAList"] = BatchDNAList

      batchDictionaryObject = json.dumps(batchDictionary, indent=1, ensure_ascii=True)

      with open(json_save_path + ("/Batch{}.json".format(i+1)), "w") as outfile:
            outfile.write(batchDictionaryObject)

      i += 1

incompleteBatch = {}
incompleteBatch["NFTs_in_Batch"] = int(len(DNAList))
incompleteBatch["hierarchy"] = hierarchy
incompleteBatch["variantMetaData"] = variantMetaData
incompleteBatch["BatchDNAList"] = DNAList
incompleteBatch["hierarchy"] = hierarchy

incompleteBatch = json.dumps(incompleteBatch, indent=1, ensure_ascii=True)

with open(json_save_path + ("/Batch{}.json".format(i+1)), "w") as outfile2:
      outfile2.write(incompleteBatch)










