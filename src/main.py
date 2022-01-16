# Purpose:
# This file is the main file you run in Blender.

import bpy
import os
import sys
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR

try:
    from src import config
    from src.Utility_Scripts import DuplicateChecker, RenderTest, Preview, BatchRefactorer, RarityChecker
    from src.Model_Generators import Model_Generator
    from src.Main_Generators import Batch_Sorter, DNA_Generator, Exporter

except:
    print(bcolors.ERROR + "ERROR:\nBlender cannot find the Blend_My_NFTs folder." + bcolors.RESET + "\nChange the "
          "directory of your .blend file to be inside the Blend_My_NFTs-main folder. For more details see the README file: "
          "https://github.com/torrinworx/Blend_My_NFTs\n\n")

importlib.reload(config)
importlib.reload(DuplicateChecker)
importlib.reload(Model_Generator)
importlib.reload(Batch_Sorter)
importlib.reload(DNA_Generator)
importlib.reload(Preview)
importlib.reload(RenderTest)
importlib.reload(Exporter)
importlib.reload(BatchRefactorer)
importlib.reload(RarityChecker)


if not config.enableExporter and not config.runPreview and not config.refactorBatchOrder:
    if config.enable3DModels:
        Model_Generator.generate3DModels()

    if not config.enable3DModels:
        DNA_Generator.send_To_Record_JSON()
        Batch_Sorter.makeBatches()
        if config.checkDups:
            DuplicateChecker.checkDups()

if config.enableExporter and not config.runPreview and not config.refactorBatchOrder:
    Exporter.render_and_save_NFTs()

if config.runPreview:
    Preview.printImportant()

if config.refactorBatchOrder:
    BatchRefactorer.reformatNFTCollection()

if config.checkRarity:
    RarityChecker.getRealRarity()
