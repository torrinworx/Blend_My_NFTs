import bpy
import os
import sys

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

import time
import json
import importlib

from src.main import config

importlib.reload(config)
from src.main.config import *

def stripColorFromName(name):
   return "_".join(name.split("_")[:-1])
   
def getBatchData():
    '''
    Retrieves a given batches data determined by renderBatch in config.py
    '''

    file_name = os.path.join(batch_save_path, "Batch{}.json".format(renderBatch))
    batch = json.load(open(file_name))
    
    NFTs_in_Batch = batch["NFTs_in_Batch"]
    hierarchy = batch["hierarchy"]
    BatchDNAList = batch["BatchDNAList"]

    return NFTs_in_Batch, hierarchy, BatchDNAList

NFTs_in_Batch, hierarchy, BatchDNAList = getBatchData()

def render_and_save_NFTs():
    '''
    Renders the NFT DNA in a Batch#.json, where # is renderBatch in config.py. Turns off the viewport camera and
    the render camera for all items in hierarchy.
    '''

    time_start_1 = time.time()

    x = 1
    for a in BatchDNAList:
        for i in hierarchy:
            for j in hierarchy[i]:
                if enableGenerateColours:
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
            listDnaDecunstructed  = a.split('-')
            dnaDictionary = {}

            for i,j in zip(listAttributes,listDnaDecunstructed):
                dnaDictionary[i] = j

            for x in dnaDictionary:
                for k in hierarchy[x]:
                    kNum = hierarchy[x][k]["number"]
                    if kNum == dnaDictionary[x]:
                        dnaDictionary.update({x:k})
            return dnaDictionary

        dnaDictionary = match_DNA_to_Variant(a)
        name = imageName + str(x)

        print("")
        print("----------Rendering New NFT----------")
        print("DNA attribute list:")
        print(list(dnaDictionary.items()))
        print("DNA Code:")
        print(a)
        print("")

        for c in dnaDictionary:
            collection = dnaDictionary[c]
            if not enableGenerateColours:
                bpy.data.collections[collection].hide_render = False
                bpy.data.collections[collection].hide_viewport = False

        time_start_2 = time.time()

        imageOutputBatchSubFolder = "Batch" + str(renderBatch)

        fullImagePath = images_save_path + slash + imageOutputBatchSubFolder + slash + "{}.jpeg".format(name)

        if enableGenerateColours:
            for c in dnaDictionary:
                collection = dnaDictionary[c]
                if stripColorFromName(collection) in colorList:
                    colorVal = int(collection.rsplit("_",1)[1])-1
                    collection = stripColorFromName(collection)
                    bpy.data.collections[collection].hide_render = False
                    bpy.data.collections[collection].hide_viewport = False
                    for activeObject in bpy.data.collections[collection].all_objects: 
                        mat = bpy.data.materials.new("PKHG")
                        mat.diffuse_color = colorList[collection][colorVal]
                        activeObject.active_material = mat
                else:
                    collection = stripColorFromName(collection)
                    bpy.data.collections[collection].hide_render = False
                    bpy.data.collections[collection].hide_viewport = False
        print("Rendering")
        bpy.context.scene.render.filepath = fullImagePath
        bpy.context.scene.render.image_settings.file_format = imageFileFormat
        bpy.ops.render.render(write_still=True)

        print("Completed {} render in ".format(name) + "%.4f seconds" % (time.time() - time_start_2))
        x += 1

    if enableResetViewport:
        for a in BatchDNAList:
            for i in hierarchy:
                for j in hierarchy[i]:
                    if enableGenerateColours:
                        j = stripColorFromName(j)
                    bpy.data.collections[j].hide_render = False
                    bpy.data.collections[j].hide_viewport = False

    print("")
    print("All NFT PNGs rendered, process finished.")
    print("Completed all renders in Batch{}.json in ".format(renderBatch) + "%.4f seconds" % (time.time() - time_start_1))
    print("")

render_and_save_NFTs()