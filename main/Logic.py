# Purpose:
# The purpose of this file is to add logic and rules to the DNA that are sent to the NFTRecord.json file in DNA_Generator.py

import bpy
import os
import sys
import json
import random
import importlib

from . import metaData

importlib.reload(metaData)

removeList = [".gitignore", ".DS_Store"]


def isAttorVar(hierarchy, items_List):
    items_returned = {}

    for i in items_List:
        for j in hierarchy:
            if i == j:  # If i is an Attribute, add all i Variants to dictionary.
                items_returned[i] = list(hierarchy[j].keys())
                items_returned[i].append("Empty")

            for h in hierarchy[j]:
                if h == i:  # If i is a Variant, add i Variant and i's Attribute to dictionary.
                    items_returned[j] = [h]

    # Check if all variants in an attribute were included, if so, add "Empty" variant.
    for i in items_returned:
        if list(items_returned[i]) == list(hierarchy[i].keys()):
            items_returned[i].append("Empty")

    return items_returned

def getAttIndex(hierarchy, attribute):
    attList = list(hierarchy.keys())
    index = attList.index(attribute)
    return index

def getVarNum(variant):
    if variant == "Empty":
        num = '0'
    else:
        num = variant.split("_")[1]
    return num

def items_to_num(hierarchy, items_List):
    num_List = {}
    for i in items_List:
        variant_num_list = []

        for j in items_List[i]:
            variant_num_list.append(getVarNum(j))

        num_List[getAttIndex(hierarchy, i)] = variant_num_list


    return num_List

def logicafyDNAList(DNAList, hierarchy, logicFile):
    logicFile = json.load(open(logicFile))

    LogicDNAList_deconstructed = []

    for a in DNAList:
        deconstructed_DNA = a.split("-")
        for b in logicFile:
            items_List1 = isAttorVar(hierarchy, logicFile[b]["Items-1"])
            items_List2 = isAttorVar(hierarchy, logicFile[b]["Items-2"])

            print(items_List1)
            print(items_List2)

            # Convert String Attributes to DNA Index number, and String Variants to Order number. Variant == 0 if Empty given.
            num_List1 = items_to_num(hierarchy, items_List1)
            # ^cannot go with:
            num_List2 = items_to_num(hierarchy, items_List2)

            if logicFile[b]["Rule"] == "Never with":
                rand_bool = random.getrandbits(1) == 0
                if rand_bool == 0:
                    for c in num_List2:
                        deconstructed_DNA[c] = '0'

                if rand_bool == 1:
                    for c in num_List1:
                        deconstructed_DNA[c] = '0'

            if logicFile[b]["Rule"] == "Only with":
                for c in list(num_List2.keys()):
                    for d in num_List2[c]:
                        if deconstructed_DNA[c] not in d:
                            for e in list(num_List1.keys()):
                                deconstructed_DNA[e] = '0'
        LogicDNAList_deconstructed.append(deconstructed_DNA)

    LogicDNAList = []
    for a in LogicDNAList_deconstructed:
        reconstructed_DNA = ""
        print(a)
        for b in a:
            num = "-" + str(b)
            reconstructed_DNA += num
        LogicDNAList.append(''.join(reconstructed_DNA.split('-', 1)))
    return LogicDNAList


if __name__ == '__main__':
    logicafyDNAList()
