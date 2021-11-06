import bpy
import os
import sys
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src.main import config
importlib.reload(config)
from src.main.config import *


coll = bpy.context.scene.collection
scriptIgnore = bpy.data.collections["Script_Ignore"]
listAllCollInScene = []
listAllCollections = []

def traverse_tree(t):
    yield t
    for child in t.children:
        yield from traverse_tree(child)

for c in traverse_tree(coll):
    listAllCollInScene.append(c)

def listSubIgnoreCollections():
  def getParentSubCollections(collection):
     yield collection
     for child in collection.children:
        yield from getParentSubCollections(child)
  collList = []
  for c in getParentSubCollections(scriptIgnore):
     collList.append(c.name)
  return collList

ignoreList = listSubIgnoreCollections()

for i in listAllCollInScene:
    if generateColors:
        if i.name in colorList:
            for j in range(len(colorList[i.name])):
                if i.name[-1].isdigit() and i.name not in ignoreList:
                    listAllCollections.append(i.name + "_" + str(j + 1))
                elif j == 0:
                    listAllCollections.append(i.name)
        elif i.name[-1].isdigit() and i.name not in ignoreList:
            listAllCollections.append(i.name + "_0")
        else:
            listAllCollections.append(i.name)
    else:
        listAllCollections.append(i.name)
listAllCollections.remove(scriptIgnore.name)
listAllCollections.remove("Master Collection")


def allScriptIgnore(collection):
    '''
    Removes all collections, sub collections in Script_Ignore collection from listAllCollections.
    '''
    for coll in list(collection.children):
        listAllCollections.remove(coll.name)
        listColl = list(coll.children)
        if len(listColl) > 0:
            allScriptIgnore(coll)
allScriptIgnore(scriptIgnore)
listAllCollections.sort()

print(listAllCollections)
