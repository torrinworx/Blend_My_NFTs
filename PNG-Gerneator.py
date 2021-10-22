import bpy
import os
import sys

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)

import json
import conFig
import importlib
importlib.reload(conFig)
from conFig import *

batch_to_render = 1

def getBatchData():
    file_name = os.path.join(json_save_path, "Batch{}.json".format(batch_to_render))
    batch = json.load(open(file_name))
    NFTs_in_Batch = batch["NFTs_in_Batch"]
    variantMetaData = batch["variantMetaData"]
    BatchDNAList = batch["BatchDNAList"]

    return NFTs_in_Batch, variantMetaData, BatchDNAList

NFTs_in_Batch, variantMetaData, BatchDNAList = getBatchData()

def render_and_save_NFTs(name):
    '''
    This function will generate a set number of NFTs based on the number of DNA and DNAlist variables in the NFTBatch.json
    file. This function will write to the NFTLedger.json file with the produced batch of NFTs at the end. It will produce
    the NFT images and store them in a file. It will also add DNA and DNAList variables to the Meta Data of each image
    made.
    '''

    for i in variantMetaData:
        bpy.data.collections[i].hide_render = True
        bpy.data.collections[i].hide_viewport = True

    def match_DNA_to_Variant():

        for i in BatchDNAList:
            dna_Decunstructed  = i.split('-')


            print(dna_Decunstructed)
            print("")
        print("")
        print(variantMetaData)
    match_DNA_to_Variant()


    '''






    for a in BatchDNAList:
        a is a single dna strand in dnaDictionary, attributeVarients are the variants of that DNA strand
        attributeVariants = BatchDNAList[a]
        print("")
        print("----------NFT----------")
        print("DNA attribute list:")
        print(BatchDNAList[a])
        print("DNA Code:")
        print(a)
        print("")


        for b in list(attributeVariants):
            bpy.data.collections[b].hide_render = False
            bpy.data.collections[b].hide_viewport = False

        bpy.context.scene.render.filepath = "/Users/torrinleonard/Desktop/Blender_Image_Generator/NFT-Images-Test-Folder/{}.jpeg".format(
            name + str(x))
        bpy.ops.render.render(write_still=True)

    print("")
    print("All NFT PNGs generated, process finished.")
    '''

render_and_save_NFTs("NFTBattleStation")

