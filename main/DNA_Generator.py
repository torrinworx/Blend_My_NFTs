# Purpose:
# This file generates NFT DNA based on a .blend file scene structure and exports NFTRecord.json.

import bpy
import os
import re
import copy
import time
import json
import random
import importlib
from functools import partial

from . import Rarity, Logic, Checks
importlib.reload(Rarity)
importlib.reload(Logic)
importlib.reload(Checks)

class bcolors:
   """
   The colour of console messages.
   """
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR


def returnData(maxNFTs, nftsPerBatch):
   """
   Generates important variables, dictionaries, and lists needed to be stored to catalog the NFTs.
   :return: listAllCollections, attributeCollections, attributeCollections1, hierarchy, variantMetaData, possibleCombinations
   """

   coll = bpy.context.scene.collection

   scriptIgnore = Checks.raise_Error_ScriptIgnore()

   listAllCollInScene = []
   listAllCollections = []

   def traverse_tree(t):
      yield t
      for child in t.children:
         yield from traverse_tree(child)

   for c in traverse_tree(coll):
      listAllCollInScene.append(c)

   for i in listAllCollInScene:
      listAllCollections.append(i.name)

   listAllCollections.remove(scriptIgnore.name)

   if "Scene Collection" in listAllCollections:
      listAllCollections.remove("Scene Collection")

   if "Master Collection" in listAllCollections:
      listAllCollections.remove("Master Collection")

   def allScriptIgnore(scriptIgnore):
      """
      Removes all collections, sub collections in Script_Ignore collection from listAllCollections.
      """
      for coll in list(scriptIgnore.children):
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
      """
      Creates a dictionary of each attribute
      """
      allAttDataList = {}
      count = 0
      previousAttribute = ""
      for i in attributeVariants:

         def getName(i):
            """
            Returns the name of "i" attribute variant
            """
            name = i.split("_")[0]
            return name

         def getOrder_rarity(i):
            """
            Returns the "order" and "rarity" (if enabled) of i attribute variant in a list
            """
            x = re.sub(r'[a-zA-Z]', "", i)
            a = x.split("_")
            del a[0]
            return list(a)

         name = getName(i)
         orderRarity = getOrder_rarity(i)

         number = orderRarity[0]
         rarity = orderRarity[1]

         eachObject = {"name": name, "number": number, "rarity": rarity}
         allAttDataList[i] = eachObject
      return allAttDataList

   variantMetaData = attributeData(attributeVariants)

   def getHierarchy():
      """
      Constructs the hierarchy dictionary from attributeCollections1 and variantMetaData.
      """
      hierarchy = {}
      for i in attributeCollections1:
         colParLong = list(bpy.data.collections[str(i)].children)
         colParShort = {}
         for x in colParLong:
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
      """
      Returns "combinations" the number of all possible NFT combinations.
      """

      hierarchyByNum = []

      for i in hierarchy:
         # Ignore Collections with nothing in them
         if len(hierarchy[i]) != 0:
            hierarchyByNum.append(len(hierarchy[i]))
         else:
            print(f"The following collection has been identified as empty: {i}")

      combinations = 1
      for i in hierarchyByNum:
         combinations = combinations*i

      # Checks:
      numBatches = Checks.raise_Error_numBatches(maxNFTs, nftsPerBatch)

      Checks.raise_Error_ZeroCombinations(combinations)

      Checks.raise_Error_numBatchesGreaterThan(numBatches)

      Checks.raise_Error_numBatchesGreaterThan(numBatches)

      return combinations

   possibleCombinations = numOfCombinations(hierarchy)

   return listAllCollections, attributeCollections, attributeCollections1, hierarchy, possibleCombinations

