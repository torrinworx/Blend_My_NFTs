import bpy
import os
import sys
import itertools
import time
import copy
import re
import json
import importlib

sys.modules.values()

import config
import DNA_Generator

importlib.reload(config)
from config import *

importlib.reload(DNA_Generator)
from DNA_Generator import *


def sortRarityWeights(DataDictionary):
    '''
    Sorts through DataDictionary and appropriately weights each variant based on their rarity percentage set in Blender
    ("rarity" in DNA_Generator). Then
    '''
    return DataDictionary