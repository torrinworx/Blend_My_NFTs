# Purpose:
# This file goes through all batches, renames, and sorts all nft files to a Complete_Collection folder in Blend_My_NFTs

import bpy
import os
import copy
import json
import shutil
from . import Metadata

from .Constants import bcolors, removeList, remove_file_by_extension


def getNFType(nftBatch_save_path):
    images = False
    animations = False
    models = False
    metaData = False

    batch1 = sorted(remove_file_by_extension(os.listdir(nftBatch_save_path)))[0]
    batchContent = remove_file_by_extension(os.listdir(os.path.join(nftBatch_save_path, batch1)))

    if "Images" in batchContent:
        images = True
    if "Animations" in batchContent:
        animations = True
    if "Models" in batchContent:
        models = True
    if "BMNFT_metaData" in batchContent:
        metaData = True

    return images, animations, models, metaData

def getMetaDataDirty(completeMetaDataPath, i):
    """
    Retrieves a given batches data determined by renderBatch in config.py
    """

    file_name = os.path.join(completeMetaDataPath, i)
    metaDataDirty = json.load(open(file_name))

    name = metaDataDirty["name"]
    NFT_DNA = metaDataDirty["NFT_DNA"]
    NFT_Variants = metaDataDirty["NFT_Variants"]

    for i in NFT_Variants:
        x = NFT_Variants[i]
        NFT_Variants[i] = x.split("_")[0]

    return name, NFT_DNA, NFT_Variants

def sendMetaDataToJson(metaDataDict, metaDataPath, jsonName):
    jsonMetaData = json.dumps(metaDataDict, indent=1, ensure_ascii=True)
    with open(os.path.join(metaDataPath, jsonName), 'w') as outfile:
        outfile.write(jsonMetaData + '\n')

def renameMetaData(rename_MetaData_Variables):
    metaDataListOld = os.listdir(rename_MetaData_Variables.completeMetaDataPath)
    cardanoMetaDataPath = os.path.join(rename_MetaData_Variables.completeCollPath, "Cardano_metaData")
    solanaMetaDataPath = os.path.join(rename_MetaData_Variables.completeCollPath, "Solana_metaData")
    erc721MetaDataPath = os.path.join(rename_MetaData_Variables.completeCollPath, "Erc721_metaData")

    for i in metaDataListOld:
        name, NFT_DNA, NFT_Variants = getMetaDataDirty(rename_MetaData_Variables.completeMetaDataPath, i)

        file_name = os.path.splitext(i)[0]
        file_num = file_name.split("_")[1]

        if rename_MetaData_Variables.cardanoMetaDataBool:
            if not os.path.exists(cardanoMetaDataPath):
                os.mkdir(cardanoMetaDataPath)

            cardanoJsonNew = "Cardano_" + i
            cardanoNewName = name.split("_")[0] + "_" + str(file_num)

            metaDataDictCardano = Metadata.returnCardanoMetaData(cardanoNewName, NFT_DNA, NFT_Variants, rename_MetaData_Variables.custom_Fields_File, rename_MetaData_Variables.enableCustomFields, rename_MetaData_Variables.cardano_description)

            sendMetaDataToJson(metaDataDictCardano, cardanoMetaDataPath, cardanoJsonNew,)

        if rename_MetaData_Variables.solanaMetaDataBool:
            if not os.path.exists(solanaMetaDataPath):
                os.mkdir(solanaMetaDataPath)

            solanaJsonNew = "Solana_" + i
            solanaNewName = name.split("_")[0] + "_" + str(file_num)

            metaDataDictSolana = Metadata.returnSolanaMetaData(solanaNewName, NFT_DNA, NFT_Variants, rename_MetaData_Variables.custom_Fields_File, rename_MetaData_Variables.enableCustomFields, rename_MetaData_Variables.solana_description)

            sendMetaDataToJson(metaDataDictSolana, solanaMetaDataPath, solanaJsonNew)

        if rename_MetaData_Variables.erc721MetaData:
            if not os.path.exists(erc721MetaDataPath):
                os.mkdir(erc721MetaDataPath)

            erc721JsonNew = "Erc721_" + i
            erc721NewName = name.split("_")[0] + "_" + str(file_num)

            metaDataDictErc721 = Metadata.returnErc721MetaData(erc721NewName, NFT_DNA, NFT_Variants, rename_MetaData_Variables.custom_Fields_File, rename_MetaData_Variables.enableCustomFields, rename_MetaData_Variables.erc721_description)

            sendMetaDataToJson(metaDataDictErc721, erc721MetaDataPath, erc721JsonNew)
    return

