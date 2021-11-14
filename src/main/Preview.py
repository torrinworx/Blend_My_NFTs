# This file allows you to preview some calculations/numbers generated when you run main. It allows you to make adjustments
# to the config.py file before running main.py in case there are any issues.

import bpy
import os
import re
import sys
import copy
import timeit
import json
import random
import itertools
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src.main import config
from src.generators_and_sorters import DNA_Generator

importlib.reload(config)
from src.main.config import *

importlib.reload(DNA_Generator)
from src.generators_and_sorters.DNA_Generator import *

class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR

listAllCollections, attributeCollections, attributeCollections1, hierarchy, possibleCombinations = DNA_Generator.returnData()

print(bcolors.OK + "--------YOU ARE RUNNING PREVIEW.py--------" + bcolors.RESET)
print("*Please Note: Running this test will have no effect on your config.py settings or the state of Blend_My_NFTs.")
print("")
print(bcolors.WARNING + "---config.py SETTINGS---" + bcolors.RESET)
print("NFTs Per Batch(nftsPerBatch): " + bcolors.WARNING + str(nftsPerBatch) + bcolors.RESET)
print("Image Name(imageName): " + bcolors.WARNING + imageName + bcolors.RESET)
print("Image File Format(imageFileFormat): " + bcolors.WARNING + imageFileFormat + bcolors.RESET)
print("Operating system: " + bcolors.WARNING + str(platform.system()) + bcolors.RESET)
print("Save Path(save_path): " + bcolors.WARNING + save_path + bcolors.RESET)
print("Possible DNA Combinations(possibleCombinations): " + bcolors.WARNING + str(possibleCombinations) + bcolors.RESET)

remainder = maxNFTs % nftsPerBatch
Number_Of_Possible_Batches = (maxNFTs - remainder) / nftsPerBatch

print("Max number of NFTs(maxNFTs): " + bcolors.WARNING + str(maxNFTs) + bcolors.RESET)
print("Number of possible batches: " + bcolors.WARNING + str(Number_Of_Possible_Batches) + bcolors.RESET)

if remainder > 0:
    print("One incomplete batch will have " + bcolors.WARNING + str(remainder) + bcolors.RESET + " DNA in it.")
elif remainder == 0:
    print("There is no incomplete batch with this combination.")

print("\nSettings:")
print("Reset viewport(enableResetViewport): " + bcolors.WARNING + str(enableResetViewport) + bcolors.RESET)
print("3D Models(enable3DModels): " + bcolors.WARNING + str(enable3DModels) + bcolors.RESET)
if enable3DModels:
    print("3D Model File Format(objectFormatExport): " + bcolors.WARNING + str(objectFormatExport) + bcolors.RESET)
print("Generate Colours(enableGenerateColours): " + bcolors.WARNING + str(enableGenerateColours) + bcolors.RESET)
print("")
print("Colour List(colorList): \n" + bcolors.WARNING + str(colorList) + bcolors.RESET)
print("")
print("Rarity(enableRarity): " + bcolors.WARNING + str(enableRarity) + bcolors.RESET)






'''

'''
'''
if config.enable3DModels:
    # Create a timer to time export of 3D models to 3D_Model_Output folder in Model_Generator.py
    print("")
'''

# Add the ability to render a test image so that you can estimate the time per batch and the over all time to render
# the total NFT collection.




# To run the following, run main.py with enableRarity = True in config.py:
# Somehow cross check percentage rarity of variant number in NFTRecord.json, iterate through all of them. Then print the
# percentage values that were generated relative to the ones set in .blend
