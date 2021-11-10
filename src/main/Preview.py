# This file allows you to preview some calculations/numbers generated when you run main. It allows you to make adjustments
# to the config.py file before running main.py in case there are any issues.

import bpy
import os
import re
import sys
import copy
import time
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
print("")
print(bcolors.WARNING + "CONFIG.py INPUT" + bcolors.RESET)
print("The number of NFT DNA per batch: " + str(nftsPerBatch))
print("Number of possible combinations with current .blend file: " + str(possibleCombinations))

if not enableMaxNFTs:

    remainder1 = possibleCombinations % nftsPerBatch
    Number_Of_Possible_Batches1 = (possibleCombinations - remainder1) / nftsPerBatch

    print("The total number of NFT DNA sent to NFTRecord: " + str(possibleCombinations))
    print("The number of possible batches: " + str(Number_Of_Possible_Batches1))
    print("The final batch will have " + str(remainder1) + " left over NFT DNA in it.")

if enableMaxNFTs:

    possibleCombinations = maxNFTs
    remainder2 = possibleCombinations % nftsPerBatch
    Number_Of_Possible_Batches2 = (possibleCombinations - remainder2) / nftsPerBatch

    print("The set Max number of NFT DNA sent to NFTRecord: " + str(maxNFTs))

    if remainder2 > 0:
        print("The final batch will have " + str(remainder2) + " left over NFT DNA in it.")
    elif remainder2 == 0:
        print("There is no extra batch with this combination.")

    print("The number of possible batches with Max number enabled: " + str(Number_Of_Possible_Batches2))

# Add the ability to render a test image so that you can estimate the time per batch and the over all time to render
# the total NFT collection.