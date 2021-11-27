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
        metaDataDict["name"] = name
        metaDataDict["symbol"] = ""
        metaDataDict["description"] = config.metaDataDescription
        metaDataDict["seller_fee_basis_points"] = None
        metaDataDict["image"] = ""
        metaDataDict["animation_url"] = ""
        metaDataDict["external_url"] = ""
        metaDataDict["attributes"] = {"NFT_DNA": a, "NFT_Variants": dnaDictionary}
        metaDataDict["collection"] = {"name": "", "family": ""}
        metaDataDict["properties"] = {"files": [{"uri": "", "type": ""}],
                                      "category": "",
                                      "creators": [{"address": "", "share": None}]
                                      }

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
