# Purpose:
# The purpose of this file is to add logic and rules to the DNA that are sent to the NFTRecord.json file in DNA_Generator.py

import bpy
import random
import collections

from .Constants import bcolors, removeList, remove_file_by_extension


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


def select_from_then_list(hierarchy, deconstructed_DNA, then_num_list, enableRarity):
    for a in then_num_list:

        a_attribute_index = getAttIndex(hierarchy, a)

        selected_variants = then_num_list[a]
        hierarchy_selected_variants = list(hierarchy[a])

        # Left over variants are removed for when the user only specifies individual variants instead of whole attributes
        left_over_variants = [x for x in hierarchy_selected_variants if x not in selected_variants]

        # If 'a' is a full attribute:
        if not left_over_variants:
            deconstructed_DNA[int(a_attribute_index)] = "0"

        # If 'a' is only part of an attribute (the user specified variant(s) from the attribute that don't add to the full
        # attribute):
        else:
            number_List_Of_i = []
            rarity_List_Of_i = []
            ifZeroBool = None
            variantNum = None

            for b in left_over_variants:
                number = b.split("_")[1]
                rarity = b.split("_")[2]

                number_List_Of_i.append(int(number))
                rarity_List_Of_i.append(float(rarity))

            for b in rarity_List_Of_i:
                if b == 0:
                    ifZeroBool = True
                elif b != 0:
                    ifZeroBool = False

            if enableRarity:
                try:
                    if ifZeroBool:
                        variantNum = random.choices(number_List_Of_i, k=1)
                    elif not ifZeroBool:
                        variantNum = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)
                except IndexError:
                    raise IndexError(
                        f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
                        f"An issue was found within the Attribute collection '{a}'. For more information on Blend_My_NFTs compatible scenes, "
                        f"see:\n{bcolors.RESET}"
                        f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
                    )
            else:
                try:
                    variantNum = random.choices(number_List_Of_i, k=1)
                except IndexError:
                    raise IndexError(
                        f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
                        f"An issue was found within the Attribute collection '{a}'. For more information on Blend_My_NFTs compatible scenes, "
                        f"see:\n{bcolors.RESET}"
                        f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
                    )
            deconstructed_DNA[int(a_attribute_index)] = str(variantNum[0])
    return deconstructed_DNA


def reconstructDNA(deconstructedDNA):
    reconstructed_DNA = ""
    for a in deconstructedDNA:
        num = "-" + str(a)
        reconstructed_DNA += num
    return (''.join(reconstructed_DNA.split('-', 1)))


def check_if_dna_violates_rules(hierarchy, deconstructed_DNA, if_num_list, then_num_list):
    """Returns True if singleDNA violates Rules stated in a Logic.json file."""
    violates_rule = None

    # Strips empty variants if full attribute collection
    for i in if_num_list:
        var_list = if_num_list[i]
        if "0" in var_list:
            var_list.remove("0")
        if_num_list[i] = var_list

    for a in if_num_list:
        for b in then_num_list:
            # The attributes slot value from the DNA given 'a' from if_num_list and 'b' from then_num_list:
            attribute_slot_value_IF = str(deconstructed_DNA[getAttIndex(hierarchy, a)])
            attribute_slot_value_THEN = str(deconstructed_DNA[getAttIndex(hierarchy, b)])

            if attribute_slot_value_IF in if_num_list[a] and attribute_slot_value_THEN in then_num_list[b]:
                violates_rule = True
                return violates_rule
            else:
                violates_rule = False
    return violates_rule


# Main Function
def logicafyDNAsingle(hierarchy, singleDNA, logicFile, enableRarity):

    deconstructed_DNA = singleDNA.split("-")
    didReconstruct = True
    originalDNA = str(singleDNA)

    while didReconstruct:
        didReconstruct = False
        for rule in logicFile:
            # Items from 'IF' key for a given rule
            if_list = isAttorVar(hierarchy, logicFile[rule]["IF"])
            if_num_list = items_to_num(if_list)

            # Items from 'THEN' key for a given rule
            then_list = isAttorVar(hierarchy, logicFile[rule]["THEN"])
            then_num_list = items_to_num(then_list)

            if check_if_dna_violates_rules(hierarchy, deconstructed_DNA, if_num_list, then_num_list):
                deconstructed_DNA = select_from_then_list(hierarchy, deconstructed_DNA, then_num_list, enableRarity)

                newDNA = reconstructDNA(deconstructed_DNA)
                if newDNA != originalDNA:
                    originalDNA = str(newDNA)
                    didReconstruct = True
                    break

    return str(reconstructDNA(deconstructed_DNA))
