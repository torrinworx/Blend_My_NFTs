# Purpose:
# This file applies DNA Rules set by user
from multiprocessing import Condition
from operator import truediv
import bpy
import os
import sys
import random
import importlib
from functools import partial


dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src import config

importlib.reload(config)

from src.Main_Generators import DNA_Generator

importlib.reload(DNA_Generator)


# if this be False then all DNA Generation will regenerate every time condition Fail. If its true it just fix the failed DNA Part.
fixSubDNA = True


def CheckDNA(dna, hierarchy):

    dnaRules = config.dnaRules

    isRuleValid = None
    for dnaRule in dnaRules:
        # Find the first item collection
        # First item is for compare so we start from second one

        for index, rule in enumerate(dnaRule):
            isRuleValid, newDNA = CheckRule(index, rule, dna, hierarchy)
            if newDNA != dna:
                dna = newDNA
                CheckDNA(dna, hierarchy)

            # No need to check rules
            if index == 0 and not isRuleValid:
                isRuleValid = True
                break
            if isRuleValid == False:
                break

        if isRuleValid == False:
            break
    print("Check dna Result")
    print(isRuleValid)
    print(index)
    return isRuleValid, dna


def CheckRule(index, rule, dna, hierarchy):
    condition = None

    if index != 0:
        condition = rule[0]
        rule = rule[1:]

    dnaArray = list(dna.split("-"))
    dnaArray = [int(s) for s in dnaArray]

    compareCollectionIndex = list(hierarchy.keys()).index(rule[0])

    # Get items in collection
    collectionSubItems = list(
        hierarchy[list(hierarchy.keys())[compareCollectionIndex]].keys()
    )

    ruleIndexs = []
    for subItemIndex, collectionSubItem in enumerate(collectionSubItems):
        subItemName = collectionSubItem[0 : collectionSubItem.index("_")]
        for ruleIndex, ruleName in enumerate(rule[1:]):
            finded = False
            realRuleName = ruleName.replace("*", "")
            if ruleName.startswith("*") and ruleName.endswith("*"):
                if subItemName.find(realRuleName) is not -1:
                    finded = True
                # Add +1 cuz dna starts from 1
            elif ruleName.startswith("*"):
                if subItemName.startswith(realRuleName) == -1:
                    finded = True
            elif ruleName.endswith("*"):
                if subItemName.endswith(realRuleName) == -1:
                    finded = True
            else:
                if subItemName == ruleName:
                    finded = True
                # Add +1 cuz dna starts from 1
            if finded:
                ruleIndexs.append(subItemIndex + 1)

    # print(ruleIndexs)
    # print(dnaArray[compareCollectionIndex])

    # do we need to check rules for this DNA
    result = True
    if dnaArray[compareCollectionIndex] in ruleIndexs:
        if condition == False:
            if fixSubDNA and index != 0:
                print("Fixing DNA")
                print(dnaToString(dna, hierarchy))
                print("-------")
                dna = FixDNAItem(
                    collectionSubItems,
                    ruleIndexs,
                    condition,
                    dna,
                    compareCollectionIndex,
                )
                result = True
            else:
                result = False
    else:
        if condition == False:
            result = True
        else:
            if fixSubDNA and index != 0:
                print("Fixing DNA")
                print(dnaToString(dna, hierarchy))
                print("-------")
                dna = FixDNAItem(
                    collectionSubItems,
                    ruleIndexs,
                    condition,
                    dna,
                    compareCollectionIndex,
                )
                # print(dnaToString(dna, hierarchy))
                result = True
            else:
                result = False

    return result, dna


# Fixing Sub DNA Item
def FixDNAItem(collectionSubItems, ruleIndexes, condition, dna, compareCollectionIndex):

    rarity_List_Of_i = []
    for subItemIndex, collectionSubItem in enumerate(collectionSubItems):
        subItemrarity = collectionSubItem.split("_")[2]

        if ((subItemIndex + 1) in ruleIndexes) is not condition:
            subItemrarity = 0
        # print(subItemrarity)
        rarity_List_Of_i.append(float(subItemrarity))

    if not config.enableRarity:
        selectedItem = random.choices(collectionSubItems, k=1)
    else:
        selectedItem = random.choices(collectionSubItems, weights=rarity_List_Of_i, k=1)

    newDNAIndex = collectionSubItems.index(str(selectedItem[0])) + 1
    dnaArray = dna.split("-")
    dnaArray[compareCollectionIndex] = newDNAIndex
    dnaArray = [str(dna) for dna in dnaArray]
    newDNAArray = "-".join(dnaArray)
    print(
        "DNA Changed. New Index:"
        + str(collectionSubItems.index(str(selectedItem[0])))
        + ",Name"
        + str(selectedItem[0])
    )
    return newDNAArray


# Convert DNA TO String
def dnaToString(dna, hierarchy):
    dnaArray = list(dna.split("-"))
    dnaArray = [int(s) for s in dnaArray]
    dnaString = ""
    for index, collection in enumerate(hierarchy):
        dnaString += str(collection) + ":"

        itemName = list(hierarchy[list(hierarchy.keys())[index]].keys())[
            dnaArray[index] - 1
        ]
        dnaString += itemName[0 : itemName.index("_")] + " - "

    return dnaString
