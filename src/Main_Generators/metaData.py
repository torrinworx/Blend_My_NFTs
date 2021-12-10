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


def returnCardanoMetaData(name, description, NFT_DNA, NFT_Variants):
    metaDataDictCardano = {}

    metaDataDictCardano["721"] = {
        "<policy_id>": {
            "<asset_name>": {
                "name": name,
                "image": "",
                "mediaType": "",
                "description": description,
                "files": [{
                    "name": "",
                    "mediaType": "",
                    "src": "",
                    "NFT_Variants": NFT_Variants,
                    "NFT_DNA": NFT_DNA
                }]
            }
        },
        "version": "1.0"
    }

    return metaDataDictCardano

def returnSolanaMetaData(name, description, NFT_DNA, NFT_Variants):
    metaDataDictSolana = {}

    metaDataDictSolana["name"] = name
    metaDataDictSolana["symbol"] = ""
    metaDataDictSolana["description"] = description
    metaDataDictSolana["seller_fee_basis_points"] = None
    metaDataDictSolana["image"] = ""
    metaDataDictSolana["animation_url"] = ""
    metaDataDictSolana["external_url"] = ""

    attributes = []

    for i in NFT_Variants:
        dictionary = {
            "trait_type": i,
            "value": NFT_Variants[i]
        }

        attributes.append(dictionary)

    metaDataDictSolana["attributes"] = attributes
    metaDataDictSolana["collection"] = {
        "name": "",
        "family": ""
    }
    metaDataDictSolana["properties"] = {"files": [{"uri": "", "type": ""}],
                                  "category": "",
                                  "creators": [{"address": "", "share": None}]
                                  }
    return metaDataDictSolana

def returnErc721MetaData(name, description, NFT_DNA, NFT_Variants):
    metaDataDictErc721 = {}

    metaDataDictErc721["title"] = name
    metaDataDictErc721["type"] = ""
    metaDataDictErc721["properties"] = {"NFT_Variants": NFT_Variants,
                                        "description": description,
                                        "NFT_DNA": NFT_DNA
                                        }
    return metaDataDictErc721

if __name__ == '__main__':
    returnSolanaMetaData()
    returnCardanoMetaData()
    returnErc721MetaData()
