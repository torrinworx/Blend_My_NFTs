# Purpose:
# This file generates NFT DNA based on a .blend file scene structure and exports NFTRecord.json.

import os
import time
import json
import random
import traceback
from functools import partial
from . import logic, material_generator, helpers
from .helpers import TextColors


def generate_nft_dna(
        collection_size,
        enable_rarity,
        enable_logic,
        logic_file,
        enable_materials,
        materials_file,
        enable_debug
):
    """
    Returns batchDataDictionary containing the number of NFT combinations, hierarchy, and the dna_list.
    """

    hierarchy = helpers.get_hierarchy()

    # DNA random, Rarity and Logic methods:
    data_dictionary = {}

    def create_dna_random(hierarchy):
        """Creates a single DNA randomly without Rarity or Logic."""
        dna_str = ""
        dna_str_list = []
        list_option_variant = []

        for i in hierarchy:
            num_child = len(hierarchy[i])
            possible_nums = list(range(1, num_child + 1))
            list_option_variant.append(possible_nums)

        for i in list_option_variant:
            random_variant_num = random.choices(i, k=1)
            str1 = ''.join(str(e) for e in random_variant_num)
            dna_str_list.append(str1)

        for i in dna_str_list:
            num = "-" + str(i)
            dna_str += num

        dna = ''.join(dna_str.split('-', 1))

        return str(dna)

    def create_dna_rarity(hierarchy):
        """
        Sorts through data_dictionary and appropriately weights each variant based on their rarity percentage set in Blender
        ("rarity" in DNA_Generator). Then
        """
        single_dna = ""

        for i in hierarchy:
            number_list_of_i = []
            rarity_list_of_i = []
            if_zero_bool = None

            for k in hierarchy[i]:
                number = hierarchy[i][k]["number"]
                number_list_of_i.append(number)

                rarity = hierarchy[i][k]["rarity"]
                rarity_list_of_i.append(float(rarity))

            for x in rarity_list_of_i:
                if x == 0:
                    if_zero_bool = True
                elif x != 0:
                    if_zero_bool = False

            try:
                if if_zero_bool:
                    variant_by_num = random.choices(number_list_of_i, k=1)
                elif not if_zero_bool:
                    variant_by_num = random.choices(number_list_of_i, weights=rarity_list_of_i, k=1)
            except IndexError:
                raise IndexError(
                    f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                    f"An issue was found within the Attribute collection '{i}'. For more information on Blend_My_NFTs "
                    f"compatible scenes, see:\n{TextColors.RESET}"
                    f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
                )

            single_dna += "-" + str(variant_by_num[0])
        single_dna = ''.join(single_dna.split('-', 1))
        return single_dna

    def singleCompleteDNA():
        """
        This function applies Rarity and Logic to a single DNA created by createDNASingle() if Rarity or Logic specified
        """

        single_dna = ""
        if not enable_rarity:
            single_dna = create_dna_random(hierarchy)
        # print("============")
        # print(f"Original DNA: {single_dna}")
        if enable_rarity:
            single_dna = create_dna_rarity(hierarchy)
        # print(f"Rarity DNA: {single_dna}")

        if enable_logic:
            single_dna = logic.logicafy_dna_single(hierarchy, single_dna, logic_file, enable_rarity)
        # print(f"Logic DNA: {single_dna}")

        if enable_materials:
            single_dna = material_generator.apply_materials(hierarchy, single_dna, materials_file, enable_rarity)
        # print(f"Materials DNA: {single_dna}")

        # print("============\n")

        return single_dna

    def create_dna_list():
        """
        Creates dna_list. Loops through createDNARandom() and applies Rarity, and Logic while checking if all DNA
        are unique.
        """
        dna_set_return = set()

        for i in range(collection_size):
            dna_push_to_list = partial(singleCompleteDNA)

            dna_set_return |= {''.join([dna_push_to_list()]) for _ in range(collection_size - len(dna_set_return))}

        dna_list_non_formatted = list(dna_set_return)

        dna_list_formatted = []
        dna_counter = 1
        for i in dna_list_non_formatted:
            dna_list_formatted.append({
                i: {
                    "complete": False,
                    "order_num": dna_counter
                }
            })

            dna_counter += 1

        return dna_list_formatted

    dna_list = create_dna_list()

    # Messages:

    helpers.raise_warning_collection_size(dna_list, collection_size)

    # Data stored in batchDataDictionary:
    data_dictionary["num_nfts_generated"] = len(dna_list)
    data_dictionary["hierarchy"] = hierarchy
    data_dictionary["dna_list"] = dna_list

    return data_dictionary


