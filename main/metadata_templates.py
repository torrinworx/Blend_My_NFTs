# Some code in this file was generously sponsored by the amazing team over at SolSweepers!
# Feel free to check out their amazing project and see how they are using Blend_My_NFTs:
# https://discord.gg/QTT7dzcuVs

# Purpose:
# This file returns the specified metadata format to the exporter.py for a given NFT DNA.

import os
import json


def send_metadata_to_json(meta_data_dict, save_path, file_name):
    json_metadata = json.dumps(meta_data_dict, indent=1, ensure_ascii=True)
    with open(os.path.join(save_path, f"{file_name}.json"), 'w') as outfile:
        outfile.write(json_metadata + '\n')


def strip_nums(variant):
    variant = str(variant).split('_')[0]
    return variant


# Cardano Template
def create_cardano_metadata(
        name,
        order_num,
        nft_dna,
        nft_variants,
        material_attributes,
        custom_fields,
        enable_custom_fields,
        cardano_description,
        cardano_metadata_path
):

    meta_data_dict_cardano = {"721": {
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
    for i in nft_variants:
        meta_data_dict_cardano["721"]["<policy_id>"][name][i] = strip_nums(nft_variants[i])

    # Material Variants and Attributes:
    for i in material_attributes:
        meta_data_dict_cardano["721"]["<policy_id>"][name][i] = material_attributes[i]

    # Custom Fields:
    if enable_custom_fields:
        for i in custom_fields:
            meta_data_dict_cardano["721"]["<policy_id>"][name][i] = custom_fields[i]

    send_metadata_to_json(
            meta_data_dict_cardano,
            cardano_metadata_path,
            name
    )


# Solana Template
def createSolanaMetaData(
        name,
        order_num,
        nft_dna,
        nft_variants,
        material_attributes,
        custom_fields,
        enable_custom_fields,
        solana_description,
        solana_metadata_path
):
    metadata_dict_solana = {
            "name": name,
            "symbol": "",
            "description": solana_description,
            "seller_fee_basis_points": None,
            "image": "",
            "animation_url": "",
            "external_url": ""
    }

    attributes = []

    # Variant and Attributes:
    for i in nft_variants:
        dictionary = {
            "trait_type": i,
            "value": strip_nums(nft_variants[i])
        }
        attributes.append(dictionary)

    # Material Variants and Attributes:
    for i in material_attributes:
        dictionary = {
            "trait_type": i,
            "value": material_attributes[i]
        }
        attributes.append(dictionary)

    # Custom Fields:
    if enable_custom_fields:
        for i in custom_fields:
            dictionary = {
                "trait_type": i,
                "value": custom_fields[i]
            }
            attributes.append(dictionary)

    metadata_dict_solana["attributes"] = attributes
    metadata_dict_solana["collection"] = {
        "name": "",
        "family": ""
    }

    metadata_dict_solana["properties"] = {
        "files": [{"uri": "", "type": ""}],
        "category": "",
        "creators": [{"address": "", "share": None}]
    }

    send_metadata_to_json(
            metadata_dict_solana,
            solana_metadata_path,
            name
    )


# ERC721 Template
def create_erc721_meta_data(
        name,
        order_num,
        nft_dna,
        nft_variants,
        material_attributes,
        custom_fields,
        enable_custom_fields,
        erc721_description,
        erc721_metadata_path
):

    metadata_dict_erc721 = {
        "name": name,
        "description": erc721_description,
        "image": "",
        "attributes": None,
    }

    attributes = []

    # Variants and Attributes:
    for i in nft_variants:
        dictionary = {
            "trait_type": i,
            "value": strip_nums(nft_variants[i])
        }

        attributes.append(dictionary)

    # Material Variants and Attributes:
    for i in material_attributes:
        dictionary = {
            "trait_type": i,
            "value": material_attributes[i]
        }

        attributes.append(dictionary)

    # Custom Fields:
    if enable_custom_fields:
        for i in custom_fields:
            dictionary = {
                "trait_type": i,
                "value": custom_fields[i]
            }
            attributes.append(dictionary)

    metadata_dict_erc721["attributes"] = attributes

    send_metadata_to_json(
            metadata_dict_erc721,
            erc721_metadata_path,
            name
    )
