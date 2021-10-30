# This script runs DNA_Generator.py and Batch_Sorter.py so you only have to run main.py in Blender
import bpy
import os
import sys
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)

sys.modules.values()

import DNA_Generator
import Batch_Sorter

importlib.reload(DNA_Generator)
from DNA_Generator import *

importlib.reload(Batch_Sorter)
from Batch_Sorter import *

DNA_Generator.send_To_Record_JSON()
Batch_Sorter.makeBatches()