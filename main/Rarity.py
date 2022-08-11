# Purpose:
# This file sorts the Variants in DNA slots based on the rarity value set in the name.

import bpy
import random

from .Constants import bcolors, removeList, remove_file_by_extension


def createDNArarity(hierarchy):
    """
    Sorts through DataDictionary and appropriately weights each variant based on their rarity percentage set in Blender
    ("rarity" in DNA_Generator). Then
    """
    singleDNA = ""

    for i in hierarchy:
        number_List_Of_i = []
        rarity_List_Of_i = []
        ifZeroBool = None

        for k in hierarchy[i]:
            number = hierarchy[i][k]["number"]
            number_List_Of_i.append(number)

            rarity = hierarchy[i][k]["rarity"]
            rarity_List_Of_i.append(float(rarity))

        for x in rarity_List_Of_i:
            if x == 0:
                ifZeroBool = True
            elif x != 0:
                ifZeroBool = False

        try:
            if ifZeroBool:
                variantByNum = random.choices(number_List_Of_i, k=1)
            elif not ifZeroBool:
                variantByNum = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)
        except IndexError:
            raise IndexError(
                f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
                f"An issue was found within the Attribute collection '{i}'. For more information on Blend_My_NFTs compatible scenes, "
                f"see:\n{bcolors.RESET}"
                f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
            )

        singleDNA += "-" + str(variantByNum[0])
    singleDNA = ''.join(singleDNA.split('-', 1))
    return singleDNA
