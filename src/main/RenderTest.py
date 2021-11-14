# This file allows you to test the time it takes to render an image, then calculate how long it will take to render all
# images specified in maxNFTs in config.py.

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

def set_configState(f):
    f.nftsPerBatch = 5
    f.renderBatch = 1
    f.maxNFTs = 5
    f.imageName = "TestRenderImage_"

if not config.enable3DModels:
    print(bcolors.WARNING + "\n---RUNNING IMAGE RENDER TEST---\n" + bcolors.RESET)
    print("This test will render one image, record the time it took, then calculate the time to render")
    print("the maxNFTs specified in config.py based on that image.")
    print("*Please Note: All config.py settings will be preserved and the test image and batch folder will be")
    print("deleted.")

    def store_configState():
        nftsPerBatchStored = copy.deepcopy(nftsPerBatch)
        renderBatchStored = copy.deepcopy(renderBatch)
        maxNFTsStored = copy.deepcopy(maxNFTs)
        return nftsPerBatchStored, renderBatchStored, maxNFTsStored

    nftsPerBatchStored, renderBatchStored, maxNFTsStored = store_configState()

    from src.generators_and_sorters import DNA_Generator
    from src.generators_and_sorters import Batch_Sorter
    from src.generators_and_sorters import Image_Generator

    importlib.reload(DNA_Generator)
    from src.generators_and_sorters.DNA_Generator import *

    importlib.reload(Batch_Sorter)
    from src.generators_and_sorters.Batch_Sorter import *

    importlib.reload(Image_Generator)
    from src.generators_and_sorters.Image_Generator import *

    print(bcolors.WARNING + "\n---RUNNING DNA_Generator.py SHELL---\n" + bcolors.RESET)
    DNA_Generator.send_To_Record_JSON()

    print(bcolors.WARNING + "\n---RUNNING Batch_Sorter.py SHELL---\n" + bcolors.RESET)
    Batch_Sorter.makeBatches()

    startRender = timeit.timeit()

    print(bcolors.WARNING + "\n---RUNNING Batch_Sorter.py SHELL---\n" + bcolors.RESET)
    #Image_Generator.render_and_save_NFTs()

    endRender = timeit.timeit()

    print("Image rendered in %.4f seconds" % (endRender - startRender))

    def resetState():
        config.nftsPerBatch = nftsPerBatchStored
        config.renderBatch = renderBatchStored
        config.maxNFTs = maxNFTsStored