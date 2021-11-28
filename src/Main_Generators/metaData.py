# Some code in this file was generously sponsored by the amazing team over at SolSweepers!
# Feel free to check out their amazing project and see how they are using Blend_My_NFTs:
# https://discord.gg/QTT7dzcuVs

# Purpose:
# This file returns the specified meta data format to the Exporter.py for a given NFT DNA.

import bpy
import os
import sys
import time
import json
import importlib

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
sys.modules.values()

from src import config

importlib.reload(config)


def returnMetaData(metaDataType, metaDataDict, name, a, dnaDictionary):
    '''
    This function exports formatted meta data based on the metaDataType variable in config.py
    '''

    if metaDataType == "DEFAULT":
        metaDataDict["name"] = name
        metaDataDict["description"] = config.metaDataDescription
        metaDataDict["NFT_DNA"] = a
        metaDataDict["NFT_Variants"] = dnaDictionary

    elif metaDataType == "SOL":
        metaDataDict["name"] = config.nftName
        metaDataDict["symbol"] = ""
        metaDataDict["description"] = config.metaDataDescription
        metaDataDict["seller_fee_basis_points"] = None
        metaDataDict["image"] = ""
        metaDataDict["animation_url"] = ""
        metaDataDict["external_url"] = ""

        attributes = []

        for i in dnaDictionary:
            dictionary = {
                "trait_type": i,
                "value": dnaDictionary[i]
            }

            attributes.append(dictionary)

        metaDataDict["attributes"] = attributes
        metaDataDict["collection"] = {
            "name": "",
            "family": ""
        }
        metaDataDict["properties"] = {"files": [{"uri": "", "type": ""}],
                                      "category": "",
                                      "creators": [{"address": "", "share": None}]
                                      }
        metaDataDict["category"] = ""
        metaDataDict["creators"] = [{
            "address": "",
            "share": None
        }]


    elif metaDataType == "ADA":
        metaDataDict["721"] = {
            "<policy_id>": {
                "<asset_name>": {
                    "name": name,
                    "image": "",
                    "mediaType": "",
                    "description": config.metaDataDescription,
                    "files": [{
                        "name": "",
                        "mediaType": "",
                        "src": "",
                        "NFT_Variants": dnaDictionary,
                        "NFT_DNA": a
                    }]
                }
            },
            "version": "1.0"
        }

    elif metaDataType == "ERC721":
        metaDataDict["title"] = name
        metaDataDict["type"] = ""
        metaDataDict["properties"] = {"NFT_Variants": dnaDictionary,
                                      "description": config.metaDataDescription,
                                      "NFT_DNA": a}

if __name__ == '__main__':
    returnMetaData()
