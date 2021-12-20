# Purpose:
# This file takes a given Batch created by DNA_Generator.py and tells blender to render the image or export a 3D model to
# the NFT_Output folder.

import bpy
import os
import sys
import time
import json
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src import config
from src.Main_Generators import metaData

importlib.reload(config)
importlib.reload(metaData)

class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR

if config.runPreview:
   config.nftsPerBatch = config.maxNFTsTest
   config.maxNFTs = config.maxNFTsTest
   config.renderBatch = 1
   config.nftName = "TestImages"

def stripColorFromName(name):
   return "_".join(name.split("_")[:-1])
   
def getBatchData():
    '''
    Retrieves a given batches data determined by renderBatch in config.py
    '''

    file_name = os.path.join(config.batch_json_save_path, "Batch{}.json".format(config.renderBatch))
    batch = json.load(open(file_name))
    
    NFTs_in_Batch = batch["NFTs_in_Batch"]
    hierarchy = batch["hierarchy"]
    BatchDNAList = batch["BatchDNAList"]

    return NFTs_in_Batch, hierarchy, BatchDNAList

def render_and_save_NFTs():
    '''
    Renders the NFT DNA in a Batch#.json, where # is renderBatch in config.py. Turns off the viewport camera and
    the render camera for all items in hierarchy.
    '''

    NFTs_in_Batch, hierarchy, BatchDNAList = getBatchData()

    time_start_1 = time.time()

    x = 1
    for a in BatchDNAList:
        for i in hierarchy:
            for j in hierarchy[i]:
                if config.enableGeneration:
                    '''
                     Remove Color code so blender recognises the collection
                    '''
                    j = stripColorFromName(j)
                bpy.data.collections[j].hide_render = True
                bpy.data.collections[j].hide_viewport = True

        def match_DNA_to_Variant(a):
            '''
            Matches each DNA number sepearted by "-" to its attribute, then its variant.
            '''

            listAttributes = list(hierarchy.keys())
            listDnaDecunstructed = a.split('-')
            dnaDictionary = {}

            for i, j in zip(listAttributes, listDnaDecunstructed):
                dnaDictionary[i] = j

            for x in dnaDictionary:
                for k in hierarchy[x]:
                    kNum = hierarchy[x][k]["number"]
                    if kNum == dnaDictionary[x]:
                        dnaDictionary.update({x: k})
            return dnaDictionary

        dnaDictionary = match_DNA_to_Variant(a)
        name = config.nftName + "_" + str(x)

        print("")
        print("----------Rendering New NFT----------")
        print("DNA attribute list:")
        print(dnaDictionary)
        print("DNA Code:")
        print(a)
        print("")

        for c in dnaDictionary:
            collection = dnaDictionary[c]
            if not config.enableGeneration:
                bpy.data.collections[collection].hide_render = False
                bpy.data.collections[collection].hide_viewport = False

        time_start_2 = time.time()

        batchFolder = os.path.join(config.nft_save_path, "Batch" + str(config.renderBatch))

        imagePath = os.path.join(batchFolder, "Images", name)
        animationPath = os.path.join(batchFolder, "Animations", name)
        modelPath = os.path.join(batchFolder, "Models", name)

        imageFolder = os.path.join(batchFolder, "Images")
        animationFolder = os.path.join(batchFolder, "Animations")
        modelFolder = os.path.join(batchFolder, "Models")
        metaDataFolder = os.path.join(batchFolder, "BMNFT_metaData")

        if config.enableGeneration:
            for c in dnaDictionary:
                collection = dnaDictionary[c]
                if stripColorFromName(collection) in config.colorList:
                    colorVal = int(collection.rsplit("_", 1)[1])-1
                    collection = stripColorFromName(collection)
                    bpy.data.collections[collection].hide_render = False
                    bpy.data.collections[collection].hide_viewport = False
                    if config.generationType == 'color':
                        for activeObject in bpy.data.collections[collection].all_objects: 
                            mat = bpy.data.materials.new("PKHG")
                            mat.diffuse_color = config.colorList[collection][colorVal]
                            activeObject.active_material = mat
                    if config.generationType == 'material':
                        for activeObject in bpy.data.collections[collection].all_objects: 
                            activeObject.material_slots[0].material = bpy.data.materials[config.colorList[collection][colorVal]]
                else:
                    collection = stripColorFromName(collection)
                    bpy.data.collections[collection].hide_render = False
                    bpy.data.collections[collection].hide_viewport = False

        print("Generating")

        if config.enableImages:
            if not os.path.exists(imageFolder):
                os.makedirs(imageFolder)

            bpy.context.scene.render.filepath = imagePath
            bpy.context.scene.render.image_settings.file_format = config.imageFileFormat
            bpy.ops.render.render(write_still=True)

        if config.enableAnimations:
            if not os.path.exists(animationFolder):
                os.makedirs(animationFolder)

            bpy.context.scene.render.filepath = animationPath
            bpy.context.scene.render.image_settings.file_format = config.animationFileFormat
            bpy.ops.render.render(animation=True)

        if config.enableModelsBlender:
            if not os.path.exists(modelFolder):
                os.makedirs(modelFolder)

            for i in dnaDictionary:
                coll = dnaDictionary[i]

                for obj in bpy.data.collections[coll].all_objects:
                    obj.select_set(True)

            for obj in bpy.data.collections['Script_Ignore'].all_objects:
                obj.select_set(True)

            if config.modelFileFormat == 'glb':
                bpy.ops.export_scene.gltf(filepath=modelPath,
                                          check_existing=True,
                                          export_format='GLB',
                                          use_selection=True)
            elif config.modelFileFormat == 'fbx':
                bpy.ops.export_scene.fbx(filepath=modelPath,
                                         check_existing=True,
                                         use_selection=True)
            elif config.modelFileFormat == 'obj':
                bpy.ops.export_scene.obj(filepath=modelPath,
                                         check_existing=True,
                                         use_selection=True)
            elif config.modelFileFormat == 'x3d':
                bpy.ops.export_scene.x3d(filepath=modelPath,
                                         check_existing=True,
                                         use_selection=True)

        if not os.path.exists(metaDataFolder):
            os.makedirs(metaDataFolder)

        metaDataDict = {}
        metaDataDict["name"] = name
        metaDataDict["description"] = config.metaDataDescription
        metaDataDict["NFT_DNA"] = a
        metaDataDict["NFT_Variants"] = dnaDictionary

        jsonMetaData = json.dumps(metaDataDict, indent=1, ensure_ascii=True)

        with open(os.path.join(metaDataFolder, "Data_" + name + ".json"), 'w') as outfile:
            outfile.write(jsonMetaData + '\n')

        print("Completed {} render in ".format(name) + "%.4f seconds" % (time.time() - time_start_2))
        x += 1

    if config.enableResetViewport:
        for a in BatchDNAList:
            for i in hierarchy:
                for j in hierarchy[i]:
                    if config.enableGeneration:
                        j = stripColorFromName(j)
                    bpy.data.collections[j].hide_render = False
                    bpy.data.collections[j].hide_viewport = False

    print("\nAll NFT PNGs rendered, process finished.")
    print("Completed all renders in Batch{}.json in ".format(config.renderBatch) + "%.4f seconds" % (time.time() - time_start_1) + "\n")

if __name__ == '__main__':
    render_and_save_NFTs()
