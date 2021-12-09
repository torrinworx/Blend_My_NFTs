# Purpose:
#
import bpy
import os
import re
import sys
import copy
import time
import json
import shutil
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src import config

importlib.reload(config)

def getNFType():
    batchListDirty = os.listdir(config.nft_save_path)
    removeList = [".gitignore", ".DS_Store"]
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

    completeCollPath = os.path.join(config.save_path, "Complete_Collection")
    completeImagePath = os.path.join(completeCollPath, "Images")
    completeAnimationsPath = os.path.join(completeCollPath, "Animations")
    completeModelsPath = os.path.join(completeCollPath, "Models")
    completeMetaDataPath = os.path.join(completeCollPath, "NFT_metaData")

    if not os.path.exists(completeCollPath):
        os.mkdir(completeCollPath)
    if images and not os.path.exists(completeImagePath):
        os.mkdir(completeImagePath)
    if animations and not os.path.exists(completeAnimationsPath):
        os.mkdir(completeAnimationsPath)
    if models and not os.path.exists(completeModelsPath):
        os.mkdir(completeModelsPath)
    if metaData and not os.path.exists(completeMetaDataPath):
        os.mkdir(completeMetaDataPath)

    batchListDirty = os.listdir(config.nft_save_path)
    removeList = [".gitignore", ".DS_Store"]
    batchList = [x for x in batchListDirty if (x not in removeList)]

    imageCount = 1
    animationCount = 1
    modelCount = 1
    dataCount = 1
    for i in batchList:
        if images:
            imagesDir = os.path.join(config.nft_save_path, i, "Images")
            imagesList = sorted(os.listdir(imagesDir))

            for j in imagesList:
                imageOldPath = os.path.join(config.nft_save_path, i, "Images", j)
                nameOldDirty = copy.deepcopy(os.path.splitext(j)[0])
                extension = copy.deepcopy(os.path.splitext(j)[1])
                nameOldClean = nameOldDirty.split("_")[0]

                nameNew = nameOldClean + "_" + str(imageCount)
                imageNewPath = os.path.join(completeImagePath, nameNew + extension)

                os.rename(imageOldPath, imageNewPath)

                imageCount += 1

        if animations:
            animationsDir = os.path.join(config.nft_save_path, i, "Animations")
            animationsList = sorted(os.listdir(animationsDir))
            
            for j in animationsList: 
                animationOldPath = os.path.join(config.nft_save_path, i, "Animations", j)
                nameOldDirty = copy.deepcopy(os.path.splitext(j)[0])
                extension = copy.deepcopy(os.path.splitext(j)[1])
                nameOldClean = nameOldDirty.split("_")[0]
    
                nameNew = nameOldClean + "_" + str(animationCount)
                animationNewPath = os.path.join(completeAnimationsPath, nameNew + extension)
    
                os.rename(animationOldPath, animationNewPath)
    
                animationCount += 1

        if models:
            modelsDir = os.path.join(config.nft_save_path, i, "Models")
            modelsList = sorted(os.listdir(modelsDir))

            for j in modelsList:
                modelOldPath = os.path.join(config.nft_save_path, i, "Models", j)
                nameOldDirty = copy.deepcopy(os.path.splitext(j)[0])
                extension = copy.deepcopy(os.path.splitext(j)[1])
                nameOldClean = nameOldDirty.split("_")[0]

                nameNew = nameOldClean + "_" + str(modelCount)
                modelsNewPath = os.path.join(completeModelsPath, nameNew + extension)

                os.rename(modelOldPath, modelsNewPath)

                modelCount += 1

        if metaData:
            dataDir = os.path.join(config.nft_save_path, i, "NFT_metaData")
            dataList = sorted(os.listdir(dataDir))

            for j in dataList:
                dataOldPath = os.path.join(config.nft_save_path, i, "NFT_metaData", j)
                nameOldDirty = copy.deepcopy(os.path.splitext(j)[0])
                extension = copy.deepcopy(os.path.splitext(j)[1])
                nameOldClean = nameOldDirty.split("_")[0]

                nameNew = nameOldClean + "_" + str(dataCount)
                dataNewPath = os.path.join(completeMetaDataPath, nameNew + extension)

                os.rename(dataOldPath, dataNewPath)

                dataCount += 1

    print("All NFT files stored and sorted to the Complete_Collection folder in {}".format(config.save_path))

if __name__ == '__main__':
    reformatBatches()
