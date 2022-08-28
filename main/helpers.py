import bpy
import os
import sys
import json
import copy
import logging
import tempfile
import platform
import traceback
from time import sleep
from itertools import cycle
from threading import Thread
from shutil import get_terminal_size
from collections import Counter, defaultdict

log = logging.getLogger(__name__)


# ======== CONSTANTS ======== #

# Constants are used for storing or updating constant values that may need to be changes depending on system
# requirements and different use-cases.

removeList = [".gitignore", ".DS_Store", "desktop.ini", ".ini"]


def remove_file_by_extension(dirlist):
    """
    Checks if a given directory list contains any of the files or file extensions listed above, if so, remove them
    from list and return a clean dir list. These files interfere with BMNFTs operations and should be removed
    whenever dealing with directories.
    """

    if str(type(dirlist)) == "<class 'list'>":
        dirlist = list(dirlist)  # converts single string path to list if dir pasted as string

    return_dirs = []
    for directory in dirlist:
        if not str(os.path.split(directory)[1]) in removeList:
            return_dirs.append(directory)

    return return_dirs


# TODO: fix colours in console logs and find a way to include coloured text in .txt file.

class TextColors:
    """
    The colour of console messages.
    """

    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    ERROR = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR


def save_result(result):
    """
    Saves json result to json file at the specified path.
    """
    file_name = "log.json"
    if platform.system() == "Linux" or platform.system() == "Darwin":
        path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop', file_name)

    if platform.system() == "Windows":
        path = os.path.join(os.environ["HOMEPATH"], "Desktop", file_name)

    data = json.dumps(result, indent=1, ensure_ascii=True)
    with open(path, 'w') as outfile:
        outfile.write(data + '\n')


# ======== GET COMBINATIONS ======== #

# This section retrieves the Scene hierarchy from the current Blender file.


def get_hierarchy():
    """
    Returns the hierarchy of a given Blender scene.
    """

    coll = bpy.context.scene.collection

    script_ignore_collection = bpy.data.collections["Script_Ignore"]

    list_all_coll_in_scene = []
    list_all_collections = []

    def traverse_tree(t):
        yield t
        for child in t.children:
            yield from traverse_tree(child)

    for c in traverse_tree(coll):
        list_all_coll_in_scene.append(c)

    for i in list_all_coll_in_scene:
        list_all_collections.append(i.name)

    list_all_collections.remove(script_ignore_collection.name)

    if "Scene Collection" in list_all_collections:
        list_all_collections.remove("Scene Collection")

    if "Master Collection" in list_all_collections:
        list_all_collections.remove("Master Collection")

    def all_script_ignore(script_ignore_coll):
        # Removes all collections, sub collections in Script_Ignore collection from list_all_collections.

        for collection in list(script_ignore_coll.children):
            list_all_collections.remove(collection.name)
            list_coll = list(collection.children)
            if len(list_coll) > 0:
                all_script_ignore(collection)

    all_script_ignore(script_ignore_collection)
    list_all_collections.sort()

    exclude = ["_"]  # Excluding characters that identify a Variant
    attribute_collections = copy.deepcopy(list_all_collections)

    def filter_num():
        """
        This function removes items from 'attribute_collections' if they include values from the 'exclude' variable.
        It removes child collections from the parent collections in from the "list_all_collections" list.
        """
        for x in attribute_collections:
            if any(i in x for i in exclude):
                attribute_collections.remove(x)

    for i in range(len(list_all_collections)):
        filter_num()

    attribute_variants = [x for x in list_all_collections if x not in attribute_collections]
    attribute_collections1 = copy.deepcopy(attribute_collections)

    def attribute_data(att_vars):
        """
        Creates a dictionary of each attribute
        """
        all_att_data_list = {}
        for i in att_vars:
            # Check if name follows naming conventions:
            if int(i.count("_")) > 2 and int(i.split("_")[1]) > 0:
                log.error(
                        f"\n{traceback.format_exc()}"
                        f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                        f"There is a naming issue with the following Attribute/Variant: '{i}'\n"
                        f"Review the naming convention of Attribute and Variant collections here:\n{TextColors.RESET}"
                        f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
                )
                raise Exception()

            try:
                number = i.split("_")[1]
                name = i.split("_")[0]
                rarity = i.split("_")[2]
            except IndexError:
                log.error(
                        f"\n{traceback.format_exc()}"
                        f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                        f"There is a naming issue with the following Attribute/Variant: '{i}'\n"
                        f"Review the naming convention of Attribute and Variant collections here:\n{TextColors.RESET}"
                        f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
                )
                raise Exception()

            all_att_data_list[i] = {"name": name, "number": number, "rarity": rarity}
        return all_att_data_list

    variant_meta_data = attribute_data(attribute_variants)

    hierarchy = {}
    for i in attribute_collections1:
        col_par_long = list(bpy.data.collections[str(i)].children)
        col_par_short = {}
        for x in col_par_long:
            col_par_short[x.name] = None
        hierarchy[i] = col_par_short

    for a in hierarchy:
        for b in hierarchy[a]:
            for x in variant_meta_data:
                if str(x) == str(b):
                    (hierarchy[a])[b] = variant_meta_data[x]

    return hierarchy


