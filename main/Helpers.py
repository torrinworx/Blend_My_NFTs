import bpy
import os
import json
import platform
from time import sleep
from itertools import cycle
from threading import Thread
from shutil import get_terminal_size
from collections import Counter, defaultdict

from . import DNA_Generator


# ======== CONSTANTS ======== #

# This section is used for debugging, coding, or general testing purposes.


def enable_debug(enable_debug_bool):
    if enable_debug_bool:
        import logging

        logging.basicConfig(
            filename="./log.txt",
            level=logging.DEBUG,
            format='[%(levelname)s][%(asctime)s]\n%(message)s\n',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


# ======== CONSTANTS ======== #

# Constants are used for storing or updating constant values that may need to be changes depending on system
# requirements and different use-cases.

removeList = [".gitignore", ".DS_Store", "desktop.ini", ".ini"]


def remove_file_by_extension(dirlist):
    """
    Checks if a given directory list contains any of the files or file extensions listed above, if so, remove them from
    list and return a clean dir list. These files interfer with BMNFTs operations and should be removed whenever dealing
    with directories.
    """

    if str(type(dirlist)) == "<class 'list'>":
        dirlist = list(dirlist)  # converts single string path to list if dir pasted as string

    return_dirs = []
    for directory in dirlist:
        if not str(os.path.split(directory)[1]) in removeList:
            return_dirs.append(directory)

    return return_dirs


class bcolors:
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

# This section is used to get the number of combinations for checks and the UI display

def get_combinations():
    """
    Returns "combinations", the number of all possible NFT DNA for a given Blender scene formatted to BMNFTs conventions
    combinations.
    """

    hierarchy = DNA_Generator.get_hierarchy()
    hierarchyByNum = []

    for i in hierarchy:
        # Ignore Collections with nothing in them
        if len(hierarchy[i]) != 0:
            hierarchyByNum.append(len(hierarchy[i]))
        else:
            print(f"The following collection has been identified as empty: {i}")

    combinations = 1
    for i in hierarchyByNum:
        combinations = combinations * i

    return combinations


# ======== CHECKS ======== #

# This section is used to check the NFTRecord.json for duplicate NFT DNA and returns any found in the console.
# It also checks the percentage each variant is chosen in the NFTRecord, then compares it with its rarity percentage
# set in the .blend file.

# This section is provided for transparency. The accuracy of the rarity values you set in your .blend file as outlined
# in the README.md file are dependent on the maxNFTs, and the maximum number of combinations of your NFT collection.

def check_Scene():  # Not complete
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
        raise TypeError(
            f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
            f"Add a Script_Ignore collection to your Blender scene and ensure the name is exactly 'Script_Ignore'. For more information, "
            f"see:"
            f"\nhttps://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n{bcolors.RESET}"
        )

    hierarchy = DNA_Generator.get_hierarchy()
    collections = bpy.context.scene.collection

    # attribute_naming_conventions


def check_Rarity(hierarchy, DNAListFormatted, save_path):
    """Checks rarity percentage of each Variant, then sends it to RarityData.json in NFT_Data folder."""

    DNAList = []
    for i in DNAListFormatted:
        DNAList.append(list(i.keys())[0])

    numNFTsGenerated = len(DNAList)

    numDict = defaultdict(list)

    hierarchy.keys()

    for i in DNAList:
        dnaSplitList = i.split("-")

        for j, k in zip(dnaSplitList, hierarchy.keys()):
            numDict[k].append(j)

    numDict = dict(numDict)

    for i in numDict:
        count = dict(Counter(numDict[i]))
        numDict[i] = count

    fullNumName = {}

    for i in hierarchy:
        fullNumName[i] = {}
        for j in hierarchy[i]:
            variantNum = hierarchy[i][j]["number"]

            fullNumName[i][variantNum] = j

    completeData = {}

    for i, j in zip(fullNumName, numDict):
        x = {}

        for k in fullNumName[i]:

            for l in numDict[j]:
                if l == k:
                    name = fullNumName[i][k]
                    num = numDict[j][l]
                    x[name] = [(str(round(((num / numNFTsGenerated) * 100), 2)) + "%"), str(num)]

        completeData[i] = x

    print(
        f"\n{bcolors.OK}\n"
        f"Rarity Checker is active. These are the percentages for each variant per attribute you set in your .blend file:"
        f"\n{bcolors.RESET}"
    )

    for i in completeData:
        print(i + ":")
        for j in completeData[i]:
            print("   " + j + ": " + completeData[i][j][0] + "   Occurrences: " + completeData[i][j][1])

    jsonMetaData = json.dumps(completeData, indent=1, ensure_ascii=True)

    with open(os.path.join(save_path, "RarityData.json"), 'w') as outfile:
        outfile.write(jsonMetaData + '\n')
    path = os.path.join(save_path, "RarityData.json")
    print(bcolors.OK + f"Rarity Data has been saved to {path}." + bcolors.RESET)


def check_Duplicates(DNAListFormatted):
    """Checks if there are duplicates in DNAList before NFTRecord.json is sent to JSON file."""
    DNAList = []
    for i in DNAListFormatted:
        DNAList.append(list(i.keys())[0])

    duplicates = 0
    seen = set()

    for x in DNAList:
        if x in seen:
            print(x)
            duplicates += 1
        seen.add(x)

    print(f"\nNFTRecord.json contains {duplicates} duplicate NFT DNA.")


def check_FailedBatches(batch_json_save_path):
    fail_state = False
    failed_batch = None
    failed_dna = None
    failed_dna_index = None

    if os.path.isdir(batch_json_save_path):
        batch_folders = remove_file_by_extension(os.listdir(batch_json_save_path))

        for i in batch_folders:
            batch = json.load(open(os.path.join(batch_json_save_path, i)))
            NFTs_in_Batch = batch["NFTs_in_Batch"]
            if "Generation Save" in batch:
                dna_generated = batch["Generation Save"][-1]["DNA Generated"]
                if dna_generated is not None and dna_generated < NFTs_in_Batch:
                    fail_state = True
                    failed_batch = int(i.removeprefix("Batch").removesuffix(".json"))
                    failed_dna = dna_generated

    return fail_state, failed_batch, failed_dna, failed_dna_index


# Raise Errors:
def raise_Error_numBatches(maxNFTs, nftsPerBatch):
    """Checks if number of Batches is less than maxNFTs, if not raises error."""

    try:
        numBatches = maxNFTs / nftsPerBatch
        return numBatches
    except ZeroDivisionError:
        raise ZeroDivisionError(
            f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
            f"The number of NFTs per Batch must be greater than ZERO."
            f"Please review your Blender scene and ensure it follows "
            f"the naming conventions and scene structure. For more information, "
            f"see:\n{bcolors.RESET}"
            f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n{bcolors.RESET}"
        )


def raise_Error_ZeroCombinations():
    """Checks if combinations is greater than 0, if so, raises error."""
    if get_combinations() == 0:
        raise ValueError(
            f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
            f"The number of all possible combinations is ZERO. Please review your Blender scene and ensure it follows "
            f"the naming conventions and scene structure. For more information, "
            f"see:\n{bcolors.RESET}"
            f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n{bcolors.RESET}"
        )


def raise_Error_numBatchesGreaterThan(numBatches):
    if numBatches < 1:
        raise ValueError(
            f"\n{bcolors.ERROR}Blend_My_NFTs Error:\n"
            f"The number of Batches is less than 1. Please review your Blender scene and ensure it follows "
            f"the naming conventions and scene structure. For more information, "
            f"see:\n{bcolors.RESET}"
            f"https://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n{bcolors.RESET}"
        )


# Raise Warnings:
def raise_Warning_maxNFTs(nftsPerBatch, collectionSize):
    """
    Prints warning if nftsPerBatch is greater than collectionSize.
    """

    if nftsPerBatch > collectionSize:
        raise ValueError(
            f"\n{bcolors.WARNING}Blend_My_NFTs Warning:\n"
            f"The number of NFTs Per Batch you set is smaller than the NFT Collection Size you set.\n{bcolors.RESET}"
        )


def raise_Warning_collectionSize(DNAList, collectionSize):
    """
    Prints warning if BMNFTs cannot generate requested number of NFTs from a given collectionSize.
    """

    if len(DNAList) < collectionSize:
        print(f"\n{bcolors.WARNING} \nWARNING: \n"
              f"Blend_My_NFTs cannot generate {collectionSize} NFTs."
              f" Only {len(DNAList)} NFT DNA were generated."

              f"\nThis might be for a number of reasons:"
              f"\n  a) Rarity is preventing combinations from being generated (See https://github.com/torrinworx/Blend_My_NFTs#notes-on-rarity-and-weighted-variants).\n"
              f"\n  b) Logic is preventing combinations from being generated (See https://github.com/torrinworx/Blend_My_NFTs#logic).\n"
              f"\n  c) The number of possible combinations of your NFT collection is too low. Add more Variants or Attributes to increase the recommended collection size.\n"
              f"\n{bcolors.RESET}")


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
