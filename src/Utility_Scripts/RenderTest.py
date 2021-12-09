# Purpose:
# This file allows you to test the time it takes to render an image, then calculate how long it will take to render all
# images specified in maxNFTs in config.py.

import bpy
import os
import sys
import copy
import time
import shutil
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src import config
from src.Main_Generators import Batch_Sorter, DNA_Generator, Exporter

importlib.reload(config)
importlib.reload(DNA_Generator)
importlib.reload(Batch_Sorter)
importlib.reload(Exporter)


class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR

def imageRenderTest():
    originalMaxNFTs = copy.deepcopy(config.maxNFTs)
    config.nftsPerBatch = config.maxNFTsTest
    config.maxNFTs = config.maxNFTsTest
    config.renderBatch = 1
    config.nftName = "TestImages"

    print(bcolors.WARNING + "\n---RUNNING IMAGE RENDER TEST---\n" + bcolors.RESET)
    print("This test will render one image, record the time it took, then calculate the time to render")
    print("the maxNFTs specified in config.py based on that image.")
    print("*Please Note: All config.py settings will be preserved and the test image and batch folder will be")
    print("deleted.")

    print(bcolors.WARNING + "\n---RUNNING DNA_Generator.py SHELL---\n" + bcolors.RESET)
    DNA_Generator.send_To_Record_JSON()

    print(bcolors.WARNING + "\n---RUNNING Batch_Sorter.py SHELL---\n" + bcolors.RESET)
    Batch_Sorter.makeBatches()

    fullRenderTime = time.time()

    print(bcolors.WARNING + "\n---RUNNING Exporter.py SHELL---\n" + bcolors.RESET)
    Exporter.render_and_save_NFTs()

    print("Image(s) rendered in %.4f seconds" % (time.time() - fullRenderTime))
    print(bcolors.WARNING + "\nTime to render " + str(originalMaxNFTs) + " NFT Images: " + bcolors.RESET)

    renderMaxTime = str(((int(time.time() - fullRenderTime)) / int(config.maxNFTs)) * originalMaxNFTs) + "s"
    
    print(renderMaxTime)

    os.remove(config.batch_json_save_path + config.slash + "Batch1.json")
    os.remove(config.save_path + config.slash + "NFTRecord.json")
    shutil.rmtree(config.nft_save_path + config.slash + "Batch1")

if __name__ == '__main__':
    imageRenderTest()
