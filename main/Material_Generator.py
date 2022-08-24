# Purpose:
# The purpose of this file is to apply the materials a user sets in a given .json file to the Variant collection objects
# also specified in the .json file. The Materialized DNA is then returned in the following format: 1-1-1:1-1-1
# Where the numbers right of the ":" are the material numbers applied to the respective Variants to the left of the ":"

import bpy

import json
import random
from .Helpers import TextColors


def select_material(materialList, variant, enableRarity):
    """Selects a material from a passed material list. """
    material_List_Of_i = []  # List of Material names instead of order numbers
    rarity_List_Of_i = []
    ifZeroBool = None

    for material in materialList:
        # Material Order Number comes from index in the Material List in materials.json for a given Variant.
        # material_order_num = list(materialList.keys()).index(material)

        material_List_Of_i.append(material)

        material_rarity_percent = materialList[material]
        rarity_List_Of_i.append(float(material_rarity_percent))

    # print(f"MATERIAL_LIST_OF_I:{material_List_Of_i}")
    # print(f"RARITY_LIST_OF_I:{rarity_List_Of_i}")

    for b in rarity_List_Of_i:
        if b == 0:
            ifZeroBool = True
        elif b != 0:
            ifZeroBool = False

    if enableRarity:
        try:
            if ifZeroBool:
                selected_material = random.choices(material_List_Of_i, k=1)
            elif not ifZeroBool:
                selected_material = random.choices(material_List_Of_i, weights=rarity_List_Of_i, k=1)
        except IndexError:
            raise IndexError(
                f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                f"An issue was found within the Material List of the Variant collection '{variant}'. For more information on Blend_My_NFTs compatible scenes, "
                f"see:\n{TextColors.RESET}"
                f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
            )
    else:
        try:
            selected_material = random.choices(material_List_Of_i, k=1)
        except IndexError:
            raise IndexError(
                f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                f"An issue was found within the Material List of the Variant collection '{variant}'. For more information on Blend_My_NFTs compatible scenes, "
                f"see:\n{TextColors.RESET}"
                f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
            )

    return selected_material[0], materialList

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

def apply_materials(hierarchy, singleDNA, materialsFile, enableRarity):
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
                material_name, materialList, = select_material(materialsFile[b]['Material List'], b, enableRarity)
                material_order_num = list(materialList.keys()).index(material_name)  # Gets the Order Number of the Material
                deconstructed_MaterialDNA[a] = str(material_order_num + 1)
                complete = True
        if not complete:
            deconstructed_MaterialDNA[a] = "0"

    # This section is now incorrect and needs updating:

    # Make Attributes have the same materials:
    # Order your Attributes alphabetically, then assign each Attribute a number, starting with 0. So Attribute 'A' = 0,
    # Attribute 'B' = 1, 'C' = 2, 'D' = 3, etc. For each pair you want to equal another, add its number it to this list:
    # synced_material_attributes = [1, 2]
    #
    # first_mat = deconstructed_MaterialDNA[synced_material_attributes[0]]
    # for i in synced_material_attributes:
    #     deconstructed_MaterialDNA[i] = first_mat

    material_DNA = ""
    for a in deconstructed_MaterialDNA:
        num = "-" + str(deconstructed_MaterialDNA[a])
        material_DNA += num
    material_DNA = ''.join(material_DNA.split('-', 1))

    return f"{singleDNA}:{material_DNA}"