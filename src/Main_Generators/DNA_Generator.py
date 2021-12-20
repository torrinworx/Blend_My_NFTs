# Purpose:
# This file generates NFT DNA based on a .blend file scene structure and exports NFTRecord.json.

import bpy
import os
import re
import sys
import copy
import time
import json
import random
import importlib
from functools import partial

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src import config
from src.Main_Generators import Rarity_Sorter

importlib.reload(config)
importlib.reload(Rarity_Sorter)


if config.runPreview:
   config.nftsPerBatch = config.maxNFTsTest
   config.maxNFTs = config.maxNFTsTest
   config.renderBatch = 1
   config.nftName = "TestImages"

class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR

time_start = time.time()

print("")

def stripColorFromName(name):
   return "_".join(name.split("_")[:-1])

def returnData():
   '''
   Generates important variables, dictionaries, and lists needed to be stored to catalog the NFTs.
   :return: listAllCollections, attributeCollections, attributeCollections1, hierarchy, variantMetaData, possibleCombinations
   '''

   coll = bpy.context.scene.collection

   try:
      scriptIgnore = bpy.data.collections["Script_Ignore"]
   except:
      print(bcolors.ERROR + "ERROR:\nScript_Ignore collection is not in .blend file scene. Please add the Script_Ignore collection to your "
            ".blend file scene. For more information, read the README.md file.\n"+ bcolors.RESET)

   listAllCollInScene = []
   listAllCollections = []

   def traverse_tree(t):
      yield t
      for child in t.children:
         yield from traverse_tree(child)

   for c in traverse_tree(coll):
      listAllCollInScene.append(c)

   def listSubIgnoreCollections():
      def getParentSubCollections(collection):
         yield collection
         for child in collection.children:
            yield from getParentSubCollections(child)

      collList = []
      for c in getParentSubCollections(scriptIgnore):
         collList.append(c.name)
      return collList

   ignoreList = listSubIgnoreCollections()

   for i in listAllCollInScene:
      if config.enableGeneration:
         if i.name in config.colorList:
            for j in range(len(config.colorList[i.name])):
               if i.name[-1].isdigit() and i.name not in ignoreList:
                  listAllCollections.append(i.name + "_" + str(j + 1))
               elif j == 0:
                  listAllCollections.append(i.name)
         elif i.name[-1].isdigit() and i.name not in ignoreList:
            listAllCollections.append(i.name + "_0")
         else:
            listAllCollections.append(i.name)
      else:
         listAllCollections.append(i.name)

   listAllCollections.remove(scriptIgnore.name)

   if "Scene Collection" in listAllCollections:
      listAllCollections.remove("Scene Collection")

   if "Master Collection" in listAllCollections:
      listAllCollections.remove("Master Collection")

   def allScriptIgnore(collection):
      '''
      Removes all collections, sub collections in Script_Ignore collection from listAllCollections.
      '''
      for coll in list(collection.children):
         listAllCollections.remove(coll.name)
         listColl = list(coll.children)
         if len(listColl) > 0:
            allScriptIgnore(coll)

   allScriptIgnore(scriptIgnore)
   listAllCollections.sort()

   exclude = ["_", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
   attributeCollections = copy.deepcopy(listAllCollections)

   def filter_num():
      """
      This function removes items from 'attributeCollections' if they include values from the 'exclude' variable.
      It removes child collections from the parent collections in from the "listAllCollections" list.
      """
      for x in attributeCollections:
         if any(a in x for a in exclude):
            attributeCollections.remove(x)

   for i in range(len(listAllCollections)):
       filter_num()

   attributeVariants = [x for x in listAllCollections if x not in attributeCollections]
   attributeCollections1 = copy.deepcopy(attributeCollections)

   def attributeData(attributeVariants):
      '''
      Creates a dictionary of each attribute
      '''
      allAttDataList = {}
      count = 0
      previousAttribute = ""
      for i in attributeVariants:

         def getName(i):
            '''
            Returns the name of "i" attribute variant
            '''
            name = re.sub(r'[^a-zA-Z]', "", i)
            return name

         def getOrder_rarity(i):
            '''
            Returns the "order", "rarity" and "color" (if enabled) of i attribute variant in a list
            '''
            x = re.sub(r'[a-zA-Z]', "", i)
            a = x.split("_")
            del a[0]
            return list(a)

         name = getName(i)
         orderRarity = getOrder_rarity(i)

         if len(orderRarity) == 0:
            print(bcolors.ERROR + "\nERROR:" + bcolors.RESET)
            print("The collection " + str(i) + " doesn't follow the naming conventions of attributes. Please move this \n"
                  "colleciton to Script_Ignore or review proper collection format in README.md")
            return

         elif len(orderRarity) > 0:
            number = orderRarity[0]
            if config.enableGeneration:
               if count == 1 or count == 0:
                  previousAttribute = i.partition("_")[0]
                  count +=1
               elif i.partition("_")[0] == previousAttribute:
                  count +=1
               else:
                  count = 1
               number = str(count)
            rarity = orderRarity[1]
            if config.enableGeneration and stripColorFromName(i) in config.colorList:
               color = orderRarity[2]
            else:
               color = "0"
            eachObject = {"name": name, "number": number, "rarity": rarity, "color": color}
            allAttDataList[i] = eachObject
      return allAttDataList

   variantMetaData = attributeData(attributeVariants)

   def getHierarchy():
      '''
      Constructs the hierarchy dictionary from attributeCollections1 and variantMetaData.
      '''
      hierarchy = {}
      for i in attributeCollections1:
         colParLong = list(bpy.data.collections[str(i)].children)
         colParShort = {}
         for x in colParLong:
            if config.enableGeneration:
               '''
               Append colors to blender name for PNG generator and NFTRecord.json to create the correct list
               '''
               if x.name in config.colorList:
                  for j in range(len(config.colorList[x.name])):
                     colParShort[x.name + "_" + str(j+1)] = None
               else:
                  colParShort[x.name + "_0"] = None
            else:
               colParShort[x.name] = None
         hierarchy[i] = colParShort

      for a in hierarchy:
         for b in hierarchy[a]:
            for x in variantMetaData:
               if str(x) == str(b):
                  (hierarchy[a])[b] = variantMetaData[x]

      return hierarchy

   hierarchy = getHierarchy()

   def numOfCombinations(hierarchy):
      '''
      Returns "combinations" the number of all possible NFT combinations.
      '''
      hierarchyByNum = []
      for i in hierarchy:
         # Ignore Collections with nothing in them
         if len(hierarchy[i]) != 0:
            hierarchyByNum.append(len(hierarchy[i]))
         else:
            print("The following collection has been identified as empty:")
            print(i)
      combinations = 1
      for i in hierarchyByNum:
         combinations = combinations*i

      if combinations == 0:
         print(bcolors.ERROR + "\nERROR:" + bcolors.RESET)
         print("The number of all possible combinations is equal to 0. Please review your collection hierarchy \n "
               "and ensure it is formatted correctly.")
         print("Please review README.md for more information.")
         print("")
         print("Here is the hierarchy of all collections the DNA_Generator gathered from your .blend file, excluding "
               "\nthose in Script_Ignore:")
         print(hierarchy)

      numBatches = combinations/config.nftsPerBatch

      if numBatches < 1:
         print(bcolors.ERROR + "ERROR:" + bcolors.RESET)
         print("The number of NFTs Per Batch (nftsPerBatch variable in config.py) is to high.")
         print("There are a total of " + str(combinations) + " possible NFT combinations and you've requested "
               + str(config.nftsPerBatch) + " NFTs per batch.")
         print("Lower the number of NFTs per batch in config.py or increase the number of \nattributes and/or variants"
               " in your .blend file.")

      return combinations

   possibleCombinations = numOfCombinations(hierarchy)

   for i in variantMetaData:
      def cameraToggle(i, toggle=True):
         if config.enableGeneration:
            '''
            Remove Color code so blender recognises the collection
            '''
            i = stripColorFromName(i)
         bpy.data.collections[i].hide_render = toggle
         bpy.data.collections[i].hide_viewport = toggle
      cameraToggle(i)

   return listAllCollections, attributeCollections, attributeCollections1, hierarchy, possibleCombinations

def generateNFT_DNA():
   '''
   Returns batchDataDictionary containing the number of NFT cominations, hierarchy, and the DNAList.
   '''

   listAllCollections, attributeCollections, attributeCollections1, hierarchy, possibleCombinations = returnData()

   print("-----------------------------------------------------------------------------")
   print("The number of possible DNA combinations is " + str(possibleCombinations))
   print("")
   print("Generating " + str(config.maxNFTs) + " combinations of DNA. Set in config.py.")
   print("")

   DataDictionary = {}
   listOptionVariant = []
   DNAList = []

   if not config.enableRarity:
      DNASet = set()

      for i in hierarchy:
         numChild = len(hierarchy[i])
         possibleNums = list(range(1, numChild + 1))
         listOptionVariant.append(possibleNums)

      def createDNARandom():
         dnaStr = ""
         dnaStrList = []

         for i in listOptionVariant:
            randomVariantNum = random.choices(i, k = 1)
            str1 = ''.join(str(e) for e in randomVariantNum)
            dnaStrList.append(str1)

         for i in dnaStrList:
            num = "-" + str(i)
            dnaStr += num

         dna = ''.join(dnaStr.split('-', 1))

         return str(dna)

      for i in range(config.maxNFTs):
         dnaPushToList = partial(createDNARandom)

         DNASet |= {''.join([dnaPushToList()]) for _ in range(config.maxNFTs - len(DNASet))}

      DNAList = list(DNASet)

      possibleCombinations = config.maxNFTs

      if config.nftsPerBatch > config.maxNFTs:
         print(bcolors.WARNING + "\nWARNING:" + bcolors.RESET)
         print("The Max num of NFTs you chose is smaller than the NFTs Per Batch you set. Only " + str(config.maxNFTs) + " were added to 1 batch")

   if config.enableRarity:
      print(bcolors.OK + "Rarity is on. Weights listed in .blend will be taken into account " + bcolors.RESET)
      possibleCombinations = config.maxNFTs
      DNAList = Rarity_Sorter.sortRarityWeights(hierarchy, listOptionVariant, DNAList)

   if len(DNAList) < config.maxNFTs:
      print(f"{bcolors.ERROR} \nWARNING: \n"
            f"You are seeing this warning because the program cannot generate {config.maxNFTs} NFTs with rarity enabled. "
            f"Only {len(DNAList)} NFT DNA were generated."
            f"Either A) Lower the number of NFTs you wish to create, or B) Increase the maximum number of possible NFTs by"
            f" creating more variants and attributes in your .blend file.{bcolors.RESET}")

   # Data stored in batchDataDictionary:
   DataDictionary["numNFTsGenerated"] = len(DNAList)
   DataDictionary["hierarchy"] = hierarchy
   DataDictionary["DNAList"] = DNAList

   return DataDictionary, possibleCombinations

def send_To_Record_JSON():
   '''
   Creates NFTRecord.json file and sends "batchDataDictionary" to it. NFTRecord.json is a permanent record of all DNA
   you've generated with all attribute variants. If you add new variants or attributes to your .blend file, other scripts
   need to reference this .json file to generate new DNA and make note of the new attributes and variants to prevent
   repeate DNA.
   '''

   DataDictionary, possibleCombinations = generateNFT_DNA()

   ledger = json.dumps(DataDictionary, indent=1, ensure_ascii=True)
   with open(os.path.join(config.save_path, "NFTRecord.json"), 'w') as outfile:
      outfile.write(ledger + '\n')

   print("")
   print("All possible combinations of DNA sent to NFTRecord.json with " + str(possibleCombinations) + " NFT DNA sequences generated in %.4f seconds" % (time.time() - time_start))
   print("")
   print("If you want the number of NFT DNA sequences to be higher, please add more variants or attributes to your .blend file")
   print("")

# Utility functions:

# ONLY FOR TESTING, DO NOT EVER USE IF NFTRecord.json IS FULL OF REAL DATA
# THIS WILL DELETE THE RECORD:
# Note - NFTRecrod.json will be created the next time you run main.py
def clearNFTRecord(AREYOUSURE):
   if AREYOUSURE == True:
      os.remove("NFTRecord.json")

# clearNFTRecord()

if __name__ == '__main__':
   stripColorFromName()
   returnData()
   send_To_Record_JSON()
   clearNFTRecord()