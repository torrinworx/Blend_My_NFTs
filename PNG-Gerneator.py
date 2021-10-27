import bpy
import os
import sys

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)

import time
import json
import conFig
import importlib
importlib.reload(conFig)
from conFig import *

def getBatchData():
    file_name = os.path.join(batch_path, "Batch{}.json".format(renderBatch))
    batch = json.load(open(file_name))
    
    NFTs_in_Batch = batch["NFTs_in_Batch"]
    hierarchy = batch["hierarchy"]
    BatchDNAList = batch["BatchDNAList"]

    return NFTs_in_Batch, hierarchy, BatchDNAList

NFTs_in_Batch, hierarchy, BatchDNAList = getBatchData()

def render_and_save_NFTs():
    '''
    This function will generate a set number of NFTs based on the number of DNA and DNAlist variables in the NFTBatch.json
    file. This function will write to the NFTLedger.json file with the produced batch of NFTs at the end. It will produce
    the NFT images and store them in a file. It will also add DNA and DNAList variables to the Meta Data of each image
    made.
    '''

    x = 1
    for a in BatchDNAList:
        time_start = time.time()

        for i in hierarchy:
            for j in hierarchy[i]:
                bpy.data.collections[j].hide_render = True
                bpy.data.collections[j].hide_viewport = True

        def match_DNA_to_Variant(a):
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

        bpy.context.scene.render.filepath = images_path + slash + "{}.jpeg".format(name)
        bpy.ops.render.render(write_still=True)
        print("Completed {} render. Time: ".format(name) + "%.4f seconds" % (time.time() - time_start))
        x += 1

    print("")
    print("All NFT PNGs generated, process finished.")
    print("")
render_and_save_NFTs()

