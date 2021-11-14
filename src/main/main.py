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
from src.main.config import *

if config.enable3DModels:
    from src.generators_and_sorters import Model_Generator

    importlib.reload(Model_Generator)
    from src.generators_and_sorters.Model_Generator import *

    Model_Generator.generate3DModels()

if not config.enable3DModels:
    from src.generators_and_sorters import DNA_Generator
    from src.generators_and_sorters import Batch_Sorter

    importlib.reload(DNA_Generator)
    from src.generators_and_sorters.DNA_Generator import *
    importlib.reload(Batch_Sorter)
    from src.generators_and_sorters.Batch_Sorter import *

    DNA_Generator.send_To_Record_JSON()
    Batch_Sorter.makeBatches()
