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

from src.generators_and_sorters import DNA_Generator
importlib.reload(DNA_Generator)

from src.generators_and_sorters import Batch_Sorter
importlib.reload(Batch_Sorter)

from src.generators_and_sorters import Model_Generator
importlib.reload(Model_Generator)

from src.main import Preview
importlib.reload(Preview)

from src.main import RenderTest
importlib.reload(RenderTest)

if not config.runPreview and config.runRenderTest:
    if config.enable3DModels:
        Model_Generator.generate3DModels()

    if not config.enable3DModels:
        DNA_Generator.send_To_Record_JSON()
        Batch_Sorter.makeBatches()

if config.runPreview:
    Preview.printImportant()

if config.runRenderTest:
    RenderTest.imageRenderTest()