import bpy
import os
import re
import sys
import copy
import time
import json
import itertools
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src.main import config
from src.generators_and_sorters import DNA_Generator

importlib.reload(config)
from src.main.config import *

importlib.reload(DNA_Generator)
from src.generators_and_sorters.DNA_Generator import *

def sortRarityWeights(hierarchy, listOptionVariant, DNAList):
    '''
    Sorts through DataDictionary and appropriately weights each variant based on their rarity percentage set in Blender
    ("rarity" in DNA_Generator). Then
    '''

    for i in hierarchy:
        numChild = len(hierarchy[i])
        possibleNums = list(range(1, numChild + 1))
        listOptionVariant.append(possibleNums)

    for x in range(maxNFTs):
        def createDNA():
            dnaStr1 = ""
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

                if ifZeroBool == True:
                    variantByNum = random.choices(number_List_Of_i, k=1)
                elif ifZeroBool == False:
                    variantByNum = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)

                dnaStr1 += '-' + str(variantByNum[0])
            return dnaStr1

        dnaStr = createDNA()

        if dnaStr not in DNAList:
            dnaPushToList = ''.join(dnaStr.split('-', 1))
        else:
            createDNA()

        DNAList.append(dnaPushToList)
    return