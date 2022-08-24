# Purpose:
# This file generates NFT DNA based on a .blend file scene structure and exports NFTRecord.json.

import bpy
import os
import time
import json
import random
from functools import partial
from . import Logic, Material_Generator, Helpers


def generateNFT_DNA(collectionSize, enableRarity, enableLogic, logicFile, enableMaterials, materialsFile, enable_debug):
    """
    Returns batchDataDictionary containing the number of NFT combinations, hierarchy, and the DNAList.
    """

    hierarchy = Helpers.get_hierarchy()

    # DNA random, Rarity and Logic methods:
    DataDictionary = {}

    def createDNArandom(hierarchy):
        """Creates a single DNA randomly without Rarity or Logic."""
        dnaStr = ""
        dnaStrList = []
        listOptionVariant = []

        for i in hierarchy:
            numChild = len(hierarchy[i])
            possibleNums = list(range(1, numChild + 1))
            listOptionVariant.append(possibleNums)

        for i in listOptionVariant:
            randomVariantNum = random.choices(i, k=1)
            str1 = ''.join(str(e) for e in randomVariantNum)
            dnaStrList.append(str1)

        for i in dnaStrList:
            num = "-" + str(i)
            dnaStr += num

        dna = ''.join(dnaStr.split('-', 1))

        return str(dna)

    def createDNArarity(hierarchy):
        """
        Sorts through DataDictionary and appropriately weights each variant based on their rarity percentage set in Blender
        ("rarity" in DNA_Generator). Then
        """
        singleDNA = ""

        for i in hierarchy:
            number_List_Of_i = []
            rarity_List_Of_i = []
            ifZeroBool = None

            for k in hierarchy[i]:
                number = hierarchy[i][k]["number"]
                number_List_Of_i.append(number)

                rarity = hierarchy[i][k]["rarity"]
                rarity_List_Of_i.append(float(rarity))

            for x in rarity_List_Of_i:
                if x == 0:
                    ifZeroBool = True
                elif x != 0:
                    ifZeroBool = False

            try:
                if ifZeroBool:
                    variantByNum = random.choices(number_List_Of_i, k=1)
                elif not ifZeroBool:
                    variantByNum = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)
            except IndexError:
                raise IndexError(
                    f"\n{Helpers.TextColors.ERROR}Blend_My_NFTs Error:\n"
                    f"An issue was found within the Attribute collection '{i}'. For more information on Blend_My_NFTs compatible scenes, "
                    f"see:\n{Helpers.TextColors.RESET}"
                    f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
                )

            singleDNA += "-" + str(variantByNum[0])
        singleDNA = ''.join(singleDNA.split('-', 1))
        return singleDNA

    def singleCompleteDNA():
        """
        This function applies Rarity and Logic to a single DNA created by createDNASingle() if Rarity or Logic specified
        """

        singleDNA = ""
        if not enableRarity:
            singleDNA = createDNArandom(hierarchy)
        # print("============")
        # print(f"Original DNA: {singleDNA}")
        if enableRarity:
            singleDNA = createDNArarity(hierarchy)
        # print(f"Rarity DNA: {singleDNA}")

        if enableLogic:
            singleDNA = Logic.logicafyDNAsingle(hierarchy, singleDNA, logicFile, enableRarity, enableMaterials)
        # print(f"Logic DNA: {singleDNA}")

        if enableMaterials:
            singleDNA = Material_Generator.apply_materials(hierarchy, singleDNA, materialsFile, enableRarity)
        # print(f"Materials DNA: {singleDNA}")

        # print("============\n")

        return singleDNA

    def create_DNAList():
        """Creates DNAList. Loops through createDNARandom() and applies Rarity, and Logic while checking if all DNA are unique"""
        DNASetReturn = set()

        for i in range(collectionSize):
            dnaPushToList = partial(singleCompleteDNA)

            DNASetReturn |= {''.join([dnaPushToList()]) for _ in range(collectionSize - len(DNASetReturn))}

        DNAListUnformatted = list(DNASetReturn)

        DNAListFormatted = []
        DNA_Counter = 1
        for i in DNAListUnformatted:
            DNAListFormatted.append({
                i: {
                    "Complete": False,
                    "Order_Num": DNA_Counter
                }
            })

            DNA_Counter += 1

        return DNAListFormatted

    DNAList = create_DNAList()

    # Messages:

    Helpers.raise_warning_collection_size(DNAList, collectionSize)

    # Data stored in batchDataDictionary:
    DataDictionary["numNFTsGenerated"] = len(DNAList)
    DataDictionary["hierarchy"] = hierarchy
    DataDictionary["DNAList"] = DNAList

    return DataDictionary


