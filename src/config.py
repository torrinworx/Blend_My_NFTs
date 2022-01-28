# Purpose:
# This file determines the settings of your NFT collection. Please read the README.md file to understand how to run this
# program.

nftName = 'Test'  # The name of the NFT image produces by PNG-Generator

maxNFTs = 10  # The maximum number of NFTs you want to generate.
nftsPerBatch = 10  # Number of NFTs per batch (Batches split maxNFTs into smaller manageable chunks)
renderBatch = 1  # The batch number to render in Exporter.py

imageFileFormat = 'PNG'  # Dictate the image extension when Blender renders the images
# Type the exact name provided below in the '' above:
# JPEG - Exports the .jpeg format
# PNG - Exports the .png format
# Visit https://docs.blender.org/api/current/bpy.types.Image.html#bpy.types.Image.file_format
# for a complete list of file formats supported by Blender. (Only use Image file extensions with imageFileFormat, 3D
# object, or animation file extensions will cause the program to fail)

animationFileFormat = ''  # Dictate the animations extension when Blender renders and compiles the images
# Type the exact name provided below in the '' above:
# AVI_JPEG - Exports the .avi jpeg format
# AVI_RAW - Exports the .avi raw format
# FFMPEG - Encodes the video using ffmpeg. Set your encoding settings in the Output Properties in Blender. Default is
# medium-quality .mp4 video.
# Visit https://docs.blender.org/api/current/bpy.types.Image.html#bpy.types.Image.file_format
# for a complete list of file formats supported by Blender. (These are the Blender only supported animation formats)

modelFileFormat = ''  # The file format of the objects you would like to export
# Type the exact name provided below in the '' above:
# fbx - The .FBX file format
# glb - The .glb file format
# obj - The .obj file format *Exports both a .obj and a .mtl files for the same generated object
# x3d - The .x3d file format
# Visit https://docs.blender.org/api/current/bpy.ops.export_scene.html?highlight=export_scene#module-bpy.ops.export_scene
# for a complete list of object formats supported by Blender.

# The path to Blend_My_NFTs folder:
save_path_mac = '/Users/torrinleonard/Desktop/ThisCozyStudio/Blend_My_NFTs'
save_path_linux = ''
save_path_windows = r''
# Place the path in the '', e.g: save_path_mac = '/Users/Path/to/Blend_My_NFTs'
# Example mac: /Users/Path/to/Blend_My_NFTs
# Example linux: /Users/Path/to/Blend_My_NFTs
# Example windows: C:\Users\Path\to\Blend_My_NFTs

# Set to True to generate images or 3D models depending on your settings below when main.py is run in Blender. Only works
# if you have already generated NFTRecord.json and all batches.
enableExporter = False

enableImages = False  # Renders and exports Images when main.py is run in Blender if enableExporter = True
enableAnimations = False  # Renders and exports Animations when main.py is run in Blender if enableExporter = True
enableModelsBlender = False  # Generates 3D models when main.py is run in Blender if enableExporter = True
# ^^ Generates models with .blend file NOT external object library.

# Enables Rarity_Sorter to weigh NFT DNA attributes and variants:
enableRarity = False
# generateColors must be turned off and enableMaxNFTs must be turned on.
# True = include weighted rarity percentages in NFTRecord.json calculations,
# False = Pure random selection of variants
# Note: The more attributes and variants you have, and by nature the more possible NFT combinations you have, the more
# accurate your percentages will be.

refactorBatchOrder = False  # When set to True, sorts, renames, and moves all NFTs files in all batches in NFT_Output
# folder to the Complete_Collection folder.
# After you generate all batches move them all to one computer and place them in the NFT_Output folder of Blend_My_NFTs.
# Run main.py with refactorBatchOrder set to True and all NFT files will be renamed and sorted into a folder called Complete_Collection.

# Meta Data Templates - Run after refactorBatchOrder
# Set the following to True to generate the format of the Meta Data template for your NFTs blockchain. (You can use multiple)
cardanoMetaData = False  # Cardano - Format Source: https://cips.cardano.org/cips/cip25/
solanaMetaData = False  # Solana - Format Source: https://docs.metaplex.com/nft-standard
erc721MetaData = False  # Ethereum ERC721 - Format Source: https://docs.opensea.io/docs/metadata-standards

turnNumsOff = True  # When set to True, turns off the extension numbers representing order and rarity from the names of
# variants in meta Data.

# NOTE: This is just the information Blend_My_NFTs can provide, you will have to add policy ID, URI information, etc
# yourself when you upload and mint your NFT collection.
# DISCLAIMER: These are only templates based on the common standards for the given blockchain, you will have to modify
# and fill them in with a script of your own when you mint your NFT collection. These metadata templates are only provided
# for your convenience and are as accurate to the standards above that I could make them.

metaDataDescription = ''  # The description of your NFT that will be inserted into its meta data