def make_batches(
        collection_size,
        nfts_per_batch,
        save_path,
        batch_json_save_path
):
    """
   Sorts through all the batches and outputs a given number of batches depending on collection_size and nfts_per_batch.
   These files are then saved as Batch#.json files to batch_json_save_path
   """

    # Clears the Batch Data folder of Batches:
    batch_list = os.listdir(batch_json_save_path)
    if batch_list:
        for i in batch_list:
            batch = os.path.join(batch_json_save_path, i)
            if os.path.exists(batch):
                os.remove(
                    os.path.join(batch_json_save_path, i)
                )

    blend_my_nf_ts_output = os.path.join(save_path, "Blend_My_NFTs Output", "NFT_Data")
    nft_record_save_path = os.path.join(blend_my_nf_ts_output, "NFTRecord.json")
    data_dictionary = json.load(open(nft_record_save_path))

    num_nfts_generated = data_dictionary["num_nfts_generated"]
    hierarchy = data_dictionary["hierarchy"]
    dna_list = data_dictionary["dna_list"]

    num_batches = collection_size // nfts_per_batch
    remainder_dna = collection_size % nfts_per_batch
    if remainder_dna > 0:
        num_batches += 1

    print(f"To generate batches of {nfts_per_batch} DNA sequences per batch, with a total of {num_nfts_generated}"
          f" possible NFT DNA sequences, the number of batches generated will be {num_batches}")

    batches_dna_list = []

    for i in range(num_batches):
        if i != range(num_batches)[-1]:
            batch_dna_list = list(dna_list[0:nfts_per_batch])
            batches_dna_list.append(batch_dna_list)

            dna_list = [x for x in dna_list if x not in batch_dna_list]
        else:
            batch_dna_list = dna_list

        batch_dictionary = {
            "nfts_in_batch": int(len(batch_dna_list)),
            "hierarchy": hierarchy,
            "batch_dna_list": batch_dna_list
        }

        batch_dictionary = json.dumps(batch_dictionary, indent=1, ensure_ascii=True)

        with open(os.path.join(batch_json_save_path, f"Batch{i + 1}.json"), "w") as outfile:
            outfile.write(batch_dictionary)


def send_to_record(
        collection_size,
        nfts_per_batch,
        save_path,
        enable_rarity,
        enable_logic,
        logic_file,
        enable_materials,
        materials_file,
        blend_my_nfts_output,
        batch_json_save_path,
        enable_debug
):
    """
   Creates NFTRecord.json file and sends "batch_data_dictionary" to it. NFTRecord.json is a permanent record of all DNA
   you've generated with all attribute variants. If you add new variants or attributes to your .blend file, other scripts
   need to reference this .json file to generate new DNA and make note of the new attributes and variants to prevent
   repeat DNA.
   """

    # Checking Scene is compatible with BMNFTs:
    helpers.check_scene()

    # Messages:
    print(
        f"\n{TextColors.OK}======== Creating NFT Data ========{TextColors.RESET}"
        f"\nGenerating {collection_size} NFT DNA"
    )

    if not enable_rarity and not enable_logic:
        print(
            f"{TextColors.OK}NFT DNA will be determined randomly, no special properties or parameters are "
            f"applied.\n{TextColors.RESET}")

    if enable_rarity:
        print(
                f"{TextColors.OK}Rarity is ON. Weights listed in .blend scene will be taken into account."
                f"{TextColors.RESET}"
        )

    if enable_logic:
        print(
                f"{TextColors.OK}Logic is ON. {len(list(logic_file.keys()))} rules detected and applied."
                f"{TextColors.RESET}"
        )

    time_start = time.time()

    def create_nft_data():
        try:
            data_dictionary = generate_nft_dna(
                    collection_size,
                    enable_rarity,
                    enable_logic,
                    logic_file,
                    enable_materials,
                    materials_file,
                    enable_debug,
            )
            nft_record_save_path = os.path.join(blend_my_nfts_output, "NFTRecord.json")

            # Checks:
            helpers.raise_warning_max_nfts(nfts_per_batch, collection_size)
            helpers.check_duplicates(data_dictionary["dna_list"])
            helpers.raise_error_zero_combinations()

            if enable_rarity:
                helpers.check_rarity(data_dictionary["hierarchy"], data_dictionary["dna_list"],
                                     os.path.join(save_path, "Blend_My_NFTs Output/NFT_Data"))

        except FileNotFoundError:
            raise FileNotFoundError(
                f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                f"Data not saved to NFTRecord.json. Please review your Blender scene and ensure it follows "
                f"the naming conventions and scene structure. For more information, see:\n{TextColors.RESET}"
                f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
            )
        finally:
            loading.stop()

        try:
            ledger = json.dumps(data_dictionary, indent=1, ensure_ascii=True)
            with open(nft_record_save_path, 'w') as outfile:
                outfile.write(ledger + '\n')

            print(
                f"\n{TextColors.OK}Blend_My_NFTs Success:\n"
                f"{len(data_dictionary['dna_list'])} NFT DNA saved to {nft_record_save_path}. NFT DNA Successfully "
                f"created.\n{TextColors.RESET}")

        except Exception:
            traceback.print_exc()
            raise (
                f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                f"Data not saved to NFTRecord.json. Please review your Blender scene and ensure it follows "
                f"the naming conventions and scene structure. For more information, "
                f"see:\n{TextColors.RESET}"
                f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
            )

    # Loading Animation:
    loading = helpers.Loader(f'Creating NFT DNA...', '').start()
    create_nft_data()
    make_batches(collection_size, nfts_per_batch, save_path, batch_json_save_path)
    loading.stop()

    time_end = time.time()

    print(
        f"{TextColors.OK}Created and saved NFT DNA in {time_end - time_start}s.\n{TextColors.RESET}"
    )
