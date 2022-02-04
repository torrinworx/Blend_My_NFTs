import bpy
import re
import copy

enableGeneration = False
colorList = []

class bcolors:
   """
   The colour of console messages.
   """
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR

def stripColorFromName(name):
   return "_".join(name.split("_")[:-1])

def get_combinations_from_scene():
   """
   Generates important variables, dictionaries, and lists needed to be stored to catalog the NFTs.
   :return: listAllCollections, attributeCollections, attributeCollections1, hierarchy, variantMetaData, possibleCombinations
   """

   coll = bpy.context.scene.collection

   try:
      scriptIgnore = bpy.data.collections["Script_Ignore"]
   except:
      print(f"{bcolors.ERROR} ERROR:\nScript_Ignore collection is not in .blend file scene. Please add the Script_Ignore collection to your "
            f".blend file scene. For more information, read the README.md file.\n {bcolors.RESET}")

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
      if enableGeneration:
         if i.name in colorList:
            for j in range(len(colorList[i.name])):
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
            Returns the "order", "rarity" and "color" (if enabled) of i attribute variant in a list
            """
            x = re.sub(r'[a-zA-Z]', "", i)
            a = x.split("_")
            del a[0]
            return list(a)

         name = getName(i)
         orderRarity = getOrder_rarity(i)

         if len(orderRarity) == 0:
            print(f"{bcolors.ERROR} \nERROR: {bcolors.RESET}")
            print(f"The collection {i} doesn't follow the naming conventions of attributes. Please move this \n"
                  "colleciton to Script_Ignore or review proper collection format in README.md")
            return

         elif len(orderRarity) > 0:
            number = orderRarity[0]
            if enableGeneration:
               if count == 1 or count == 0:
                  previousAttribute = i.partition("_")[0]
                  count +=1
               elif i.partition("_")[0] == previousAttribute:
                  count +=1
               else:
                  count = 1
               number = str(count)
            rarity = orderRarity[1]
            if enableGeneration and stripColorFromName(i) in colorList:
               color = orderRarity[2]
            else:
               color = "0"
            eachObject = {"name": name, "number": number, "rarity": rarity, "color": color}
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
            if enableGeneration:
               """
               Append colors to blender name for PNG generator and NFTRecord.json to create the correct list
               """
               if x.name in colorList:
                  for j in range(len(colorList[x.name])):
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

      if combinations == 0:
         print(bcolors.ERROR + "\nERROR:" + bcolors.RESET)
         print("The number of all possible combinations is equal to 0. Please review your collection hierarchy"
               "and ensure it is formatted correctly. Please review README.md for more information. \nHere is the "
               "hierarchy of all collections the DNA_Generator gathered from your .blend file, excluding those in "
               f"Script_Ignore: {hierarchy}")

      return combinations

   possibleCombinations = numOfCombinations(hierarchy)

   return possibleCombinations


if __name__ == '__main__':
   get_combinations_from_scene()