# ======== GET COMBINATIONS ======== #

# This section is used to get the number of combinations for checks and the UI display

def get_combinations():
    """
    Returns "combinations", the number of all possible NFT DNA for a given Blender scene formatted to BMNFTs conventions
    combinations.
    """

    hierarchy = get_hierarchy()
    hierarchy_by_num = []

    for i in hierarchy:
        # Ignore Collections with nothing in them
        if len(hierarchy[i]) != 0:
            hierarchy_by_num.append(len(hierarchy[i]))
        else:
            log.warning(f"\nThe following collection has been identified as empty: {i}")

    combinations = 1
    for i in hierarchy_by_num:
        combinations = combinations * i

    return combinations


# ======== CHECKS ======== #

# This section is used to check the NFTRecord.json for duplicate NFT DNA and returns any found in the console.
# It also checks the percentage each variant is chosen in the NFTRecord, then compares it with its rarity percentage
# set in the .blend file.

# This section is provided for transparency. The accuracy of the rarity values you set in your .blend file as outlined
# in the README.md file are dependent on the maxNFTs, and the maximum number of combinations of your NFT collection.

def check_scene():  # Not complete
    """
    Checks if Blender file Scene follows the Blend_My_NFTs conventions. If not, raises error with all instances of
    violations.
    """

    script_ignore_exists = None  # True if Script_Ignore collection exists in Blender scene
    attribute_naming_conventions = None  # True if all attributes in Blender scene follow BMNFTs naming conventions
    variant_naming_conventions = None  # True if all variants in Blender scene follow BMNFTs naming conventions
    object_placing_conventions = None  # True if all objects are within either Script_Ignore or a variant collection

    # script_ignore_exists:
    try:
        scriptIgnoreCollection = bpy.data.collections["Script_Ignore"]
        script_ignore_exists = True
    except KeyError:
        log.error(
                f"\n{traceback.format_exc()}"
                f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                f"Add a Script_Ignore collection to your Blender scene and ensure the name is exactly 'Script_Ignore'. "
                f"For more information, see:"
                f"\nhttps://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n{TextColors.RESET}"
        )
        raise

    hierarchy = get_hierarchy()
    collections = bpy.context.scene.collection

    # attribute_naming_conventions


