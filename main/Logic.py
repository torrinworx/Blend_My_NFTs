# Purpose:
# The purpose of this file is to add logic and rules to the DNA that are sent to the NFTRecord.json file in DNA_Generator.py

import bpy
import json
import random
import collections


# Helper Functions
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

def items_to_num(items_List):
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

def reconstructDNA(deconstructedDNA):
    reconstructed_DNA = ""
    for a in deconstructedDNA:
        num = "-" + str(a)
        reconstructed_DNA += num
    return (''.join(reconstructed_DNA.split('-', 1)))

def strip_empty_variant(num_list):
    """Strips empty variants if full attribute collection. Used for processing below."""
    for i in num_list:
        var_list = num_list[i]
        if "0" in var_list:
            var_list.remove("0")
        num_list[i] = var_list
    return num_list

# Rule Checks:
def never_with_Rule_Check(hierarchy, deconstructed_DNA, num_List1, num_List2):
    """Returns True if singleDNA violates Never with Rule stated in Logic.json."""
    violates_rule = None

    num_List1 = strip_empty_variant(num_List1)
    num_List2 = strip_empty_variant(num_List2)

    for a in num_List1:
        for b in num_List2:
            if str(deconstructed_DNA[getAttIndex(hierarchy, a)]) in num_List1[a] and \
                    str(deconstructed_DNA[getAttIndex(hierarchy, b)]) in num_List2[b]:
                violates_rule = True
                return violates_rule
            else:
                violates_rule = False
    return violates_rule

def only_with_Rule_Check(hierarchy, deconstructed_DNA, num_List1, num_List2):
    """Returns True if singleDNA violates Only with Rule stated in Logic.json."""
    violates_rule = None

    for a in num_List1:
        for b in num_List2:
            if str(deconstructed_DNA[getAttIndex(hierarchy, a)]) in num_List1[a] and \
                    str(deconstructed_DNA[getAttIndex(hierarchy, b)]) not in num_List2[b]:
                violates_rule = True
                return violates_rule

            else:
                violates_rule = False
    return violates_rule

def always_with_Rule_Check(hierarchy, deconstructed_DNA, num_List1, num_List2):
    """Returns True if singleDNA violates Always with Rule stated in Logic.json."""
    violates_rule = None

    for a in num_List2:
        if str(deconstructed_DNA[getAttIndex(hierarchy, a)]) not in num_List2[a]:
            violates_rule = True
            return violates_rule
        else:
            violates_rule = False
    return violates_rule


# Main Function
def logicafyDNAsingle(hierarchy, singleDNA, logicFile):

    logicFile = json.load(open(logicFile))
    deconstructed_DNA = singleDNA.split("-")

    didReconstruct = True
    originalDNA = str(singleDNA)

    while didReconstruct:
        didReconstruct = False
        for rule in logicFile:
            items_List1 = isAttorVar(hierarchy, logicFile[rule]["Items-1"])
            items_List2 = isAttorVar(hierarchy, logicFile[rule]["Items-2"])
            num_List1 = items_to_num(items_List1)
            num_List2 = items_to_num(items_List2)

            if logicFile[rule]["Rule-Type"] == "Never with":
                if never_with_Rule_Check(hierarchy, deconstructed_DNA, num_List1, num_List2):

                    rand_bool = bool(random.getrandbits(1))

                    if rand_bool:
                        deconstructed_DNA = rar_selectVar(hierarchy, items_List2, deconstructed_DNA)

                    if not rand_bool:
                        deconstructed_DNA = rar_selectVar(hierarchy, items_List1, deconstructed_DNA)

                    newDNA = reconstructDNA(deconstructed_DNA)
                    if newDNA != originalDNA:
                        originalDNA = str(newDNA)
                        didReconstruct = True
                        break

            if logicFile[rule]["Rule-Type"] == "Only with":
                if only_with_Rule_Check(hierarchy, deconstructed_DNA, num_List1, num_List2):
                    for b in num_List1:
                        if "0" in num_List1[b]:  # If complete attribute
                            deconstructed_DNA[getAttIndex(hierarchy, b)] = "0"

                        if "0" not in num_List1[b]:  # Not complete attribute, select from other variants with rarity:
                            deconstructed_DNA = rar_selectVar(hierarchy, items_List1, deconstructed_DNA)

                    newDNA = reconstructDNA(deconstructed_DNA)
                    if newDNA != originalDNA:
                        originalDNA = str(newDNA)
                        didReconstruct = True
                        break

            if logicFile[rule]["Rule-Type"] == "Always with":
                if always_with_Rule_Check(hierarchy, deconstructed_DNA, num_List1, num_List2):
                    deconstructed_DNA = rar_selectVar(hierarchy, items_List1, deconstructed_DNA)

                    newDNA = reconstructDNA(deconstructed_DNA)
                    if newDNA != originalDNA:
                        originalDNA = str(newDNA)
                        didReconstruct = True
                        break

    return str(reconstructDNA(deconstructed_DNA))