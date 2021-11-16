# This script runs DNA_Generator.py and Batch_Sorter.py so you only have to run main.py in Blender
import bpy
import os
import sys
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src.main import config
importlib.reload(config)

from src.generators_and_sorters import DNA_Generator, Preview, RenderTest, Batch_Sorter, Model_Generator, Image_Generator
importlib.reload(DNA_Generator)
importlib.reload(Batch_Sorter)
importlib.reload(Model_Generator)
importlib.reload(Preview)
importlib.reload(RenderTest)
importlib.reload(Image_Generator)

if not config.runPreview and not config.renderImage:
    if config.enable3DModels:
        Model_Generator.generate3DModels()

    if not config.enable3DModels:
        DNA_Generator.send_To_Record_JSON()
        Batch_Sorter.makeBatches()

if config.runPreview:
    Preview.printImportant()

if config.renderImage:
    Image_Generator.render_and_save_NFTs()

