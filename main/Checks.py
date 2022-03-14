# Purpose:
# The purpose of this file is to check the NFTRecord.json for duplicate NFT DNA and returns any found in the console.
# It also checks the percentage each variant is chosen in the NFTRecord, then compares it with its rarity percentage
# set in the .blend file.

# This file is provided for transparency. The accuracy of the rarity values you set in your .blend file as outlined in
# the README.md file are dependent on the maxNFTs, and the maximum number of combinations of your NFT collection.


import bpy
import os
import sys
import json
import importlib
from collections import Counter
from collections import defaultdict


class bcolors:
    """
    The colour of console messages.
    """

    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    ERROR = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR


# Rarity Check
def check_Rarity(hierarchy, DNAList, save_path):
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

if __name__ == '__main__':
    check_Rarity()
    check_Duplicates()
