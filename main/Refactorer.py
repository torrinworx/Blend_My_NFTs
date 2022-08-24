# Purpose:
# This file goes through all batches, renames, and sorts all nft files to a Complete_Collection folder in Blend_My_NFTs

import bpy
import os
import json
import shutil

from .Helpers import bcolors, removeList, remove_file_by_extension


def reformatNFTCollection(refactor_panel_input):
    completeCollPath = os.path.join(refactor_panel_input.save_path, "Blend_My_NFTs Output", "Complete_Collection")

    if not os.path.exists(completeCollPath):
        os.mkdir(completeCollPath)

    batchListDirty = os.listdir(refactor_panel_input.nftBatch_save_path)
    batchList = remove_file_by_extension(batchListDirty)
    collection_info = {"Total Time": 0}

    for folder in batchList:
        batch_info = json.load(open(os.path.join(refactor_panel_input.nftBatch_save_path, folder, "batch_info.json")))
        collection_info[os.path.basename(folder)] = batch_info
        collection_info["Total Time"] = collection_info["Total Time"] + batch_info["Batch Render Time"]

        fileListDirty = os.listdir(os.path.join(refactor_panel_input.nftBatch_save_path, folder))
        filelist = remove_file_by_extension(fileListDirty)

        for mediaTypeFolder in filelist:
            if mediaTypeFolder != "batch_info.json":
                mediaTypeFolderDir = os.path.join(refactor_panel_input.nftBatch_save_path, folder, mediaTypeFolder)

                for i in os.listdir(mediaTypeFolderDir):
                    destination = os.path.join(completeCollPath, mediaTypeFolder)
                    if not os.path.exists(destination):
                        os.makedirs(destination)

                    shutil.move(os.path.join(mediaTypeFolderDir, i), destination)

    collection_info = json.dumps(collection_info, indent=1, ensure_ascii=True)
    with open(os.path.join(completeCollPath, "collection_info.json"), 'w') as outfile:
        outfile.write(collection_info + '\n')

    print(f"All NFT files stored and sorted to the Complete_Collection folder in {refactor_panel_input.save_path}")

    shutil.rmtree(refactor_panel_input.nftBatch_save_path)

