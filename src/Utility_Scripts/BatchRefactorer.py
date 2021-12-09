# Purpose:
#
import bpy
import os
import re
import sys
import copy
import time
import json
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src import config

importlib.reload(config)

def getNFType():
    batchListDirty = os.listdir(config.nft_save_path)
    removeList = [".gitignore", ".DS_Store", "Script_Ignore_Folder"]
    batchList = [x for x in batchListDirty if (x not in removeList)]

    images = False
    animations = False
    models = False
    metaData = False

    batchContent = os.listdir(os.path.join(config.nft_save_path, "Batch1"))

    if "Images" in batchContent:
        images = True
    if "Animations" in batchContent:
        animations = True
    if "Models" in batchContent:
        models = True
    if "NFT_metaData" in batchContent:
        metaData = True

    return images, animations, models, metaData

def reformatBatches():
    images, animations, models, metaData = getNFType()

    completeCollPath = os.path.join(config.nft_save_path, "Complete_Collection")
    completeImagePath = os.path.join(completeCollPath, "Images")
    completeAnimationsPath = os.path.join(completeCollPath, "Animations")
    completeModelsPath = os.path.join(completeCollPath, "Models")
    completeMetaDataPath = os.path.join(completeCollPath, "NFT_metaData")

    os.mkdir(completeCollPath)

    if images:
        os.mkdir(completeImagePath)
    if animations:
        os.mkdir(completeAnimationsPath)
    if models:
        os.mkdir(completeModelsPath)
    if metaData:
        os.mkdir(completeMetaDataPath)

    batchListDirty = os.listdir(config.nft_save_path)
    removeList = [".gitignore", ".DS_Store", "Script_Ignore_Folder"]
    batchList = [x for x in batchListDirty if (x not in removeList)]

    count = 1
    for i in batchList:
        if images:
            imagesDir = os.path.join(config.nft_save_path, i, "Images")
            imagesList = sorted(os.listdir(imagesDir))
            print(imagesList)

            for j in imagesList:
                k = copy.deepcopy(j.removeprefix("Image_"))
                extension = os.path.splitext(k)[1]
                nameDirty = os.path.splitext(k)[0]

                name = nameDirty.split("_")[0]

                os.rename(os.path.join(imagesDir, j), os.path.join(completeImagePath, "Image_" + name + "_" + str(count) + extension))

        count += 1

        '''
        if animations:
        if models:
        if metaData:'''


if __name__ == '__main__':
    reformatBatches()
