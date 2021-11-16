import bpy
import os
import sys
import timeit
import json
import random
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src.main import config
importlib.reload(config)

if config.runPreview:
   config.nftsPerBatch = config.maxNFTsTest
   config.maxNFTs = config.maxNFTsTest
   config.renderBatch = 1
   config.imageName = config.imageNameTest

def makeBatches():

      file_name = os.path.join(config.save_path, "NFTRecord.json")
      DataDictionary = json.load(open(file_name))

      numNFTsGenerated = DataDictionary["numNFTsGenerated"]
      hierarchy = DataDictionary["hierarchy"]
      DNAList = DataDictionary["DNAList"]

      numBatches = config.maxNFTs/config.nftsPerBatch

      print("To generate batches of " + str(config.nftsPerBatch) + " DNA sequences per batch, with a total of " +
            str(numNFTsGenerated) + " possible NFT DNA sequences, the number of batches generated will be " + str(numBatches))

      i = 0
      while i < numBatches:
            batchDictionary = {}
            BatchDNAList = []

            j = 0
            while j < config.nftsPerBatch:
                  oneDNA = random.choice(DNAList)
                  BatchDNAList.append(oneDNA)
                  DNAList.remove(oneDNA)
                  j += 1

            batchDictionary["NFTs_in_Batch"] = int(len(BatchDNAList))
            batchDictionary["hierarchy"] = hierarchy
            batchDictionary["BatchDNAList"] = BatchDNAList

            batchDictionaryObject = json.dumps(batchDictionary, indent=1, ensure_ascii=True)

            with open(config.batch_save_path + config.slash + ("Batch{}.json".format(i + 1)), "w") as outfile:
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

            with open(config.batch_save_path + config.slash + ("Batch{}.json".format(i + 1)), "w") as outfile2:
                  outfile2.write(incompleteBatch)

if __name__ == '__main__':
      makeBatches()