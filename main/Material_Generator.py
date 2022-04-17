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
            return
        elif x != 0:
            ifZeroBool = False

    if ifZeroBool:
        selected_material = random.choices(number_List_Of_i, k=1)
    elif not ifZeroBool:
        selected_material = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)

    return selected_material

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

    deconstructed_DNA = singleDNA.split("-")
    singelDNADict = match_DNA_to_Variant(hierarchy, singleDNA)

    materialsFile = json.load(open(materialsFile))

    deconstructed_MaterialDNA = {}

    for a in singelDNADict:
        for b in materialsFile:
            print(f"{singelDNADict[a]} = {b}")
            if singelDNADict[a] == b:
                deconstructed_MaterialDNA[a] = select_material(materialsFile[b]['Material List'])



        # for variant_m in materialsFile:
        #     if
        #
        #
        #         materialList = materialsFile[variant_m]['Material List']
        #         selected_material = select_material(materialList)
        #
        #         attribute_index, variant_order_num = get_variant_att_index(variant_m, hierarchy)
        #
        #         if variant_order_num == deconstructed_DNA[attribute_index]:
        #             deconstructed_MaterialDNA[attribute_index] = selected_material


    return singleDNA





    # As of now deconstructed_MaterialDNA only has variants and attribute_index's with materials applied, now add '0' (empty) material variant to each appropriate attribute slot











            # This code should be in the Exporter:
            #
            # if not materialsFile[variant]['Variant Objects']:
            #     """
            #     If objects to apply material to not specified, apply to all objects in Variant collection.
            #     """
            #
            #     for obj in bpy.data.collections[variant].all_objects:
            #         selected_object = bpy.data.objects.get(obj)
            #         selected_object.active_material = selected_material
            #
            # if materialsFile[variant]['Variant Objects']:
            #     """
            #     If objects to apply material to are specified, apply material only to objects specified withing the Variant collection.
            #     """
            #     for obj in materialsFile[variant]['Variant Objects']:
            #         selected_object = bpy.data.objects.get(obj)
            #         selected_object.active_material = selected_material

        # material_name = variant[]
        #
        # material = bpy.data.materials.get(material_name)
        # if material is None:
        #     material = bpy.data.materials.new(material_name)
        # material.use_nodes = True
        #
        # principled_bsdf = material.node_tree.nodes['Principled BSDF']
        # principled_bsdf.inputs[0].default_value = selected_colour_RGBA
        #
        # selected_object.active_material = material