def check_rarity(hierarchy, dna_list_formatted, save_path):
    """Checks rarity percentage of each Variant, then sends it to RarityData.json in NFT_Data folder."""

    dna_list = [list(i.keys())[0] for i in dna_list_formatted]
    num_nfts_generated = len(dna_list)
    num_dict = defaultdict(list)
    hierarchy.keys()

    for i in dna_list:
        dna_split_list = i.split("-")

        for j, k in zip(dna_split_list, hierarchy.keys()):
            num_dict[k].append(j)

    num_dict = dict(num_dict)

    for i in num_dict:
        count = dict(Counter(num_dict[i]))
        num_dict[i] = count

    full_num_name = {}

    for i in hierarchy:
        full_num_name[i] = {}
        for j in hierarchy[i]:
            variant_num = hierarchy[i][j]["number"]

            full_num_name[i][variant_num] = j

    complete_data = {}

    for i, j in zip(full_num_name, num_dict):
        x = {}
        for k in full_num_name[i]:
            for l in num_dict[j]:
                if l == k:
                    name = full_num_name[i][k]
                    num = num_dict[j][l]
                    x[name] = [(str(round(((num / num_nfts_generated) * 100), 2)) + "%"), str(num)]

        complete_data[i] = x

    # Saving Rarity data to console and log:
    x = f"\nPercentages for each Variant per Attribute:"
    for i in complete_data:
        x += f"\n\n{i}:"
        if complete_data[i]:
            for j in complete_data[i]:
                x += f"\n - {j}: {complete_data[i][j][0]} occurs {complete_data[i][j][1]} times."
        else:
            x += f"\n - Variants not selected."

    log.info(x)

    json_meta_data = json.dumps(complete_data, indent=1, ensure_ascii=True)

    with open(os.path.join(save_path, "RarityData.json"), 'w') as outfile:
        outfile.write(json_meta_data + '\n')
    path = os.path.join(save_path, "RarityData.json")

    log.info(
            f"\nRarity data has been saved to:\n{path}"
    )


def check_duplicates(dna_list_formatted):
    """Checks if there are duplicates in dna_list before NFTRecord.json is sent to JSON file."""
    dna_list = []
    for i in dna_list_formatted:
        dna_list.append(list(i.keys())[0])

    duplicates = 0
    seen = set()

    for x in dna_list:
        if x in seen:
            duplicates += 1
        seen.add(x)

    if duplicates > 0:
        log.warning(
                f"\n{TextColors.WARNING}Blend_My_NFTs Warning:\n"
                f"{duplicates} duplicate NFT DNA was detected. This should not be possible. For more information, see:"
                f"\nhttps://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure"
                f"\n{TextColors.RESET}"
        )

    log.info(f"\n\nDuplicate NFT DNA found: {duplicates}")


def check_failed_batches(batch_json_save_path):
    fail_state = False
    failed_batch = None
    failed_dna = None
    failed_dna_index = None

    if os.path.isdir(batch_json_save_path):
        batch_folders = remove_file_by_extension(os.listdir(batch_json_save_path))

        for i in batch_folders:
            batch = json.load(open(os.path.join(batch_json_save_path, i)))
            nfts_in_batch = batch["nfts_in_batch"]
            if "Generation Save" in batch:
                dna_generated = batch["Generation Save"][-1]["DNA Generated"]
                if dna_generated is not None and dna_generated < nfts_in_batch:
                    fail_state = True
                    failed_batch = int(i.removeprefix("Batch").removesuffix(".json"))
                    failed_dna = dna_generated

    return fail_state, failed_batch, failed_dna, failed_dna_index


# Raise Errors:
def raise_error_num_batches(max_nfts, nfts_per_batch):
    """Checks if number of Batches is less than maxNFTs, if not raises error."""

    try:
        num_batches = max_nfts / nfts_per_batch
        return num_batches
    except ZeroDivisionError:
        log.error(
                f"\n{traceback.format_exc()}"
                f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                f"The number of NFTs per Batch must be greater than ZERO."
                f"Please review your Blender scene and ensure it follows "
                f"the naming conventions and scene structure. For more information, "
                f"see:\n{TextColors.RESET}"
                f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure"
                f"\n{TextColors.RESET}"
        )
        raise ZeroDivisionError()


