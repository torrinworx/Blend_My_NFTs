import bpy
import os
import sys

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)

import time
import json
import config
import importlib
importlib.reload(config)
from config import *

def getBatchData():
    '''
    Retrieves a given batches data determined by renderBatch in config.py
    '''

    file_name = os.path.join(batch_path, "Batch{}.json".format(renderBatch))
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

    x = 1
    for a in BatchDNAList:
        for i in hierarchy:
            for j in hierarchy[i]:
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
            bpy.data.collections[collection].hide_render = False
            bpy.data.collections[collection].hide_viewport = False

        time_start_2 = time.time()

        fullImagePath = images_path + slash + "{}.jpeg".format(name)

        bpy.context.scene.render.filepath = fullImagePath
        bpy.ops.render.render(write_still=True)
        print("Completed {} render. Time: ".format(name) + "%.4f seconds" % (time.time() - time_start_2))

        def imageMetaData():
            meta = {}
            


        x += 1

    print("")
    print("All NFT PNGs rendered, process finished.")
    print("Time to complete all renders in Batch{}.json:".format(renderBatch) + "%.4f seconds" % (time.time() - time_start_2))
    print("")

render_and_save_NFTs()

