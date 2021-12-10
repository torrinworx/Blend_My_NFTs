# Purpose:
# This file allows you to preview some calculations/numbers generated when you run main. It allows you to make adjustments
# to the config.py file before running main.py in case there are any issues.

import bpy
import os
import sys
import platform
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src.Main_Generators import DNA_Generator
from src.Utility_Scripts import RenderTest

importlib.reload(DNA_Generator)
importlib.reload(RenderTest)


class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR

def printImportant():
    from src import config
    importlib.reload(config)

    listAllCollections, attributeCollections, attributeCollections1, hierarchy, possibleCombinations = DNA_Generator.returnData()

    print(bcolors.OK + "--------YOU ARE RUNNING PREVIEW.py--------" + bcolors.RESET)
    print("*Please Note: Running this test will have no effect on your config.py settings or the state of Blend_My_NFTs.")
    print("")
    print(bcolors.WARNING + "---config.py SETTINGS---" + bcolors.RESET)
    print("NFTs Per Batch(nftsPerBatch): " + bcolors.WARNING + str(config.nftsPerBatch) + bcolors.RESET)
    print("Image Name(imageName): " + bcolors.WARNING + config.nftName + bcolors.RESET)
    print("Image File Format(imageFileFormat): " + bcolors.WARNING + config.imageFileFormat + bcolors.RESET)
    print("Operating system: " + bcolors.WARNING + str(platform.system()) + bcolors.RESET)
    print("Save Path(save_path): " + bcolors.WARNING + config.save_path + bcolors.RESET)
    print("Possible DNA Combinations(possibleCombinations): " + bcolors.WARNING + str(possibleCombinations) + bcolors.RESET)

    remainder = config.maxNFTs % config.nftsPerBatch
    Number_Of_Possible_Batches = (config.maxNFTs - remainder) / config.nftsPerBatch

    print("Max number of NFTs(maxNFTs): " + bcolors.WARNING + str(config.maxNFTs) + bcolors.RESET)
    print("Number of possible batches: " + bcolors.WARNING + str(Number_Of_Possible_Batches) + bcolors.RESET)

    if remainder > 0:
        print("One incomplete batch will have " + bcolors.WARNING + str(remainder) + bcolors.RESET + " DNA in it.")
    elif remainder == 0:
        print("There is no incomplete batch with this combination.")

    print("\nSettings:")
    print("Reset viewport(enableResetViewport): " + bcolors.WARNING + str(config.enableResetViewport) + bcolors.RESET)
    print("3D Models(enable3DModels): " + bcolors.WARNING + str(config.enable3DModels) + bcolors.RESET)
    print("")

    if config.enable3DModels:
        print("3D Model File Format(objectFormatExport): " + bcolors.WARNING + str(config.modelFileFormat) + bcolors.RESET)

    print("Generate Colours(enableGeneration): " + bcolors.WARNING + str(config.enableGeneration) + bcolors.RESET)
    print("")
    print("Colour List(colorList): \n" + bcolors.WARNING + str(config.colorList) + bcolors.RESET)
    print("")
    print("Rarity(enableRarity): " + bcolors.WARNING + str(config.enableRarity) + bcolors.RESET)

    if not config.enable3DModels:
        RenderTest.imageRenderTest()
    if config.enable3DModels:
        print( bcolors.WARNING + "Cannot run Render Test when enable3DModels = True" + bcolors.RESET)

if __name__ == '__main__':
    printImportant()

# To run the following, run main.py with enableRarity = True in config.py:
# Somehow cross check percentage rarity of variant number in NFTRecord.json, iterate through all of them. Then print the
# percentage values that were generated relative to the ones set in .blend
