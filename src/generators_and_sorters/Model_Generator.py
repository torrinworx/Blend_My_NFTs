# The code in this file was generous sponsored by the amazing team over at Rumble Worlds!
# Feel free to check out their amazing project and see how they are using Blend_My_NFTs
# https://www.rumbleworlds.io/

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
    '''
    This sorter assumes that every object file variant for each attribute has a unique name. Names can include numbers, or 
    any character value, but must be unique for each object. 
    '''
    time_start = time.time()

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

    deleteAllObjects()

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

        path1 = modelAssetPath + slash + "Script_Ignore_Folder"
        Script_Ignore_Folder = os.listdir(path1)

        for h in Script_Ignore_Folder:
            fileName, fileExtension = os.path.splitext(h)
            if fileExtension == ".glb":
                bpy.ops.import_scene.gltf(filepath=path1 + slash + h)
            elif fileExtension == ".fbx":
                bpy.ops.import_scene.fbx(filepath=path1 + slash + h)
            elif fileExtension == ".obj":
                bpy.ops.import_scene.obj(filepath=path1 + slash + h)
            elif fileExtension == ".x3d":
                bpy.ops.import_scene.obj(filepath=path1 + slash + h)

        for j in i:
            def getParent(hierarchy):
                for x in hierarchy:
                    for y in hierarchy[x]:
                        if y == j:
                            return x

            parent = getParent(hierarchy)
            path2 = modelAssetPath + slash + parent + slash + j

            fileName, fileExtension = os.path.splitext(j)
            if fileExtension == ".glb":
                bpy.ops.import_scene.gltf(filepath=path2)
            elif fileExtension == ".fbx":
                bpy.ops.import_scene.fbx(filepath=path2)
            elif fileExtension == ".obj":
                bpy.ops.import_scene.obj(filepath=path2)
            elif fileExtension == ".x3d":
                bpy.ops.import_scene.obj(filepath=path2)

        if objectFormatExport == 'glb':
            bpy.ops.export_scene.gltf(filepath=model_save_path + slash + imageName + str(count),
                                      check_existing=True, export_format='GLB')
        elif objectFormatExport == 'fbx':
            bpy.ops.export_scene.fbx(filepath=model_save_path + slash + imageName + str(count),
                                      check_existing=True)
        elif objectFormatExport == 'obj':
            bpy.ops.export_scene.obj(filepath=model_save_path + slash + imageName + str(count),
                                      check_existing=True)
        elif objectFormatExport == 'x3d':
            bpy.ops.export_scene.x3d(filepath=model_save_path + slash + imageName + str(count),
                                      check_existing=True)

        deleteAllObjects()

        count += 1

    print("Generated .glb files in %.4f seconds" % (time.time() - time_start))


if __name__ == '__main__':
    generate3DModels()
