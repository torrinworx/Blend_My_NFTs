# Purpose:
# This file goes through all batches, renames, and sorts all nft files to a Complete_Collection folder in Blend_My_NFTs

import os
import json
import shutil

from .helpers import remove_file_by_extension


def reformat_nft_collection(refactor_panel_input):
    complete_coll_path = os.path.join(refactor_panel_input.save_path, "Blend_My_NFTs Output", "Complete_Collection")

    if not os.path.exists(complete_coll_path):
        os.mkdir(complete_coll_path)

    batch_list_dirty = os.listdir(refactor_panel_input.nft_batch_save_path)
    batch_list = remove_file_by_extension(batch_list_dirty)
    collection_info = {"Total Time": 0}

    for folder in batch_list:
        batch_info = json.load(open(os.path.join(refactor_panel_input.nft_batch_save_path, folder, "batch_info.json")))
        collection_info[os.path.basename(folder)] = batch_info
        collection_info["Total Time"] = collection_info["Total Time"] + batch_info["Batch Render Time"]

        file_list_dirty = os.listdir(os.path.join(refactor_panel_input.nft_batch_save_path, folder))
        filelist = remove_file_by_extension(file_list_dirty)

        for mediaTypeFolder in filelist:
            if mediaTypeFolder != "batch_info.json":
                media_type_folder_dir = os.path.join(refactor_panel_input.nft_batch_save_path, folder, mediaTypeFolder)

                for i in os.listdir(media_type_folder_dir):
                    destination = os.path.join(complete_coll_path, mediaTypeFolder)
                    if not os.path.exists(destination):
                        os.makedirs(destination)

                    shutil.move(os.path.join(media_type_folder_dir, i), destination)

    collection_info = json.dumps(collection_info, indent=1, ensure_ascii=True)
    with open(os.path.join(complete_coll_path, "collection_info.json"), 'w') as outfile:
        outfile.write(collection_info + '\n')

    print(f"All NFT files stored and sorted to the Complete_Collection folder in {refactor_panel_input.save_path}")

    shutil.rmtree(refactor_panel_input.nft_batch_save_path)
