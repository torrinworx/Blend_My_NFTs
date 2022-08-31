# Purpose:
# The purpose of this file is to apply the materials a user sets in a given .json file to the Variant collection objects
# also specified in the .json file. The Materialized DNA is then returned in the following format: 1-1-1:1-1-1
# Where the numbers right of the ":" are the material numbers applied to the respective Variants to the left of the ":"

import json
import random
import logging
import traceback
from .helpers import TextColors

log = logging.getLogger(__name__)


def select_material(material_list, variant, enable_rarity):
    """Selects a material from a passed material list. """
    material_list_of_i = []  # List of Material names instead of order numbers
    rarity_list_of_i = []
    if_zero_bool = None

    for material in material_list:
        # Material Order Number comes from index in the Material List in materials.json for a given Variant.
        # material_order_num = list(material_list.keys()).index(material)

        material_list_of_i.append(material)

        material_rarity_percent = material_list[material]
        rarity_list_of_i.append(float(material_rarity_percent))

    # print(f"MATERIAL_LIST_OF_I:{material_list_of_i}")
    # print(f"RARITY_LIST_OF_I:{rarity_list_of_i}")

    for b in rarity_list_of_i:
        if b == 0:
            if_zero_bool = True
        elif b != 0:
            if_zero_bool = False

    if enable_rarity:
        try:
            if if_zero_bool:
                selected_material = random.choices(material_list_of_i, k=1)
            elif not if_zero_bool:
                selected_material = random.choices(material_list_of_i, weights=rarity_list_of_i, k=1)
        except IndexError:
            log.error(
                    f"\n{traceback.format_exc()}"
                    f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                    f"An issue was found within the Material List of the Variant collection '{variant}'. For more "
                    f"information on Blend_My_NFTs compatible scenes, see:\n{TextColors.RESET}"
                    f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
            )
            raise IndexError()
    else:
        try:
            selected_material = random.choices(material_list_of_i, k=1)
        except IndexError:
            log.error(
                    f"\n{traceback.format_exc()}"
                    f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                    f"An issue was found within the Material List of the Variant collection '{variant}'. For more "
                    f"information on Blend_My_NFTs compatible scenes, see:\n{TextColors.RESET}"
                    f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
            )
            raise IndexError()

    return selected_material[0], material_list


def get_variant_att_index(variant, hierarchy):
    variant_attribute = None

    for attribute in hierarchy:
        for variant_h in hierarchy[attribute]:
            if variant_h == variant:
                variant_attribute = attribute

    attribute_index = list(hierarchy.keys()).index(variant_attribute)
    variant_order_num = variant.split("_")[1]
    return attribute_index, variant_order_num


def match_dna_to_variant(hierarchy, single_dna):
    """
    Matches each DNA number separated by "-" to its attribute, then its variant.
    """

    list_attributes = list(hierarchy.keys())
    list_dna_decunstructed = single_dna.split('-')
    dna_dictionary = {}

    for i, j in zip(list_attributes, list_dna_decunstructed):
        dna_dictionary[i] = j

    for x in dna_dictionary:
        for k in hierarchy[x]:
            k_num = hierarchy[x][k]["number"]
            if k_num == dna_dictionary[x]:
                dna_dictionary.update({x: k})
    return dna_dictionary


def apply_materials(hierarchy, single_dna, materials_file, enable_rarity):
    """
    DNA with applied material example: "1-1:1-1" <Normal DNA>:<Selected Material for each Variant>

    The Material DNA will select the material for the Variant order number in the NFT DNA based on the Variant Material
    list in the Variant_Material.json file.
    """

    single_dna_dict = match_dna_to_variant(hierarchy, single_dna)
    materials_file = json.load(open(materials_file))
    deconstructed_material_dna = {}

    for a in single_dna_dict:
        complete = False
        for b in materials_file:
            if single_dna_dict[a] == b:
                material_name, material_list, = select_material(materials_file[b]['Material List'], b, enable_rarity)

                # Gets the Order Number of the Material
				# We add 1 to the index because 0 is what we return on an invalid lookup. 
				# If we don't add 1 then when material index 0 is chosen randomly we will not change materials, 
				# and conversly the last material in the list will never show up
                material_order_num = (list(material_list.keys()).index(material_name))+1

                deconstructed_material_dna[a] = str(material_order_num)
                complete = True
        if not complete:
            deconstructed_material_dna[a] = "0"

    # This section is now incorrect and needs updating:

    # Make Attributes have the same materials:
    # Order your Attributes alphabetically, then assign each Attribute a number, starting with 0. So Attribute 'A' = 0,
    # Attribute 'B' = 1, 'C' = 2, 'D' = 3, etc. For each pair you want to equal another, add its number it to this list:
    # synced_material_attributes = [1, 2]
    #
    # first_mat = deconstructed_material_dna[synced_material_attributes[0]]
    # for i in synced_material_attributes:
    #     deconstructed_material_dna[i] = first_mat

    material_dna = ""
    for a in deconstructed_material_dna:
        num = "-" + str(deconstructed_material_dna[a])
        material_dna += num
    material_dna = ''.join(material_dna.split('-', 1))

    return f"{single_dna}:{material_dna}"
