# Some code in this file was generously sponsored by the amazing team over at SolSweepers!
# Feel free to check out their amazing project and see how they are using Blend_My_NFTs:
# https://discord.gg/QTT7dzcuVs

# Purpose:
# This file returns the specified meta data format to the Exporter.py for a given NFT DNA.

import bpy
import json

# Cardano Template
def returnCardanoMetaData(name, NFT_DNA, NFT_Variants, custom_Fields_File, enableCustomFields, cardano_description):
    metaDataDictCardano = {"721": {
        "<policy_id>": {
            name: {
                "name": name,
                "image": "",
                "mediaType": "",
                "description": cardano_description,
            }
        },
        "version": "1.0"
    }}

    for i in NFT_Variants:
        metaDataDictCardano["721"]["<policy_id>"][name][i] = NFT_Variants[i]

    # Custom Fields:
    if enableCustomFields:
        custom_Fields = json.load(open(custom_Fields_File))
        for i in custom_Fields:
            metaDataDictCardano["721"]["<policy_id>"][name][i] = custom_Fields[i]

    return metaDataDictCardano

# Solana Template
def returnSolanaMetaData(name, NFT_DNA, NFT_Variants, custom_Fields_File, enableCustomFields, solana_description):
    metaDataDictSolana = {"name": name, "symbol": "", "description": solana_description, "seller_fee_basis_points": None,
                          "image": "", "animation_url": "", "external_url": ""}

    attributes = []

    for i in NFT_Variants:
        dictionary = {
            "trait_type": i,
            "value": NFT_Variants[i]
        }

        attributes.append(dictionary)

    # Custom Fields:
    if enableCustomFields:
        custom_Fields = json.load(open(custom_Fields_File))
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
    return metaDataDictSolana

# ERC721 Template
def returnErc721MetaData(name, NFT_DNA, NFT_Variants, custom_Fields_File, enableCustomFields, erc721_description):
    metaDataDictErc721 = {
        "name": name,
        "description": erc721_description,
        "image": "",
        "attributes": None,
    }

    attributes = []

    for i in NFT_Variants:
        dictionary = {
            "trait_type": i,
            "value": NFT_Variants[i]
        }

        attributes.append(dictionary)

    # Custom Fields:
    if enableCustomFields:
        custom_Fields = json.load(open(custom_Fields_File))
        for i in custom_Fields:
            dictionary = {
                "trait_type": i,
                "value": custom_Fields[i]
            }
            attributes.append(dictionary)

    metaDataDictErc721["attributes"] = attributes

    return metaDataDictErc721
