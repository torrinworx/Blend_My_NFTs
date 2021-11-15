import bpy
import os
import sys
import time
import json
import random
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src.main import config

importlib.reload(config)
from src.main.config import *

if config.runPreview:
   config.maxNFTs = config.maxNFTsTest
   config.renderBatch = 1
   config.imageName = config.imageNameTest

def makeBatches():

      file_name = os.path.join(save_path, "NFTRecord.json")
      DataDictionary = json.load(open(file_name))

      numNFTsGenerated = DataDictionary["numNFTsGenerated"]
      hierarchy = DataDictionary["hierarchy"]
      DNAList = DataDictionary["DNAList"]

      remainder = numNFTsGenerated % nftsPerBatch
      Number_Of_Possible_Batches = (numNFTsGenerated - remainder)/nftsPerBatch

      print("To generate batches of " + str(nftsPerBatch) + " DNA sequences per batch, with a total of " +
            str(numNFTsGenerated) + " possible NFT DNA sequences, the number of batches generated will be " + str(Number_Of_Possible_Batches))

      i = 0
      while i < Number_Of_Possible_Batches:
            batchDictionary = {}
            BatchDNAList = []

            j = 0
            while j < nftsPerBatch:
                  oneDNA = random.choice(DNAList)
                  BatchDNAList.append(oneDNA)
                  DNAList.remove(oneDNA)
                  j += 1

            batchDictionary["NFTs_in_Batch"] = int(len(BatchDNAList))
            batchDictionary["hierarchy"] = hierarchy
            batchDictionary["BatchDNAList"] = BatchDNAList

            batchDictionaryObject = json.dumps(batchDictionary, indent=1, ensure_ascii=True)

            with open(batch_save_path + slash + ("Batch{}.json".format(i + 1)), "w") as outfile:
                  outfile.write(batchDictionaryObject)

            i += 1

      if len(DNAList) > 0:
            print("One batch could not be filled completely and will contain " + str(len(DNAList)) + " NFTs.")

            incompleteBatch = {}

            incompleteBatch["NFTs_in_Batch"] = int(len(DNAList))
            incompleteBatch["hierarchy"] = hierarchy
            incompleteBatch["BatchDNAList"] = DNAList
            incompleteBatch["hierarchy"] = hierarchy

            incompleteBatch = json.dumps(incompleteBatch, indent=1, ensure_ascii=True)

            with open(batch_save_path + slash + ("Batch{}.json".format(i + 1)), "w") as outfile2:
                  outfile2.write(incompleteBatch)

if __name__ == '__main__':
      makeBatches()