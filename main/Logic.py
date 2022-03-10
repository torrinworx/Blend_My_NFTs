# Purpose:
# The purpose of this file is to add logic and rules to the DNA that are sent to the NFTRecord.json file in DNA_Generator.py

import bpy
import os
import sys
import json
import random
import importlib
import collections

from . import metaData

importlib.reload(metaData)
removeList = [".gitignore", ".DS_Store"]


def isAttorVar(hierarchy, items_List):
    items_returned = collections.defaultdict(list)
    for i in items_List:
        for j in hierarchy:
            if i == j:  # If i is an Attribute, add all i Variants to dictionary.
                items_returned[i] = list(hierarchy[j].keys())
                items_returned[i].append("Empty")

            if i in list(hierarchy[j].keys()):
                items_returned[j].append(i)

    # Check if all variants in an attribute were included, if so, add "Empty" variant.
    for i in items_returned:
        if list(items_returned[i]) == list(hierarchy[i].keys()):
            items_returned[i].append("Empty")

    return dict(items_returned)

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

        num_List[i] = variant_num_list
    return num_List

def rar_selectVar(hierarchy, items_List, deconstructed_DNA):

    for attribute in items_List:

        a_attribute_index = getAttIndex(hierarchy, attribute)

        selected_variants = items_List[attribute]
        hierarchy_selected_variants = list(hierarchy[attribute])

        left_over_variants = [x for x in hierarchy_selected_variants if x not in selected_variants]
        print(left_over_variants)

        if not left_over_variants:
            deconstructed_DNA[int(a_attribute_index)] = "0"
        else:
            number_List_Of_i = []
            rarity_List_Of_i = []
            ifZeroBool = None
            variantNum = None

            for a in left_over_variants:
                number = a.split("_")[1]
                rarity = a.split("_")[2]

                number_List_Of_i.append(int(number))
                rarity_List_Of_i.append(float(rarity))

            for x in rarity_List_Of_i:
                if x == 0:
                    ifZeroBool = True
                elif x != 0:
                    ifZeroBool = False

            if ifZeroBool:
                variantNum = random.choices(number_List_Of_i, k=1)

            if not ifZeroBool:
                variantNum = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)

            deconstructed_DNA[int(a_attribute_index)] = str(variantNum[0])

    return deconstructed_DNA

def logicafyDNAList(DNAList, hierarchy, logicFile):
    logicFile = json.load(open(logicFile))
    LogicDNAList_deconstructed = []
    items_List1 = []
    items_List2 = []

    for a in logicFile:
        items_List1 = isAttorVar(hierarchy, logicFile[a]["Items-1"])
        items_List2 = isAttorVar(hierarchy, logicFile[a]["Items-2"])

    # Convert String Attributes to DNA Index number, and String Variants to Order number. Variant == 0 if Empty given.
    num_List1 = items_to_num(hierarchy, items_List1)
    num_List2 = items_to_num(hierarchy, items_List2)

    for a in DNAList:
        deconstructed_DNA = a.split("-")
        for b in logicFile:
            if logicFile[b]["Rule"] == "Never with":
                rand_bool = bool(random.getrandbits(1))

                if rand_bool:
                    deconstructed_DNA = rar_selectVar(hierarchy, items_List2, deconstructed_DNA)

                if not rand_bool:
                    deconstructed_DNA = rar_selectVar(hierarchy, items_List1, deconstructed_DNA)

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
        for b in a:
            num = "-" + str(b)
            reconstructed_DNA += num
        LogicDNAList.append(''.join(reconstructed_DNA.split('-', 1)))
    return LogicDNAList


if __name__ == '__main__':
    logicafyDNAList()
