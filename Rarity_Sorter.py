import bpy
import os
import sys

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)

import itertools
import time
import copy
import re
import json
import importlib

import config
importlib.reload(config)
from config import *

import DNA_Generator
importlib.reload(DNA_Generator)
from DNA_Generator import *

def sortRarityWeights(DataDictionary):
    '''
    Sorts through DataDictionary and appropriately weights each variant based on their rarity percentage set in Blender
    ("rarity" in DNA_Generator). Then
    '''
    return DataDictionary