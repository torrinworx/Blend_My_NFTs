# This script runs DNA_Generator.py and Batch_Sorter.py so you only have to run main.py in Blender
import bpy
import os
import sys
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)

sys.modules.values()

from src.generators_and_sorters import DNA_Generator

from src.generators_and_sorters import Batch_Sorter

importlib.reload(DNA_Generator)
from src.generators_and_sorters.DNA_Generator import *

importlib.reload(Batch_Sorter)
from src.generators_and_sorters.Batch_Sorter import *

if not useModels:
    DNA_Generator.send_To_Record_JSON()
    Batch_Sorter.makeBatches()

'''
if useModels:
    # Some function that activates DNA_Generator_3D_Models.py
'''