# Purpose:
# The purpose of this file is to add logic and rules to the DNA that are sent to the NFTRecord.json file in DNA_Generator.py

import bpy
import random
import collections

from .Helpers import bcolors, removeList, remove_file_by_extension, save_result


def reconstructDNA(deconstructedDNA):
    reconstructed_DNA = ""
    for a in deconstructedDNA:
        num = "-" + str(a)
        reconstructed_DNA += num
    return ''.join(reconstructed_DNA.split('-', 1))


def get_var_info(variant, hierarchy):
    # Get info for variant dict
    name = variant.split("_")[0]
    order_number = variant.split("_")[1]
    rarity_number = variant.split("_")[2]
    attribute = ""

    for a in hierarchy:
        for var in list(hierarchy[a].keys()):
            if var == variant:
                attribute = a
                break
    attribute_index = list(hierarchy.keys()).index(attribute)

    return [name, order_number, rarity_number, attribute, attribute_index]  # list of Var info sent back


def apply_rules_to_dna(hierarchy, deconstructed_DNA, if_dict, result_dict, result_dict_type, enableRarity):
    # Check if Variants in if_dict are in deconstructed_DNA, if so return if_list_selected = True:
    if_list_selected = False
    for a in deconstructed_DNA:
        attribute_index = deconstructed_DNA.index(a)
        attribute = list(hierarchy.keys())[attribute_index]

        for b in hierarchy[attribute]:
            if hierarchy[attribute][b]["number"] == a:
                a_dna_var = b

        if attribute in if_dict:
            if a_dna_var in list(if_dict[attribute].keys()):
                if_list_selected = True

    # Apply changes in accordance to Variants in 'result_dict' and 'if_list_selected' bool above:
    for a in deconstructed_DNA:
        attribute_index = deconstructed_DNA.index(a)
        attribute = list(hierarchy.keys())[attribute_index]

        if attribute in result_dict:  # Check if Attribute from DNA is in 'result_dict'

            # If 'a' is a full Attribute and Variants in if_dict not selected, set 'a' to empty (0):
            if list(result_dict[attribute].keys()) == list(hierarchy[attribute].keys()) and not if_list_selected:
                deconstructed_DNA[attribute_index] = "0"

            # If 'a' is a full Attribute and result_dict_type = "NOT", set 'a' to empty (0):
            if list(result_dict[attribute].keys()) == list(
                    hierarchy[attribute].keys()) and if_list_selected and result_dict_type == "NOT":
                deconstructed_DNA[attribute_index] = "0"

    # If Variants in if_dict are selected, set each attribute in 'result_dict' to a random or rarity selected Variant from
    # 'result_dict[attribute]' variant_list:
    if if_list_selected:

        # Invert 'items_returned' if 'NOT' rule is selected:
        if result_dict_type == "NOT":
            for a in result_dict:
                var_selected_list = list(result_dict[a].keys())  # list of variants from 'NOT'
                att_selected_list = list(hierarchy[a].keys())  # full list of variants from hierarchy attribute

                # If 'a' is not a full Attribute, invert the variants:
                if len(var_selected_list) != len(att_selected_list):
                    var_selected_list = [i for i in att_selected_list if i not in var_selected_list]

                    var_selected_list_complete = {}
                    for i in var_selected_list:
                        var_selected_list_complete[i] = get_var_info(i, hierarchy)
                    result_dict[a] = var_selected_list_complete

        for a in result_dict:
            attribute_index = list(hierarchy.keys()).index(a)
            attribute = list(hierarchy.keys())[attribute_index]

            variant_list = list(result_dict[a].keys())

            if attribute in result_dict:  # Check if Attribute from DNA is in 'then_dict'

                number_List_Of_i = []
                rarity_List_Of_i = []
                ifZeroBool = None
                variantNum = None

                for b in variant_list:
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
                deconstructed_DNA[int(attribute_index)] = str(variantNum[0])

    return deconstructed_DNA


