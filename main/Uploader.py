"""
NftGenerator Using NFTPort
@author https://github.com/aizwellenstan
"""

import os
import json
import requests
from os import listdir
from os.path import isfile, join
import time

def nftPortFileUploader(apikey, file):
    response = requests.post(
        "https://api.nftport.xyz/v0/files",
        headers={"Authorization": apikey},
        files={"file": file}
    )
    
    return json.loads(response.text)

def nftPortMetaUploader(apikey, metaData):
    response = requests.post(
        "https://api.nftport.xyz/v0/metadata",
        headers={"Authorization": apikey, "Content-Type": "appication/json"},
        data=json.dumps(metaData, indent=4) 
    )
    
    return json.loads(response.text)

def minter(apikey, meta, CONTRACT_ADDRESS, MINT_TO_ADDRESS):
    mintInfo = {
        'chain': 'polygon',
        'contract_address': CONTRACT_ADDRESS,
        'metadata_uri': meta['metadata_uri'],
        'mint_to_address': MINT_TO_ADDRESS,
        'token_id': meta['custom_fields']['edition']
    }
    response = requests.post(
        "https://api.nftport.xyz/v0/mints/customizable",
        headers={"Authorization": apikey, "Content-Type": "appication/json"},
        data=json.dumps(mintInfo, indent=4) 
    )

    return json.loads(response.text)

def uploadToNFTPort(nftport_panel_input):
    glbFile = f"{nftport_panel_input.modelPath}\{nftport_panel_input.fileName}.glb"
    with open(glbFile, 'rb') as modelFile:
        res = nftPortFileUploader(nftport_panel_input.apikey, modelFile)
        resModelUrl = f"{res['ipfs_url']}?fileName={nftport_panel_input.fileName}.glb"

    pngFile = f"{nftport_panel_input.imagePath}\{nftport_panel_input.fileName}.png"
    with open(pngFile, 'rb') as imageFile:
        res = nftPortFileUploader(nftport_panel_input.apikey, imageFile)
        resImageUrl = f"{res['ipfs_url']}"

    jsonFile = f"{nftport_panel_input.metaDataPath}\{nftport_panel_input.fileName}.json"
    with open(jsonFile, 'r') as inputFile:
        metaData = json.load(inputFile)
        metaData['animation_url'] = resModelUrl
        metaData['file_url'] = resImageUrl
        
    res = nftPortMetaUploader(nftport_panel_input.apikey, metaData)
    metaData['metadata_uri'] = res['metadata_uri']
    with open(jsonFile, 'w') as outputFile:
        json.dump(metaData, outputFile, ensure_ascii=False, indent=4)
    
    return metaData
        
def uploadNFTCollection(uploader_panel_input):
    completeCollPath = os.path.join(uploader_panel_input.save_path, "Blend_My_NFTs Output", "Complete_Collection")
    completeImagePath = os.path.join(completeCollPath, "Images")
    completeAnimationsPath = os.path.join(completeCollPath, "Animations")
    completeModelsPath = os.path.join(completeCollPath, "Models")
    openSeaMetaDataPath = os.path.join(completeCollPath, "OpenSea_metaData")

    class nftport_panel_input:
        apikey = uploader_panel_input.nftport_api_key
        modelPath = completeModelsPath
        imagePath = completeImagePath
        metaDataPath = openSeaMetaDataPath
        fileName = ""

    onlyfiles = [f for f in listdir(completeModelsPath) if isfile(join(completeModelsPath, f))]

    print(onlyfiles)
    allMetadata = []
    for file in onlyfiles:
        fileName = file.split(".")[0]
        nftport_panel_input.fileName = fileName
        metaData = uploadToNFTPort(nftport_panel_input)
        allMetadata.append(metaData)
    print(allMetadata)
    for meta in allMetadata:
        minted = minter(nftport_panel_input.apikey, meta, uploader_panel_input.contract_address, uploader_panel_input.wallet_address)
        print(minted)
        file = f"{nftport_panel_input.metaDataPath}\{meta['custom_fields']['edition']}_minted.json"
        with open(file, 'w') as outputFile:
            json.dump(minted, outputFile, ensure_ascii=False, indent=4)
    print("All Minted")
    
    
if __name__ == '__main__':
    uploadNFTCollection()