# ADVANCED FEATURES:
### Select colour or material.###
# Object generation options:
enableGeneration = False  # When set to true this applies the sets of colors listed below to the objects in the collections named below

generationType = 'material'  # You can either set 'color' or 'material' here. Type you set will correspond to following options.
# generationType = 'material' mode is experimental. Be sure that you back-up your file.
# You need to set materials as "fake user". Do not miss this step. Or your materials going to vanish after running this script.

# The collections below are RGBA Color values. You can put as many or as little color values in these lists as you would like.
# You can create any number of rgbaColorLists and assign them to any number of collections that you would like.
# Each set of rgbaColorList1 assigned to an object by collection name in the colorList will act like an attribute and create a unique variant of that item.
rgbaColorList1 = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 1, 1), (.5, 0, 0, 1)]
rgbaColorList2 = [(1, 1, 0, 1), (0, 1, 1, 1), (.5, 0, 1, 1), (.5, 1, 1, 1), (0, .5, 0, 1)]
# The following color list can be as long or as short as you want it to be.
# To use this all you need to do is place the name of the collection you want colored in the "" and the set of colors you want to apply to it after the :
# The collection named can only contain objects and not sub collections. Every object in the collection will be set to the colors you assigned above for each attribute
if generationType == 'color':  # Do not change this line.
    colorList = {"Cube_1_33": rgbaColorList1, "Sphere_4_0": rgbaColorList2}

### These materials must be in your Current Files' Materials. Make sure that you've set your materials as "fake user". ###
# The collections below are Current Files' Materials. You can put as many or as little materials values in these lists as you would like.
# You can create any number of materialLists and assign them to any number of collections that you would like.
# Each set of materialLists assigned to an object by collection name in the materialList will act like an attribute and create a unique variant of that item.
materialList1 = ['Material1', 'Material1.001', 'Material1.002', 'Material1.003', 'Material1.004']
materialList2 = ['Material2', 'Material2.001', 'Material2.002', 'Material2.003', 'Material2.004']

# The following material list can be as long or as short as you want it to be.
# To use this all you need to do is place the name of the collection you want materials assigned in the "" and the set of materials you want to apply to it after the :
# The collection named can only contain objects and not sub collections. Every object in the collection will be set to the materials you assigned above for each attribute
if generationType == 'material':  # Do not change this line.
    colorList = {"Cube_1_33": materialList1, "Sphere_2_0": materialList2}

enableResetViewport = True  # If True: turns all viewport and render cameras on after Image_Generator is finished operations

# 3D model imports and exports variables:
enable3DModels = False  # Set to True if using external models as attributes instead of Blender objects
# ^Does not work with colour options and rarity, both must be turned off in order to use this.

# Tests and Previews:

# Preview and render test settings:
# Set to True to run Preview test, set to False to stop test. Run main.py in Blender to initiate the test. Results will
# be displayed in the Blender terminal or console. enableExporter must be False, and enableImages and/or enableModelsBlender
# to run a preview.
runPreview = False
maxNFTsTest = 5  # Increase to get a more accurate reading of the render time. The number of images generated in the render test.

# Turn this on when you run main.py to generate NFTRecord.json and appropriate batches to confirm there are no duplicate
# NFT DNA. Note - This file is provided for transparency, it is impossible for duplicates to be made with the current code in
# DNA_Generator.py.
checkDups = False

# Turn this on when running main.py to generate NFTRecord.json and Batch#.json files to record the rarity percentage of each variant.
# Note - This file is provided for transparency. The accuracy of the rarity values you set in your .blend file as outlined
# in the README.md file are dependent on the maxNFTs, and the maximum number of combinations of your NFT collection.
checkRarity = False

# Utilities - DO NOT TOUCH:
import platform
import os

# Save_path utilities and os compatibility
mac = 'Darwin'
linux = 'Linux'
windows = 'Windows'
save_path = None

if platform.system() == mac:
    save_path = save_path_mac
elif platform.system() == linux:
    save_path = save_path_linux
elif platform.system() == windows:
    save_path = save_path_windows

# Paths to folders
batch_json_save_path = os.path.join(save_path, 'Batch_Json_files')  # The output path for batches generated by Batch_Sorter.py
nft_save_path = os.path.join(save_path, 'NFT_Output')  # The output path for images generated by Exporter.py
modelAssetPath = os.path.join(save_path, "3D_Model_Input")  # The input path for 3D models
model_save_path = os.path.join(save_path, "3D_Model_Output")  # The output path for 3D models generated by Model_Generator.py
model_Script_Ignore_Path = os.path.join(modelAssetPath, "Script_Ignore_Folder")  # The path to the Script_Ignore_Folder for 3D models

# error handling #
if modelFileFormat not in ['fbx', 'glb', 'obj', 'x3d'] and enable3DModels:
    raise ValueError("Output format in `objectFormatExport` can only be 'fbx', 'glb', 'obj', 'x3d'.")
