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

def get():
    '''
    Refactor this code to get it from the batch number set in config.
    '''

    ledger = json.load(open(batch_path))

    lastLognum = list(ledger)[-1]

    newestBatchDataDictionary = ledger[lastLognum]

    numNFTs = newestBatchDataDictionary['numNFTs_in_Batch']

    dnaDictionary = newestBatchDataDictionary['dnaDictionary']

    variantMetaData = newestBatchDataDictionary['variantMetaData']

    print("")
    print("Generating PNGs of batch #" + str(lastLognum) + ".")
    print("This batch contains " + str(numNFTs) + " strands of NFT DNA>")
    print("")
    print("The DNA strands and their attributes in this batch are as follows: ")
    print("")
    print(dnaDictionary)
    print("")


    return dnaDictionary, numNFTs, variantMetaData

dnaDictionary, numNFTs, variantMetaData = getNumNFTs()

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


    for a in dnaDictionary:
        ''' a is a single dna strand in dnaDictionary, attributeVarients are the variants of that DNA strand'''
        attributeVariants = dnaDictionary[a]
        print("")
        print("----------NFT----------")
        print("DNA attribute list:")
        print(dnaDictionary[a])
        print("DNA Code:")
        print(a)
        print("")

        x = list(dnaDictionary).index(a)
        for i in variantMetaData:
            bpy.data.collections[i].hide_render = True
            bpy.data.collections[i].hide_viewport = True

        for b in list(attributeVariants):
            bpy.data.collections[b].hide_render = False
            bpy.data.collections[b].hide_viewport = False

        bpy.context.scene.render.filepath = "/Users/torrinleonard/Desktop/Blender_Image_Generator/NFT-Images-Test-Folder/{}.jpeg".format(
            name + str(x))
        bpy.ops.render.render(write_still=True)

    print("")
    print("All NFT PNGs generated, process finished.")

render_and_save_NFTs("NFTBattleStation")

