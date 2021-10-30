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

import config
import importlib
importlib.reload(config)
from config import *

import DNA_Generator
import importlib
importlib.reload(DNA_Generator)
from DNA_Generator import *