def get_rule_break_type(hierarchy, deconstructed_DNA, if_dict, result_dict, result_dict_type):
    # Check if Variants in 'if_dict' found in deconstructed_DNA:
    if_bool = False  # True if Variant in 'deconstructed_DNA' found in 'if_dict'
    for a in if_dict:  # Attribute in 'if_dict'
        for b in if_dict[a]:  # Variant in if_dict[Attribute]
            var_order_num = str(if_dict[a][b][1])  # Order number of 'b' (Variant)
            dna_order_num = str(
                deconstructed_DNA[if_dict[a][b][4]])  # Order Number of 'b's attribute in deconstructed_DNA

            if var_order_num == dna_order_num:  # If DNA selected Variants found inside IF list variants:
                if_bool = True
                break
        else:
            continue
        break

    # Check if Variants in 'result_dict' found in deconstructed_DNA:
    full_att_bool = False
    result_bool = False  # True if Variant in 'deconstructed_DNA' found in 'result_dict'
    for a in result_dict:  # Attribute in 'result_dict'
        for b in result_dict[a]:  # Variant in if_dict[Attribute]
            var_order_num = str(result_dict[a][b][1])  # Order number of 'b' (Variant)
            dna_order_num = str(
                deconstructed_DNA[result_dict[a][b][4]])  # Order Number of 'b's attribute in deconstructed_DNA
            if var_order_num == dna_order_num:  # If DNA selected Variants found inside THEN list variants:
                if list(result_dict[a].keys()) == list(hierarchy[a].keys()):
                    full_att_bool = True
                result_bool = True
                break
        else:
            continue
        break

    # Rule Bool return summary:
    violates_rule = False

    # If Variants in 'if_dict' found in deconstructed_DNA and Variants in 'result_dict' not found in deconstructed_DNA:
    if if_bool and not result_bool:
        violates_rule = True

    elif if_bool and result_bool and result_dict_type == "NOT":
        violates_rule = True

    # If Variants in 'if_dict' not found in deconstructed_DNA, and 'result_dict' variants are found in deconstructed_DNA,
    # and they are a part of a full Attribute in 'then_dict'
    elif not if_bool and result_bool and full_att_bool:
        violates_rule = True

    # If Variants in 'if_dict' not found in deconstructed_DNA, but Variants in 'then_dict' are found in deconstructed_DNA,
    # and don't make up a full Attribute:
    # elif not if_bool and result_bool and not full_att_bool:
    #     violates_rule = False

    return violates_rule, if_bool, result_bool, full_att_bool


def create_dicts(hierarchy, rule_list_items, result_dict_type):
    # Example of output structure:
    structure = {
        "attribute1": {
            "variant1": [
                "name",
                "order_number",
                "rarity_number"
                "attribute"
                "attribute_index"
            ],
            "variant2": [
                "name",
                "order_number",
                "rarity_number"
                "attribute"
                "attribute_index"
            ]
        },
        "attribute2": {
            "variant1": [
                "name",
                "order_number",
                "rarity_number"
                "attribute"
                "attribute_index"
            ],
            "variant2": [
                "name",
                "order_number",
                "rarity_number"
                "attribute"
                "attribute_index"
            ]
        }
    }

    items_returned = collections.defaultdict(dict)
    for a in rule_list_items:
        for b in hierarchy:
            if a == b:  # If 'a' is an Attribute, add all 'a' Variants to items_returned dict.
                variant_list_of_a = list(hierarchy[a].keys())
                variant_dict_of_a = {}
                for c in variant_list_of_a:
                    variant_dict_of_a[c] = get_var_info(c, hierarchy)

                items_returned[a] = variant_dict_of_a

            if a in list(hierarchy[b].keys()):  # If 'a' is a Variant, add all info about that variant to items_returned
                items_returned[b][a] = get_var_info(a, hierarchy)

    items_returned = dict(items_returned)

    return dict(items_returned)


def logicafyDNAsingle(hierarchy, singleDNA, logicFile, enableRarity, enableMaterials):
    deconstructed_DNA = singleDNA.split("-")
    didReconstruct = True
    originalDNA = str(singleDNA)

    while didReconstruct:
        didReconstruct = False
        for rule in logicFile:
            # Items from 'IF' key for a given rule
            if_dict = create_dicts(hierarchy, logicFile[rule]["IF"], "IF")

            result_dict_type = ""
            if "THEN" in logicFile[rule]:
                result_dict_type = "THEN"

            if "NOT" in logicFile[rule]:
                result_dict_type = "NOT"

            result_dict = create_dicts(hierarchy, logicFile[rule][result_dict_type], result_dict_type)

            # Change 'then_bool' to 'result_bool'
            violates_rule, if_bool, then_bool, full_att_bool = get_rule_break_type(hierarchy, deconstructed_DNA,
                                                                                   if_dict, result_dict,
                                                                                   result_dict_type)
            if violates_rule:
                # print(f"======={deconstructed_DNA} VIOLATES RULE======")

                deconstructed_DNA = apply_rules_to_dna(
                    hierarchy, deconstructed_DNA, if_dict, result_dict, result_dict_type, enableRarity
                )

                newDNA = reconstructDNA(deconstructed_DNA)
                if newDNA != originalDNA:
                    originalDNA = str(newDNA)
                    didReconstruct = True
                    break

    return str(reconstructDNA(deconstructed_DNA))
