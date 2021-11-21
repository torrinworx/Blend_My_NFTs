# Some code in this file was generously sponsored by the amazing team over at SolSweepers!
# Feel free to check out their amazing project and see how they are using Blend_My_NFTs:
# https://discord.gg/QTT7dzcuVs

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
importlib.reload(config)

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

    file_name = os.path.join(config.batch_save_path, "Batch{}.json".format(config.renderBatch))
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
        metaData = {}

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
        name = config.nftName + str(x)


        def returnMetaData(metaDataType):
            '''
            This function exports formatted meta data based on the metaDataType variable in config.py
            '''
            if metaDataType == "SOL":
                metaData["name"] = name
                metaData["symbol"] = ""
                metaData["description"] = config.metaDataDescription
                metaData["seller_fee_basis_points"] = None
                metaData["image"] = ""
                metaData["animation_url"] = ""
                metaData["external_url"] = ""
                metaData["attributes"] = dnaDictionary
                metaData["collection"] = {"name": "", "family": ""}
                metaData["properties"] = {"files": [{"uri": "", "type": ""}],
                                          "category": "",
                                          "creators": [{"address": "", "share": None}]
                                          }

            elif metaDataType == "ADA":

                return
            return

        returnMetaData(config.metaDataType)

        print("")
        print("----------Rendering New NFT----------")
        print("DNA attribute list:")
        print(list(dnaDictionary.items()))
        print("DNA Code:")
        print(a)
        print("")

        for c in dnaDictionary:
            collection = dnaDictionary[c]
            if not config.enableGeneration:
                bpy.data.collections[collection].hide_render = False
                bpy.data.collections[collection].hide_viewport = False

        time_start_2 = time.time()

        batchFolder = os.path.join(config.images_save_path, "Batch" + str(config.renderBatch))
        imagePath = os.path.join(batchFolder, "Images", name)
        metaDataFolder = os.path.join(batchFolder, "Image_Data")

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
        print("Rendering")
        bpy.context.scene.render.filepath = imagePath
        bpy.context.scene.render.image_settings.file_format = config.imageFileFormat
        bpy.ops.render.render(write_still=True)

        if not os.path.exists(metaDataFolder):
            os.mkdir(metaDataFolder)

        jsonMetaData = json.dumps(metaData, indent=1, ensure_ascii=True)
        with open(os.path.join(metaDataFolder, name + "_Data"), 'w') as outfile:
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
