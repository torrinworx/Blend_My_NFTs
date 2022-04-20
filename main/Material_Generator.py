# Purpose:
# The purpose of this file is to apply the materials a user sets in a given .json file to the Variant collection objects
# also specified in the .json file. The Materialized DNA is then returned in the following format: 1-1-1:1-1-1
# Where the numbers right of the ":" are the material numbers applied to the respective Variants to the left of the ":"

import bpy

import json
import random


def select_material(materialList):
    """Selects a material from a passed material list. """

    number_List_Of_i = []
    rarity_List_Of_i = []
    ifZeroBool = None

    for material in materialList:

        material_order_num = material.split("_")[1]
        number_List_Of_i.append(material_order_num)

        material_rarity_percent = material.split("_")[1]
        rarity_List_Of_i.append(float(material_rarity_percent))

    for x in rarity_List_Of_i:
        if x == 0:
            ifZeroBool = True
            break
        elif x != 0:
            ifZeroBool = False

    if ifZeroBool:
        selected_material = random.choices(number_List_Of_i, k=1)
    elif not ifZeroBool:
        selected_material = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)

    return selected_material[0]

def get_variant_att_index(variant, hierarchy):
    variant_attribute = None

    for attribute in hierarchy:
        for variant_h in hierarchy[attribute]:
            if variant_h == variant:
                variant_attribute = attribute

    attribute_index = list(hierarchy.keys()).index(variant_attribute)
    variant_order_num = variant.split("_")[1]
    return attribute_index, variant_order_num

def match_DNA_to_Variant(hierarchy, singleDNA):
    """
    Matches each DNA number separated by "-" to its attribute, then its variant.
    """

    listAttributes = list(hierarchy.keys())
    listDnaDecunstructed = singleDNA.split('-')
    dnaDictionary = {}

    for i, j in zip(listAttributes, listDnaDecunstructed):
        dnaDictionary[i] = j

    for x in dnaDictionary:
        for k in hierarchy[x]:
            kNum = hierarchy[x][k]["number"]
            if kNum == dnaDictionary[x]:
                dnaDictionary.update({x: k})
    return dnaDictionary

def apply_materials(hierarchy, singleDNA, materialsFile):
    """
    DNA with applied material example: "1-1:1-1" <Normal DNA>:<Selected Material for each Variant>

    The Material DNA will select the material for the Variant order number in the NFT DNA based on the Variant Material
    list in the Variant_Material.json file.
    """

    singleDNADict = match_DNA_to_Variant(hierarchy, singleDNA)
    materialsFile = json.load(open(materialsFile))
    deconstructed_MaterialDNA = {}

    for a in singleDNADict:
        complete = False
        for b in materialsFile:
            if singleDNADict[a] == b:
                mat = select_material(materialsFile[b]['Material List'])
                deconstructed_MaterialDNA[a] = mat
                complete = True
        if not complete:
            deconstructed_MaterialDNA[a] = "0"

    material_DNA = ""
    for a in deconstructed_MaterialDNA:
        num = "-" + str(deconstructed_MaterialDNA[a])
        material_DNA += num
    material_DNA = ''.join(material_DNA.split('-', 1))

    return f"{singleDNA}:{material_DNA}"
