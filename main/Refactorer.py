# Purpose:
# This file goes through all batches, renames, and sorts all nft files to a Complete_Collection folder in Blend_My_NFTs

import bpy
import os
import json
import shutil

from .Constants import bcolors, removeList, remove_file_by_extension


def moveAll(completeCollPath: str, batch_path: str, folder_type_list: list):
    """
    Creates all Completed_Collection sub folders and moves all files of a given batch to the appropriate file folders.
    """

    # Create folder_type_dict and make dirs from batch_folder_list if they exist in a given batch:
    for folder_type in folder_type_list:
        folder_type_old_path = os.path.join(batch_path, folder_type)
        folder_type_new_path = os.path.join(completeCollPath, folder_type)

        if os.path.isdir(folder_type_old_path):
            if not os.path.isdir(folder_type_new_path):
                os.mkdir(folder_type_new_path)

            file_list = sorted(os.listdir(folder_type_old_path))
            for item in file_list:
                file_list_dir_old = os.path.join(folder_type_old_path, item)
                file_list_dir_new = os.path.join(folder_type_new_path, item)

                os.rename(file_list_dir_old, file_list_dir_new)


def reformatNFTCollection(refactor_panel_input):
    completeCollPath = os.path.join(refactor_panel_input.save_path, "Blend_My_NFTs Output", "Complete_Collection")
    if not os.path.exists(completeCollPath):
        os.mkdir(completeCollPath)

    batchListDirty = os.listdir(refactor_panel_input.nftBatch_save_path)
    batchList = sorted([x for x in batchListDirty if (x not in removeList)])

    collection_info = {"Total Time": 0}
    for batch in batchList:
        folder_type_list = [
            "Images",
            "Animations",
            "Models",
            "Cardano_metadata",
            "Solana_metadata",
            "Erc721_metadata",
            "BMNFT_metaData"
        ]

        batch_path = os.path.join(refactor_panel_input.nftBatch_save_path, batch)

        moveAll(completeCollPath, batch_path, folder_type_list)

        batch_info = json.load(open(os.path.join(refactor_panel_input.nftBatch_save_path, batch, "batch_info.json")))
        collection_info[os.path.basename(batch)] = batch_info

        collection_info["Total Time"] = collection_info["Total Time"] + batch_info["Batch Render Time"]

    collection_info = json.dumps(collection_info, indent=1, ensure_ascii=True)
    with open(os.path.join(completeCollPath, "collection_info.json"), 'w') as outfile:
        outfile.write(collection_info + '\n')

    print(f"All NFT files stored and sorted to the Complete_Collection folder in {refactor_panel_input.save_path}")

    shutil.rmtree(refactor_panel_input.nftBatch_save_path)
