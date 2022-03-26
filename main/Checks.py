# Purpose:
# The purpose of this file is to check the NFTRecord.json for duplicate NFT DNA and returns any found in the console.
# It also checks the percentage each variant is chosen in the NFTRecord, then compares it with its rarity percentage
# set in the .blend file.

# This file is provided for transparency. The accuracy of the rarity values you set in your .blend file as outlined in
# the README.md file are dependent on the maxNFTs, and the maximum number of combinations of your NFT collection.

import bpy
import os
import json
from collections import Counter, defaultdict


class bcolors:
    """
    The colour of console messages.
    """

    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    ERROR = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR

# Checks:
def check_Scene():
    """
    Checks if Blender file Scene follows the Blend_My_NFTs conventions. If not, raises error with all instances of
    violations.
    """

def check_Rarity(hierarchy, DNAList, save_path):
    """Checks rarity percentage of each Variant, then sends it to RarityData.json in NFT_Data folder."""
    numNFTsGenerated = len(DNAList)

    attributeNames = []
    numDict = defaultdict(list)

    hierarchy.keys()

    for i in DNAList:
        dnaSplitList = i.split("-")

        for j, k in zip(dnaSplitList, hierarchy.keys()):
            numDict[k].append(j)

    numDict = dict(numDict)

    for i in numDict:
        count = dict(Counter(numDict[i]))
        numDict[i] = count

    fullNumName = {}

    for i in hierarchy:
        fullNumName[i] = {}
        for j in hierarchy[i]:
            variantNum = hierarchy[i][j]["number"]

            fullNumName[i][variantNum] = j

    completeData = {}

    for i, j in zip(fullNumName, numDict):
        x = {}

        for k in fullNumName[i]:

            for l in numDict[j]:
                if l == k:
                    name = fullNumName[i][k]
                    num = numDict[j][l]
                    x[name] = [(str(round(((num/numNFTsGenerated)*100), 2)) + "%"), str(num)]

        completeData[i] = x

    print(completeData)

    print(bcolors.OK + "Rarity Checker is active. These are the percentages for each variant per attribute you set in your .blend file:" + bcolors.RESET)

    for i in completeData:
        print(i + ":")
        for j in completeData[i]:
            print("   " + j + ": " + completeData[i][j][0] + "   Occurrences: " + completeData[i][j][1])

    jsonMetaData = json.dumps(completeData, indent=1, ensure_ascii=True)

    with open(os.path.join(save_path, "RarityData.json"), 'w') as outfile:
        outfile.write(jsonMetaData + '\n')
    path = os.path.join(save_path, "RarityData.json")
    print(bcolors.OK + f"Rarity Data has been saved to {path}." + bcolors.RESET)

def check_Duplicates(DNAList):
    """Checks if there are duplicates in DNAList before NFTRecord.json is sent to JSON file."""

    duplicates = 0
    seen = set()

    for x in DNAList:
        if x in seen:
            print(x)
            duplicates += 1
        seen.add(x)

    print(f"NFTRecord.json contains {duplicates} duplicate NFT DNA.")

def check_FailedBatches(batch_json_save_path):
    batch_folders = os.listdir(batch_json_save_path)
    fail_state = False
    failed_batch = None
    failed_dna = None
    failed_dna_index = None

    for i in batch_folders:
        batch = json.load(open(os.path.join(batch_json_save_path, i)))
        NFTs_in_Batch = batch["NFTs_in_Batch"]
        if "Generation Save" in batch:
            dna_generated = batch["Generation Save"][-1]["DNA Generated"]
            if dna_generated < NFTs_in_Batch:
                fail_state = True
                failed_batch = int(i.removeprefix("Batch").removesuffix(".json"))
                failed_dna = dna_generated


    return fail_state, failed_batch, failed_dna, failed_dna_index


# Raise Errors:
def raise_Error_ScriptIgnore():
    """Checks if Script_Ignore collection exists, if not raises error."""

    try:
        scriptIgnore = bpy.data.collections["Script_Ignore"]
        return scriptIgnore
    except KeyError:
        raise KeyError(
            f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
            f"Script_Ignore collection not found in Blender scene. Please add the Script_Ignore "
            f"collection to Blender scene or ensure the spelling is exactly 'Script_Ignore'. For more information, "
            f"see:\n{bcolors.RESET}"
            f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n{bcolors.RESET}"
        )

def raise_Error_numBatches(maxNFTs, nftsPerBatch):
    """Checks if number of Batches is less than maxNFTs, if not raises error."""

    try:
        numBatches = maxNFTs / nftsPerBatch
        return numBatches
    except ZeroDivisionError:
        print(f"{bcolors.ERROR} ERROR:\nnftsPerBatch in config.py needs to be a positive integer. {bcolors.RESET}")
        raise ZeroDivisionError(
            f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
            f"The number of combinations is less than the number of \n{bcolors.RESET}"
        )

def raise_Error_ZeroCombinations(combinations):
    """Checks if combinations is greater than 0, if so, raises error."""
    if combinations == 0:
        raise ValueError(
            f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
            f"The number of all possible combinations is ZERO. Please review your Blender scene and ensure it follows "
            f"the naming conventions and scene structure. For more information, "
            f"see:\n{bcolors.RESET}"
            f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n{bcolors.RESET}"
        )

def raise_Error_numBatchesGreaterThan(numBatches):
    if numBatches < 1:
        raise ValueError(
            f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
            f"The number of Batches is less than 1. Please review your Blender scene and ensure it follows "
            f"the naming conventions and scene structure. For more information, "
            f"see:\n{bcolors.RESET}"
            f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n{bcolors.RESET}"
        )

# Raise Warnings:

def raise_Warning_maxNFTs(nftsPerBatch, maxNFTs):
    """

    """

    if nftsPerBatch > maxNFTs:
        raise (
            f"\n{bcolors.WARNING}Blend_My_NFTs Warning:\n"
            f"The number of NFTs Per Batch you set is smaller than the NFT Collection Size you set.\n{bcolors.RESET}"
        )
