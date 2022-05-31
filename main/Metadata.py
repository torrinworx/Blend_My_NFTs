# Some code in this file was generously sponsored by the amazing team over at SolSweepers!
# Feel free to check out their amazing project and see how they are using Blend_My_NFTs:
# https://discord.gg/QTT7dzcuVs

# Purpose:
# This file returns the specified meta data format to the Exporter.py for a given NFT DNA.

import bpy
import os
import json

def sendMetaDataToJson(metaDataDict, save_path, file_name):
    jsonMetaData = json.dumps(metaDataDict, indent=1, ensure_ascii=True)
    with open(os.path.join(save_path, f"{file_name}.json"), 'w') as outfile:
        outfile.write(jsonMetaData + '\n')

def stripNums(variant):
    variant = str(variant).split('_')[0]
    return variant

# Cardano Template
def createCardanoMetadata(name, Order_Num, NFT_DNA, NFT_Variants, Material_Attributes,
                          custom_Fields, enableCustomFields, cardano_description, cardanoMetadataPath):

    metaDataDictCardano = {"721": {
        "<policy_id>": {
            name: {
                "name": name,
                "image": "<ipfs_link>",
                "mediaType": "<mime_type>",
                "description": cardano_description,
            }
        },
        "version": "1.0"
    }}

    # Variants and Attributes:
    for i in NFT_Variants:
        metaDataDictCardano["721"]["<policy_id>"][name][i] = stripNums(NFT_Variants[i])

    # Material Variants and Attributes:
    for i in Material_Attributes:
        metaDataDictCardano["721"]["<policy_id>"][name][i] = Material_Attributes[i]

    # Custom Fields:
    if enableCustomFields:
        for i in custom_Fields:
            metaDataDictCardano["721"]["<policy_id>"][name][i] = custom_Fields[i]

    sendMetaDataToJson(metaDataDictCardano, cardanoMetadataPath, name)


# Solana Template
def createSolanaMetaData(name, Order_Num, NFT_DNA, NFT_Variants, Material_Attributes, custom_Fields, enableCustomFields,
                         solana_description, solanaMetadataPath):
    metaDataDictSolana = {"name": name, "symbol": "", "description": solana_description, "seller_fee_basis_points": None,
                          "image": "", "animation_url": "", "external_url": ""}

    attributes = []

    # Variant and Attributes:
    for i in NFT_Variants:
        dictionary = {
            "trait_type": i,
            "value": stripNums(NFT_Variants[i])
        }
        attributes.append(dictionary)

    # Material Variants and Attributes:
    for i in Material_Attributes:
        dictionary = {
            "trait_type": i,
            "value": Material_Attributes[i]
        }
        attributes.append(dictionary)

    # Custom Fields:
    if enableCustomFields:
        for i in custom_Fields:
            dictionary = {
                "trait_type": i,
                "value": custom_Fields[i]
            }
            attributes.append(dictionary)

    metaDataDictSolana["attributes"] = attributes
    metaDataDictSolana["collection"] = {
        "name": "",
        "family": ""
    }

    metaDataDictSolana["properties"] = {
        "files": [{"uri": "", "type": ""}],
        "category": "",
        "creators": [{"address": "", "share": None}]
    }

    sendMetaDataToJson(metaDataDictSolana, solanaMetadataPath, name)


# ERC721 Template
def createErc721MetaData(name, Order_Num, NFT_DNA, NFT_Variants, Material_Attributes, custom_Fields, enableCustomFields,
                         erc721_description, erc721MetadataPath):
    metaDataDictErc721 = {
        "name": name,
        "description": erc721_description,
        "image": "",
        "attributes": None,
    }

    attributes = []

    # Variants and Attributes:
    for i in NFT_Variants:
        dictionary = {
            "trait_type": i,
            "value": stripNums(NFT_Variants[i])
        }

        attributes.append(dictionary)

    # Material Variants and Attributes:
    for i in Material_Attributes:
        dictionary = {
            "trait_type": i,
            "value": Material_Attributes[i]
        }

        attributes.append(dictionary)

    # Custom Fields:
    if enableCustomFields:
        for i in custom_Fields:
            dictionary = {
                "trait_type": i,
                "value": custom_Fields[i]
            }
            attributes.append(dictionary)

    metaDataDictErc721["attributes"] = attributes

    sendMetaDataToJson(metaDataDictErc721, erc721MetadataPath, name)

