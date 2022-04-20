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

from . import DNA_Generator, get_combinations
from .Constants import bcolors, removeList, remove_file_by_extension


# Checks:
def check_Scene():  # Not complete
    """
    Checks if Blender file Scene follows the Blend_My_NFTs conventions. If not, raises error with all instances of
    violations.
    """

    script_ignore_exists = None  # True if Script_Ignore collection exists in Blender scene
    attribute_naming_conventions = None  # True if all attributes in Blender scene follow BMNFTs naming conventions
    variant_naming_conventions = None  # True if all variants in Blender scene follow BMNFTs naming conventions
    object_placing_conventions = None  # True if all objects are within either Script_Ignore or a variant collection

    hierarchy = DNA_Generator.get_hierarchy()

    # script_ignore_exists:
    try:
        scriptIgnoreCollection = bpy.data.collections["Script_Ignore"]
    except KeyError:
        raise TypeError(
            f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
            f"collection to your Blender scene and ensure the name is exactly 'Script_Ignore'. For more information, "
            f"see:"
            f"\nhttps://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n{bcolors.RESET}"
        )
    else:
        script_ignore_exists = True

    collections = bpy.context.scene.collection
    print(collections)

    # attribute_naming_conventions

def check_Rarity(hierarchy, DNAList, save_path):
    """Checks rarity percentage of each Variant, then sends it to RarityData.json in NFT_Data folder."""
    numNFTsGenerated = len(DNAList)

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

    print(
        f"\n{bcolors.OK}\n"
        f"Rarity Checker is active. These are the percentages for each variant per attribute you set in your .blend file:"
        f"\n{bcolors.RESET}"
    )

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
    fail_state = False
    failed_batch = None
    failed_dna = None
    failed_dna_index = None

    if os.path.isdir(batch_json_save_path):
        batch_folders = remove_file_by_extension(os.listdir(batch_json_save_path))

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
def raise_Error_numBatches(maxNFTs, nftsPerBatch):
    """Checks if number of Batches is less than maxNFTs, if not raises error."""

    try:
        numBatches = maxNFTs / nftsPerBatch
        return numBatches
    except ZeroDivisionError:
        raise ZeroDivisionError(
            f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
            f"The number of NFTs per Batch must be greater than ZERO."
            f"Please review your Blender scene and ensure it follows "
            f"the naming conventions and scene structure. For more information, "
            f"see:\n{bcolors.RESET}"
            f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n{bcolors.RESET}"
        )

def raise_Error_ZeroCombinations():
    """Checks if combinations is greater than 0, if so, raises error."""
    if get_combinations.get_combinations() == 0:
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

def raise_Warning_maxNFTs(nftsPerBatch, collectionSize):
    """
    Prints warning if nftsPerBatch is greater than collectionSize.
    """

    if nftsPerBatch > collectionSize:
        raise ValueError(
            f"\n{bcolors.WARNING}Blend_My_NFTs Warning:\n"
            f"The number of NFTs Per Batch you set is smaller than the NFT Collection Size you set.\n{bcolors.RESET}"
        )

def raise_Warning_collectionSize(DNAList, collectionSize):
    """
    Prints warning if BMNFTs cannot generate requested number of NFTs from a given collectionSize.
    """

    if len(DNAList) < collectionSize:
        print(f"\n{bcolors.WARNING} \nWARNING: \n"
              f"Blend_My_NFTs cannot generate {collectionSize} NFTs."
              f" Only {len(DNAList)} NFT DNA were generated."
              
              f"\nThis might be for a number of reasons:"
              f"\n  a) Rarity is preventing combinations from being generated (See https://github.com/torrinworx/Blend_My_NFTs#notes-on-rarity-and-weighted-variants).\n"
              f"\n  b) Logic is preventing combinations from being generated (See https://github.com/torrinworx/Blend_My_NFTs#logic).\n"
              f"\n  c) The number of possible combinations of your NFT collection is too low. Add more Variants or Attributes to increase the recommended collection size.\n"
              f"\n{bcolors.RESET}")
