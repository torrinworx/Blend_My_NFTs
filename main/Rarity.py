# Purpose:
# This file sorts the Variants in DNA slots based on the rarity value set in the name.

import bpy
import random

def createDNArarity(hierarchy):
    """
    Sorts through DataDictionary and appropriately weights each variant based on their rarity percentage set in Blender
    ("rarity" in DNA_Generator). Then
    """
    singleDNA = ""

    for i in hierarchy:
        number_List_Of_i = []
        rarity_List_Of_i = []
        count = 0
        ifZeroBool = None

        for k in hierarchy[i]:
            number = hierarchy[i][k]["number"]
            number_List_Of_i.append(number)

            rarity = hierarchy[i][k]["rarity"]
            rarity_List_Of_i.append(float(rarity))

            count += 1

        for x in rarity_List_Of_i:
            if x == 0:
                ifZeroBool = True
            elif x != 0:
                ifZeroBool = False

        if ifZeroBool:
            variantByNum = random.choices(number_List_Of_i, k=1)
        elif not ifZeroBool:
            variantByNum = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)

        singleDNA += "-" + str(variantByNum[0])
    singleDNA = ''.join(singleDNA.split('-', 1))
    return singleDNA