def makeBatches(collectionSize, nftsPerBatch, save_path, batch_json_save_path):
    """
   Sorts through all the batches and outputs a given number of batches depending on collectionSize and nftsPerBatch.
   These files are then saved as Batch#.json files to batch_json_save_path
   """

    # Clears the Batch Data folder of Batches:
    batchList = os.listdir(batch_json_save_path)
    if batchList:
        for i in batchList:
            batch = os.path.join(batch_json_save_path, i)
            if os.path.exists(batch):
                os.remove(
                    os.path.join(batch_json_save_path, i)
                )

    Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFTs Output", "NFT_Data")
    NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")
    DataDictionary = json.load(open(NFTRecord_save_path))

    numNFTsGenerated = DataDictionary["numNFTsGenerated"]
    hierarchy = DataDictionary["hierarchy"]
    DNAList = DataDictionary["DNAList"]

    numBatches = collectionSize // nftsPerBatch
    remainder_dna = collectionSize % nftsPerBatch
    if remainder_dna > 0:
        numBatches += 1

    print(f"To generate batches of {nftsPerBatch} DNA sequences per batch, with a total of {numNFTsGenerated}"
          f" possible NFT DNA sequences, the number of batches generated will be {numBatches}")

    batches_dna_list = []

    for i in range(numBatches):
        BatchDNAList = []
        if i != range(numBatches)[-1]:
            BatchDNAList = list(DNAList[0:nftsPerBatch])
            batches_dna_list.append(BatchDNAList)

            DNAList = [x for x in DNAList if x not in BatchDNAList]
        else:
            BatchDNAList = DNAList

        batchDictionary = {
            "NFTs_in_Batch": int(len(BatchDNAList)),
            "hierarchy": hierarchy,
            "BatchDNAList": BatchDNAList
        }

        batchDictionary = json.dumps(batchDictionary, indent=1, ensure_ascii=True)

        with open(os.path.join(batch_json_save_path, f"Batch{i + 1}.json"), "w") as outfile:
            outfile.write(batchDictionary)


def send_To_Record_JSON(collectionSize, nftsPerBatch, save_path, enableRarity, enableLogic, logicFile, enableMaterials,
                        materialsFile, Blend_My_NFTs_Output, batch_json_save_path, enable_debug):
    """
   Creates NFTRecord.json file and sends "batchDataDictionary" to it. NFTRecord.json is a permanent record of all DNA
   you've generated with all attribute variants. If you add new variants or attributes to your .blend file, other scripts
   need to reference this .json file to generate new DNA and make note of the new attributes and variants to prevent
   repeate DNA.
   """

    # Checking Scene is compatible with BMNFTs:
    Helpers.check_scene()

    # Messages:
    print(
        f"\n{Helpers.TextColors.OK}======== Creating NFT Data ========{Helpers.TextColors.RESET}"
        f"\nGenerating {collectionSize} NFT DNA"
    )

    if not enableRarity and not enableLogic:
        print(
            f"{Helpers.TextColors.OK}NFT DNA will be determined randomly, no special properties or parameters are "
            f"applied.\n{Helpers.TextColors.RESET}")

    if enableRarity:
        print(
                f"{Helpers.TextColors.OK}Rarity is ON. Weights listed in .blend scene will be taken into account."
                f"{Helpers.TextColors.RESET}"
        )

    if enableLogic:
        print(
                f"{Helpers.TextColors.OK}Logic is ON. {len(list(logicFile.keys()))} rules detected and applied."
                f"{Helpers.TextColors.RESET}"
        )

    time_start = time.time()

    def create_nft_data():
        try:
            DataDictionary = generateNFT_DNA(collectionSize, enableRarity, enableLogic, logicFile, enableMaterials,
                                             materialsFile, enable_debug)
            NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")

            # Checks:

            Helpers.raise_warning_max_nfts(nftsPerBatch, collectionSize)
            Helpers.check_duplicates(DataDictionary["DNAList"])
            Helpers.raise_error_zero_combinations()

            if enableRarity:
                Helpers.check_rarity(DataDictionary["hierarchy"], DataDictionary["DNAList"],
                                     os.path.join(save_path, "Blend_My_NFTs Output/NFT_Data"))

        except FileNotFoundError:
            raise FileNotFoundError(
                f"\n{Helpers.TextColors.ERROR}Blend_My_NFTs Error:\n"
                f"Data not saved to NFTRecord.json. Please review your Blender scene and ensure it follows "
                f"the naming conventions and scene structure. For more information, "
                f"see:\n{Helpers.TextColors.RESET}"
                f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
            )
        finally:
            loading.stop()

        try:
            ledger = json.dumps(DataDictionary, indent=1, ensure_ascii=True)
            with open(NFTRecord_save_path, 'w') as outfile:
                outfile.write(ledger + '\n')

            print(
                f"\n{Helpers.TextColors.OK}Blend_My_NFTs Success:\n"
                f"{len(DataDictionary['DNAList'])} NFT DNA saved to {NFTRecord_save_path}. NFT DNA Successfully created.\n{Helpers.TextColors.RESET}")

        except:
            raise (
                f"\n{Helpers.TextColors.ERROR}Blend_My_NFTs Error:\n"
                f"Data not saved to NFTRecord.json. Please review your Blender scene and ensure it follows "
                f"the naming conventions and scene structure. For more information, "
                f"see:\n{Helpers.TextColors.RESET}"
                f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
            )

    # Loading Animation:
    loading = Helpers.Loader(f'Creating NFT DNA...', '').start()
    create_nft_data()
    makeBatches(collectionSize, nftsPerBatch, save_path, batch_json_save_path)
    loading.stop()

    time_end = time.time()

    print(
        f"{Helpers.TextColors.OK}Created and saved NFT DNA in {time_end - time_start}s.\n{Helpers.TextColors.RESET}"
    )