def reformatNFTCollection(refactor_panel_input):
    images, animations, models, metaData = getNFType(refactor_panel_input.nftBatch_save_path)

    global completeCollPath
    global completeMetaDataPath

    completeCollPath = os.path.join(refactor_panel_input.save_path, "Blend_My_NFTs Output", "Complete_Collection")
    completeImagePath = os.path.join(completeCollPath, "Images")
    completeAnimationsPath = os.path.join(completeCollPath, "Animations")
    completeModelsPath = os.path.join(completeCollPath, "Models")
    completeMetaDataPath = os.path.join(completeCollPath, "BMNFT_metaData")

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

    batchListDirty = os.listdir(refactor_panel_input.nftBatch_save_path)
    batchList = [x for x in batchListDirty if (x not in removeList)]

    imageCount = 1
    animationCount = 1
    modelCount = 1
    dataCount = 1
    for i in batchList:
        if images:
            imagesDir = os.path.join(refactor_panel_input.nftBatch_save_path, i, "Images")
            imagesList = sorted(os.listdir(imagesDir))

            for j in imagesList:
                imageOldPath = os.path.join(refactor_panel_input.nftBatch_save_path, i, "Images", j)
                nameOldDirty = copy.deepcopy(os.path.splitext(j)[0])
                extension = copy.deepcopy(os.path.splitext(j)[1])
                nameOldClean = nameOldDirty.split("_")[0]

                nameNew = nameOldClean + "_" + str(imageCount)
                imageNewPath = os.path.join(completeImagePath, nameNew + extension)

                os.rename(imageOldPath, imageNewPath)

                imageCount += 1

        if animations:
            animationsDir = os.path.join(refactor_panel_input.nftBatch_save_path, i, "Animations")
            animationsList = sorted(os.listdir(animationsDir))
            
            for j in animationsList: 
                animationOldPath = os.path.join(refactor_panel_input.nftBatch_save_path, i, "Animations", j)
                nameOldDirty = copy.deepcopy(os.path.splitext(j)[0])
                extension = copy.deepcopy(os.path.splitext(j)[1])
                nameOldClean = nameOldDirty.split("_")[0]
    
                nameNew = nameOldClean + "_" + str(animationCount)
                animationNewPath = os.path.join(completeAnimationsPath, nameNew + extension)
    
                os.rename(animationOldPath, animationNewPath)
    
                animationCount += 1

        if models:
            modelsDir = os.path.join(refactor_panel_input.nftBatch_save_path, i, "Models")
            modelsList = sorted(os.listdir(modelsDir))

            for j in modelsList:
                modelOldPath = os.path.join(refactor_panel_input.nftBatch_save_path, i, "Models", j)
                nameOldDirty = copy.deepcopy(os.path.splitext(j)[0])
                extension = copy.deepcopy(os.path.splitext(j)[1])
                nameOldClean = nameOldDirty.split("_")[0]

                nameNew = nameOldClean + "_" + str(modelCount)
                modelsNewPath = os.path.join(completeModelsPath, nameNew + extension)

                os.rename(modelOldPath, modelsNewPath)

                modelCount += 1

        if metaData:
            dataDir = os.path.join(refactor_panel_input.nftBatch_save_path, i, "BMNFT_metaData")
            dataList = sorted(os.listdir(dataDir))

            for j in dataList:
                dataOldPath = os.path.join(refactor_panel_input.nftBatch_save_path, i, "BMNFT_metaData", j)
                nameOldDirty = copy.deepcopy(os.path.splitext(j)[0])
                extension = copy.deepcopy(os.path.splitext(j)[1])
                nameOldClean = nameOldDirty.split("_")[0]

                nameNew = nameOldClean + "_" + str(dataCount)
                dataNewPath = os.path.join(completeMetaDataPath, nameNew + extension)
                os.rename(dataOldPath, dataNewPath)

                BMFNT_Meta = json.load(open(dataNewPath))
                name = BMFNT_Meta["name"].split("_")[0]
                BMFNT_Meta["name"] = name + "_" + str(dataCount)
                jsonMetaData = json.dumps(BMFNT_Meta, indent=1, ensure_ascii=True)

                with open(dataNewPath, 'w') as outfile:
                    outfile.write(jsonMetaData + '\n')

                dataCount += 1

    print(f"All NFT files stored and sorted to the Complete_Collection folder in {refactor_panel_input.save_path}")

    class rename_MetaData_Variables:
        completeCollPath = completeCollPath
        completeMetaDataPath = completeMetaDataPath

        cardanoMetaDataBool = refactor_panel_input.cardanoMetaDataBool
        solanaMetaDataBool = refactor_panel_input.solanaMetaDataBool
        erc721MetaData = refactor_panel_input.erc721MetaData

        custom_Fields_File = refactor_panel_input.custom_Fields_File
        enableCustomFields = refactor_panel_input.enableCustomFields


        cardano_description = refactor_panel_input.cardano_description
        solana_description = refactor_panel_input.solana_description
        erc721_description = refactor_panel_input.erc721_description


    renameMetaData(rename_MetaData_Variables)

    shutil.rmtree(refactor_panel_input.nftBatch_save_path)
