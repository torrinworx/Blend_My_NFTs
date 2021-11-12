import bpy
import os
import re
import sys
import copy
import time
import json
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

def sortRarityWeights(DataDictionary):
    '''
    Sorts through DataDictionary and appropriately weights each variant based on their rarity percentage set in Blender
    ("rarity" in DNA_Generator). Then
    '''
    return DataDictionary