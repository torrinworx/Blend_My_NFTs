# Purpose:
# This file is the main file you run in Blender.

import bpy
import os
import sys
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src import config
from src.Utility_Scripts import DuplicateChecker, RenderTest, Preview
from src.Model_Generators import Model_Generator
from src.Main_Generators import Batch_Sorter, DNA_Generator, Exporter

importlib.reload(config)
importlib.reload(DuplicateChecker)
importlib.reload(Model_Generator)
importlib.reload(Batch_Sorter)
importlib.reload(DNA_Generator)
importlib.reload(Preview)
importlib.reload(RenderTest)
importlib.reload(Exporter)


if not config.enableExporter and not config.runPreview:
    if config.enable3DModels:
        Model_Generator.generate3DModels()

    if not config.enable3DModels:
        DNA_Generator.send_To_Record_JSON()
        Batch_Sorter.makeBatches()
        if config.checkDups:
            DuplicateChecker.checkDups()

if config.enableExporter and not config.runPreview:
    Exporter.render_and_save_NFTs()

if config.runPreview:
    Preview.printImportant()