def generateNFT_DNA(maxNFTs, nftsPerBatch, logicFile, enableRarity, enableLogic):
   """
   Returns batchDataDictionary containing the number of NFT combinations, hierarchy, and the DNAList.
   """

   listAllCollections, attributeCollections, attributeCollections1, hierarchy, possibleCombinations = returnData(maxNFTs, nftsPerBatch)

   # DNA random, Rarity and Logic methods:
   DataDictionary = {}

   def createDNArandom():
      """Creates a single DNA randomly without Rarity or Logic."""
      dnaStr = ""
      dnaStrList = []
      listOptionVariant = []

      for i in hierarchy:
         numChild = len(hierarchy[i])
         possibleNums = list(range(1, numChild + 1))
         listOptionVariant.append(possibleNums)

      for i in listOptionVariant:
         randomVariantNum = random.choices(i, k=1)
         str1 = ''.join(str(e) for e in randomVariantNum)
         dnaStrList.append(str1)

      for i in dnaStrList:
         num = "-" + str(i)
         dnaStr += num

      dna = ''.join(dnaStr.split('-', 1))

      return str(dna)

   def singleCompleteDNA():
      """This function applies Rarity and Logic to a single DNA created by createDNASingle() if Rarity or Logic specified"""
      singleDNA = ""
      if not enableRarity:
         singleDNA = createDNArandom()
      # print("============")
      if enableRarity:
         singleDNA = Rarity.createDNArarity(hierarchy)
      # print(f"Rarity DNA: {singleDNA}")

      if enableLogic:
         singleDNA = Logic.logicafyDNAsingle(hierarchy, singleDNA, logicFile)
      # print(f"Logic DNA: {singleDNA}")
      # print("============\n")
      return singleDNA

   def create_DNAList():
      """Creates DNAList. Loops through createDNARandom() and applies Rarity, and Logic while checking if all DNA are unique"""
      DNASetReturn = set()

      for i in range(maxNFTs):
         dnaPushToList = partial(singleCompleteDNA)

         DNASetReturn |= {''.join([dnaPushToList()]) for _ in range(maxNFTs - len(DNASetReturn))}

      DNAListReturn = list(DNASetReturn)

      return DNAListReturn

   DNAList = create_DNAList()

   # Messages:
   if len(DNAList) < maxNFTs:
      print(f"{bcolors.ERROR} \nWARNING: \n"
            f"You are seeing this warning because the program cannot generate {maxNFTs} NFTs with rarity enabled. "
            f"Only {len(DNAList)} NFT DNA were generated."
            f"Either A) Lower the number of NFTs you wish to create, or B) Increase the maximum number of possible NFTs by"
            f" creating more variants and attributes in your .blend file.{bcolors.RESET}")

   # Data stored in batchDataDictionary:
   DataDictionary["numNFTsGenerated"] = len(DNAList)
   DataDictionary["hierarchy"] = hierarchy
   DataDictionary["DNAList"] = DNAList

   return DataDictionary, possibleCombinations

def send_To_Record_JSON(maxNFTs, nftsPerBatch, save_path, enableRarity, enableLogic, logicFile, Blend_My_NFTs_Output):
   """
   Creates NFTRecord.json file and sends "batchDataDictionary" to it. NFTRecord.json is a permanent record of all DNA
   you've generated with all attribute variants. If you add new variants or attributes to your .blend file, other scripts
   need to reference this .json file to generate new DNA and make note of the new attributes and variants to prevent
   repeate DNA.
   """

   # Messages:
   print(
      f"\n========================================\n"
      f"Creating NFT Data. Generating {maxNFTs} NFT DNA.\n"
   )

   if not enableRarity and not enableLogic:
      print(f"{bcolors.OK}NFT DNA will be determined randomly, no special properties or parameters are applied.\n{bcolors.RESET}")

   if enableRarity:
      print(f"{bcolors.OK}Rarity is ON. Weights listed in .blend scene will be taken into account.\n{bcolors.RESET}")

   if enableLogic:
      print(f"{bcolors.OK}Logic is ON. Rules listed in {logicFile} will be taken into account.\n{bcolors.RESET}")

   time_start = time.time()
   def create_nft_data():
      DataDictionary, possibleCombinations = generateNFT_DNA(maxNFTs, nftsPerBatch, logicFile, enableRarity, enableLogic)
      NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")

      # Checks:
      Checks.raise_Warning_maxNFTs(nftsPerBatch, maxNFTs)

      Checks.check_Rarity(DataDictionary["hierarchy"], DataDictionary["DNAList"], os.path.join(save_path, "Blend_My_NFTs Output/NFT_Data"))

      Checks.check_Duplicates(DataDictionary["DNAList"])

      try:
         ledger = json.dumps(DataDictionary, indent=1, ensure_ascii=True)
         with open(NFTRecord_save_path, 'w') as outfile:
            outfile.write(ledger + '\n')

         print(
            f"\n{bcolors.OK}Blend_My_NFTs Success:\n"
            f"{len(DataDictionary['DNAList'])} NFT DNA saved to {NFTRecord_save_path}. NFT DNA Successfully created.\n{bcolors.RESET}")

      except:
         raise (
            f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
            f"Data not saved to NFTRecord.json. Please review your Blender scene and ensure it follows "
            f"the naming conventions and scene structure. For more information, "
            f"see:\n{bcolors.RESET}"
            f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
         )
      return True

   # Loading Animations:
   bar = [
      " [=     ]",
      " [ =    ]",
      " [  =   ]",
      " [   =  ]",
      " [    = ]",
      " [     =]",
      " [    = ]",
      " [   =  ]",
      " [  =   ]",
      " [ =    ]",
   ]
   i = 0

   while not create_nft_data():
      print(bar[i % len(bar)], end="\r")
      time.sleep(.2)
      i += 1

   time_end = time.time()

   print(
      f"Created NFT Data in {time_end - time_start}s.\n"
   )


if __name__ == '__main__':
   send_To_Record_JSON()
