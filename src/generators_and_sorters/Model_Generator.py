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

importlib.reload(config)
from src.main.config import *

class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR

def generate3DModels():
    time_start = time.time()

    '''
    This sorter assumes that every object file variant for each attribute has a unique name. Names can include numbers, or 
    any character value, but must be unique for each object. 
    '''

    def deleteAllObjects():
        '''
        Deletes all objects in the current scene open in Blender
        '''
        deleteListObjects = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'HAIR', 'POINTCLOUD', 'VOLUME', 'GPENCIL',
                             'ARMATURE', 'LATTICE', 'EMPTY', 'LIGHT', 'LIGHT_PROBE', 'CAMERA', 'SPEAKER']

        for o in bpy.context.scene.objects:
            for i in deleteListObjects:
                if o.type == i:
                    o.select_set(False)
                else:
                    o.select_set(True)
        bpy.ops.object.delete()

    attributeList = os.listdir(modelAssetPath)
    removeList = [".gitignore", ".DS_Store", "Script_Ignore_Folder"]
    attributeList = [x for x in attributeList if (x not in removeList)]
    hierarchy = {}

    for i in attributeList:
        hierarchy[i] = os.listdir(modelAssetPath + slash + i)

    def numOfCombinations(hierarchy):
      '''
      Returns "combinations" the number of all possible NFT combinations.
      '''
      hierarchyByNum = []
      for i in hierarchy:
         hierarchyByNum.append(len(hierarchy[i]))
      combinations = 1
      for i in hierarchyByNum:
         combinations = combinations*i

      if combinations == 0:
          print(bcolors.FAIL + "ERROR:" + bcolors.RESET)
          print("The number of all possible combinations is equal to 0. Please review your collection hierarchy \n "
                "and ensure it is formatted correctly.")
      return combinations

    combinations = numOfCombinations(hierarchy)
    allCombinationsNames = list(itertools.product(*hierarchy.values()))

    count = 1
    for i in allCombinationsNames:
        if objectFormatImport == "gltf":
            path1 = modelAssetPath + slash + "Script_Ignore_Folder"
            Script_Ignore_Folder = os.listdir(path1)

            for h in Script_Ignore_Folder:
                bpy.ops.import_scene.gltf(filepath=path1 + slash + h)

        for j in i:
            def getParent(hierarchy):
                for x in hierarchy:
                    for y in hierarchy[x]:
                        if y == j:
                            return x

            parent = getParent(hierarchy)
            path2 = modelAssetPath + slash + parent + slash + j

            if objectFormatImport == "gltf":
                bpy.ops.import_scene.gltf(filepath=path2)

        bpy.ops.export_scene.gltf(filepath=model_save_path + slash + imageName + str(count),
                                  check_existing=True, export_format='GLB')
        deleteAllObjects()
        count += 1

    print("Generated .glb files in %.4f seconds" % (time.time() - time_start))