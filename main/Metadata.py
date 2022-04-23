# Some code in this file was generously sponsored by the amazing team over at SolSweepers!
# Feel free to check out their amazing project and see how they are using Blend_My_NFTs:
# https://discord.gg/QTT7dzcuVs

# Purpose:
# This file returns the specified meta data format to the Exporter.py for a given NFT DNA.

import bpy

# Cardano Template


def returnCardanoMetaData(cardanoNewName, NFT_DNA, NFT_Variants, Material_Attributes,
                          custom_Fields, enableCustomFields, cardano_description):

    metaDataDictCardano = {"721": {
        "<policy_id>": {
            cardanoNewName: {
                "name": cardanoNewName,
                "image": "",
                "mediaType": "",
                "description": cardano_description,
            }
        },
        "version": "1.0"
    }}

    # Variants and Attributes:
    for i in NFT_Variants:
        metaDataDictCardano["721"]["<policy_id>"][cardanoNewName][i] = NFT_Variants[i]

    # Material Variants and Attributes:
    for i in Material_Attributes:
        metaDataDictCardano["721"]["<policy_id>"][cardanoNewName][i] = Material_Attributes[i]

    # Custom Fields:
    if enableCustomFields:
        for i in custom_Fields:
            metaDataDictCardano["721"]["<policy_id>"][cardanoNewName][i] = custom_Fields[i]

    return metaDataDictCardano

# Solana Template
def returnSolanaMetaData(solanaNewName, NFT_DNA, NFT_Variants, Material_Attributes, custom_Fields, enableCustomFields,
                         solana_description):
    metaDataDictSolana = {"name": solanaNewName, "symbol": "", "description": solana_description, "seller_fee_basis_points": None,
                          "image": "", "animation_url": "", "external_url": ""}

    attributes = []

    # Variant and Attributes:
    for i in NFT_Variants:
        dictionary = {
            "trait_type": i,
            "value": NFT_Variants[i]
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
    return metaDataDictSolana

# ERC721 Template
def returnErc721MetaData(erc721NewName, NFT_DNA, NFT_Variants, Material_Attributes, custom_Fields, enableCustomFields,
                         erc721_description):
    metaDataDictErc721 = {
        "name": erc721NewName,
        "description": erc721_description,
        "image": "",
        "attributes": None,
    }

    attributes = []

    # Variants and Attributes:
    for i in NFT_Variants:
        dictionary = {
            "trait_type": i,
            "value": NFT_Variants[i]
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

    return metaDataDictErc721