def raise_error_zero_combinations():
    """Checks if combinations is greater than 0, if so, raises error."""
    if get_combinations() == 0:
        log.error(
                f"\n{traceback.format_exc()}"
                f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                f"The number of all possible combinations is ZERO. Please review your Blender scene and ensure it "
                f"follows the naming conventions and scene structure. For more information, see:\n{TextColors.RESET}"
                f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure"
                f"\n{TextColors.RESET}"
        )

        raise ValueError()


def raise_error_num_batches_greater_then(num_batches):
    if num_batches < 1:
        log.error(
                f"\n{traceback.format_exc()}"
                f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                f"The number of Batches is less than 1. Please review your Blender scene and ensure it follows "
                f"the naming conventions and scene structure. For more information, "
                f"see:\n{TextColors.RESET}"
                f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure"
                f"\n{TextColors.RESET}"
        )
        raise ValueError()


# Raise Warnings:
def raise_warning_max_nfts(nfts_per_batch, collection_size):
    """
    Prints warning if nfts_per_batch is greater than collection_size.
    """

    if nfts_per_batch > collection_size:
        log.error(
                f"\n{traceback.format_exc()}"
                f"\n{TextColors.WARNING}Blend_My_NFTs Warning:\n"
                f"The number of NFTs Per Batch you set is smaller than the NFT Collection Size you set."
                f"\n{TextColors.RESET}"
        )

        raise ValueError()


def raise_warning_collection_size(dna_list, collection_size):
    """
    Prints warning if BMNFTs cannot generate requested number of NFTs from a given collection_size.
    """

    if len(dna_list) < collection_size:
        log.warning(
                f"\n{traceback.format_exc()}"
                f"\n{TextColors.WARNING} \nWARNING: \n"
                f"Blend_My_NFTs cannot generate {collection_size} NFTs."
                f" Only {len(dna_list)} NFT DNA were generated."

                f"\nThis might be for a number of reasons:"
                f"\n  a) Rarity is preventing combinations from being generated (See "
                f"https://github.com/torrinworx/Blend_My_NFTs#notes-on-rarity-and-weighted-variants).\n "
                f"\n  b) Logic is preventing combinations from being generated (See "
                f"https://github.com/torrinworx/Blend_My_NFTs#logic).\n "
                f"\n  c) The number of possible combinations of your NFT collection is too low. Add more Variants or "
                f"Attributes to increase the recommended collection size.\n "
                f"\n{TextColors.RESET}"
        )


# ======== LOADING ANIMATION ======== #

# This section is used for the loading animation used in the system console.

class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = [
                " [==     ]",
                " [ ==    ]",
                " [  ==   ]",
                " [   ==  ]",
                " [    == ]",
                " [     ==]",
                " [    == ]",
                " [   ==  ]",
                " [  ==   ]",
                " [ ==    ]",
        ]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


def activate_logging():
    """
    Used as an intermediate activated at runtime of the following operators: CreateData, ExportNFTs, ResumeFailedBatch,
    RefactorBatches, and ExportSettings. Must be independent of 'input' class to be safe, gets variables directly from
    bpy.
    """

    log_path = bpy.context.scene.input_tool.log_path
    if log_path:
        file_handler = logging.FileHandler(os.path.join(log_path, 'BMNFTs_Log.txt'), 'a')
    else:
        file_handler = logging.FileHandler(os.path.join(tempfile.gettempdir(), 'BMNFTs_Log.txt'), 'a')

    formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(filename)s > %(funcName)s() > Line:%(lineno)d]\n%(message)s\n'
    )
    file_handler.setFormatter(formatter)

    log = logging.getLogger()
    for handler in log.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            log.removeHandler(handler)
        if isinstance(handler, logging.StreamHandler):
            log.removeHandler(handler)
    log.addHandler(file_handler)

    # Record log to console:
    console_handler = logging.StreamHandler(sys.stdout)
    log.addHandler(console_handler)

    if bpy.context.scene.input_tool.enable_debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
