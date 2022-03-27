# Purpose:
# This file sorts the NFT DNA from NFTRecord.json and exports it to a given number of Batch#.json files set by nftsPerBatch
# in config.py.

import bpy
import os
import json
import random


def makeBatches(nftName, maxNFTs, nftsPerBatch, save_path, batch_json_save_path):
    Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFTs Output", "NFT_Data")
    NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")

    DataDictionary = json.load(open(NFTRecord_save_path))

    numNFTsGenerated = DataDictionary["numNFTsGenerated"]
    hierarchy = DataDictionary["hierarchy"]
    DNAList = DataDictionary["DNAList"]

    numBatches = maxNFTs / nftsPerBatch

    print(f"To generate batches of {nftsPerBatch} DNA sequences per batch, with a total of {numNFTsGenerated}"
          f" possible NFT DNA sequences, the number of batches generated will be {numBatches}")

    # Clears the Batch Data folder of Batches:
    batchList = os.listdir(batch_json_save_path)

    if batchList:
        for i in batchList:
            batch = os.path.join(batch_json_save_path, i)
            if os.path.exists(batch):
                os.remove(
                    os.path.join(batch_json_save_path, i)
                )

    i = 0
    while i < numBatches:
        batchDictionary = {}
        BatchDNAList = []

        j = 0
        while (j < nftsPerBatch) and (DNAList):
            oneDNA = random.choice(DNAList)
            BatchDNAList.append({
                oneDNA: {"Complete": False}
            })
            DNAList.remove(oneDNA)
            j += 1

        batchDictionary["NFTs_in_Batch"] = int(len(BatchDNAList))
        batchDictionary["hierarchy"] = hierarchy
        batchDictionary["BatchDNAList"] = BatchDNAList

        batchDictionaryObject = json.dumps(batchDictionary, indent=1, ensure_ascii=True)

        with open(os.path.join(batch_json_save_path, ("Batch{}.json".format(i + 1))), "w") as outfile:
            outfile.write(batchDictionaryObject)

        i += 1

    if len(DNAList) > 0:  # Add to Checks.py
        print(f"One batch could not be filled completely and will contain {len(DNAList)} NFTs.")

        incompleteBatch = {"NFTs_in_Batch": int(len(DNAList)), "hierarchy": hierarchy, "BatchDNAList": DNAList}

        incompleteBatch = json.dumps(incompleteBatch, indent=1, ensure_ascii=True)

        with open(os.path.join(batch_json_save_path, ("Batch{}.json".format(i + 1))), "w") as outfile2:
            outfile2.write(incompleteBatch)
