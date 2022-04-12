bl_info = {
    "name": "Blend_My_NFTs",
    "author": "Torrin Leonard, This Cozy Studio Inc",
    "version": (3, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "An open source, free to use Blender add-on that enables you to create thousands of unique images, animations, and 3D models.",
    "category": "Development",
}

# Import handling:

import bpy
from bpy.app.handlers import persistent

import os
import sys
import json
import importlib

#a little hacky bs
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

if bpy in locals():
        importlib.reload(DNA_Generator)
        importlib.reload(Batch_Sorter)
        importlib.reload(Exporter)
        importlib.reload(Refactorer)
        importlib.reload(get_combinations)
        importlib.reload(Checks)

else:
    from main import \
        DNA_Generator, \
        Batch_Sorter, \
        Exporter, \
        Refactorer, \
        get_combinations, \
        Checks

# User input Property Group:
class BMNFTS_PGT_MyProperties(bpy.types.PropertyGroup):

    # Main BMNFTS Panel properties: 

    nftName: bpy.props.StringProperty(name="NFT Name")

    collectionSize: bpy.props.IntProperty(name="NFT Collection Size", default=1, min=1)  # max=(combinations - offset)
    nftsPerBatch: bpy.props.IntProperty(name="NFTs Per Batch", default=1, min=1)  # max=(combinations - offset)
    batchToGenerate: bpy.props.IntProperty(name="Batch To Generate", default=1, min=1)  # max=(collectionSize / nftsPerBatch)

    save_path: bpy.props.StringProperty(
                        name="Save Path",
                        description="Save path for NFT files",
                        default="",
                        maxlen=1024,
                        subtype="DIR_PATH"
    )

    enableRarity: bpy.props.BoolProperty(name="Enable Rarity")

    imageBool: bpy.props.BoolProperty(name="Image")
    imageEnum: bpy.props.EnumProperty(
        name="Image File Format", 
        description="Select Image file format", 
        items=[
            ('PNG', ".PNG", "Export NFT as PNG"),
            ('JPEG', ".JPEG", "Export NFT as JPEG")
        ]
    )
    
    animationBool: bpy.props.BoolProperty(name="Animation")
    animationEnum: bpy.props.EnumProperty(
        name="Animation File Format", 
        description="Select Animation file format", 
        items=[
            ('AVI_JPEG', '.avi (AVI_JPEG)', 'Export NFT as AVI_JPEG'),
            ('AVI_RAW', '.avi (AVI_RAW)', 'Export NFT as AVI_RAW'),
            ('FFMPEG', '.mkv (FFMPEG)', 'Export NFT as FFMPEG'),
            ('MP4', '.mp4', 'Export NFT as .mp4')
        ]
    )

    modelBool: bpy.props.BoolProperty(name="3D Model")
    modelEnum: bpy.props.EnumProperty(
        name="3D Model File Format", 
        description="Select 3D Model file format", 
        items=[
            ('GLB', '.glb', 'Export NFT as .glb'),
            ('GLTF_SEPARATE', '.gltf + .bin + textures', 'Export NFT as .gltf with separated textures in .bin + textures.'),
            ('GLTF_EMBEDDED', '.gltf', 'Export NFT as embedded .gltf file that contains textures.'),
            ('FBX', '.fbx', 'Export NFT as .fbx'),
            ('OBJ', '.obj', 'Export NFT as .obj'),
            ('X3D', '.x3d', 'Export NFT as .x3d'),
            ('STL', '.stl', 'Export NFT as .stl'),
            ('VOX', '.vox (Experimental)', 'Export NFT as .vox, requires the voxwriter add on: https://github.com/Spyduck/voxwriter')
        ]
    )

    cardanoMetaDataBool: bpy.props.BoolProperty(name="Cardano Cip")
    solanaMetaDataBool: bpy.props.BoolProperty(name="Solana Metaplex")
    erc721MetaData: bpy.props.BoolProperty(name="ERC721")

    # API Panel properties:
    apiKey: bpy.props.StringProperty(name="API Key", subtype='PASSWORD')

    # Logic:
    enableLogic: bpy.props.BoolProperty(name="Enable Logic")
    logicFile: bpy.props.StringProperty(
                        name="Logic File",
                        description="Path where Logic.json is located.",
                        default="",
                        maxlen=1024,
                        subtype="FILE_PATH"
    )

    # Custom Metadata Fields:
    enableCustomFields: bpy.props.BoolProperty(name="Enable Custom Metadata Fields")
    customfieldsFile: bpy.props.StringProperty(
                        name="Custom Fields File",
                        description="Path where Custom_Fields.json is located.",
                        default="",
                        maxlen=1024,
                        subtype="FILE_PATH"
    )

    # Cardano Custom Metadata Fields
    cardano_description: bpy.props.StringProperty(name="Cardano description")

    # Solana Custom Metadata Fields

    solana_description: bpy.props.StringProperty(name="Solana description")

    # ERC721 Custom Metadata Fields
    erc721_description: bpy.props.StringProperty(name="ERC721 description")


def make_directories(save_path):
    Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFTs Output", "NFT_Data")
    batch_json_save_path = os.path.join(Blend_My_NFTs_Output, "Batch_Data")

    nftBatch_save_path = os.path.join(save_path, "Blend_My_NFTs Output", "Generated NFT Batches")

    if not os.path.exists(Blend_My_NFTs_Output):
        os.makedirs(Blend_My_NFTs_Output)
    if not os.path.exists(batch_json_save_path):
        os.makedirs(batch_json_save_path)
    if not os.path.exists(nftBatch_save_path):
        os.makedirs(nftBatch_save_path)
    return Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path


# Update NFT count:
combinations: int = 0
recommended_limit: int = 0

@persistent
def update_combinations(dummy1, dummy2):
    global combinations
    global recommended_limit
    global offset

    combinations = (get_combinations.get_combinations_from_scene())
    recommended_limit = int(round(combinations/2))

    redraw_panel()


bpy.app.handlers.depsgraph_update_post.append(update_combinations)


# Main Operators:
class createData(bpy.types.Operator):
    bl_idname = 'create.data'
    bl_label = 'Create Data'
    bl_description = 'Creates NFT Data. Run after any changes were made to scene.'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        nftName = bpy.context.scene.my_tool.nftName
        maxNFTs = bpy.context.scene.my_tool.collectionSize
        nftsPerBatch = bpy.context.scene.my_tool.nftsPerBatch
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        logicFile = bpy.path.abspath(bpy.context.scene.my_tool.logicFile)

        enableRarity = bpy.context.scene.my_tool.enableRarity
        enableLogic = bpy.context.scene.my_tool.enableLogic

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        DNA_Generator.send_To_Record_JSON(maxNFTs, nftsPerBatch, save_path, enableRarity, enableLogic, logicFile, Blend_My_NFTs_Output)
        Batch_Sorter.makeBatches(nftName, maxNFTs, nftsPerBatch, save_path, batch_json_save_path)

        self.report({'INFO'}, f"NFT Data created!")

        return {"FINISHED"}

class exportNFTs(bpy.types.Operator):
    bl_idname = 'exporter.nfts'
    bl_label = 'Export NFTs'
    bl_description = 'Generate and export a given batch of NFTs.'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        nftName = bpy.context.scene.my_tool.nftName
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        batchToGenerate = bpy.context.scene.my_tool.batchToGenerate
        maxNFTs = bpy.context.scene.my_tool.collectionSize

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        enableImages = bpy.context.scene.my_tool.imageBool
        imageFileFormat = bpy.context.scene.my_tool.imageEnum

        enableAnimations = bpy.context.scene.my_tool.animationBool
        animationFileFormat = bpy.context.scene.my_tool.animationEnum

        enableModelsBlender = bpy.context.scene.my_tool.modelBool
        modelFileFormat = bpy.context.scene.my_tool.modelEnum

        # fail state variables, set to no fail due to resume_failed_batch() Operator in BMNFTS_PT_GenerateNFTs Panel
        fail_state = False
        failed_batch = None
        failed_dna = None
        failed_dna_index = None

        Exporter.render_and_save_NFTs(nftName, maxNFTs, batchToGenerate, batch_json_save_path, nftBatch_save_path, enableImages,
                                      imageFileFormat, enableAnimations, animationFileFormat, enableModelsBlender,
                                      modelFileFormat, fail_state, failed_batch, failed_dna, failed_dna_index
                                      )

        self.report({'INFO'}, f"All NFTs generated for batch {batchToGenerate}!")

        return {"FINISHED"}

class resume_failed_batch(bpy.types.Operator):
    bl_idname = 'exporter.resume_nfts'
    bl_label = 'Resume Failed Batch'
    bl_description = 'Failed Batch detected. Generate NFTs where the previous batch failed?'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        nftName = bpy.context.scene.my_tool.nftName
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        batchToGenerate = bpy.context.scene.my_tool.batchToGenerate
        maxNFTs = bpy.context.scene.my_tool.collectionSize

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)
        fail_state, failed_batch, failed_dna, failed_dna_index = Checks.check_FailedBatches(batch_json_save_path)

        file_name = os.path.join(batch_json_save_path, "Batch{}.json".format(batchToGenerate))
        batch = json.load(open(file_name))

        nftBatch_save_path = batch["Generation Save"][-1]["Render_Settings"]["nftBatch_save_path"]
        enableImages = batch["Generation Save"][-1]["Render_Settings"]["enableImages"]
        imageFileFormat = batch["Generation Save"][-1]["Render_Settings"]["imageFileFormat"]
        enableAnimations = batch["Generation Save"][-1]["Render_Settings"]["enableAnimations"]
        animationFileFormat = batch["Generation Save"][-1]["Render_Settings"]["animationFileFormat"]
        enableModelsBlender = batch["Generation Save"][-1]["Render_Settings"]["enableModelsBlender"]
        modelFileFormat = batch["Generation Save"][-1]["Render_Settings"]["modelFileFormat"]

        Exporter.render_and_save_NFTs(nftName, maxNFTs, failed_batch, batch_json_save_path, nftBatch_save_path, enableImages,
                                      imageFileFormat, enableAnimations, animationFileFormat, enableModelsBlender,
                                      modelFileFormat, fail_state, failed_batch, failed_dna, failed_dna_index
                                      )

        self.report({'INFO'}, f"Resuming Failed Batch Generation!")

        return {"FINISHED"}

class refactor_Batches(bpy.types.Operator):
    """Refactor your collection? This action cannot be undone."""
    bl_idname = 'refactor.batches'
    bl_label = 'Refactor your Batches?'
    bl_description = 'This action cannot be undone.'
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        class refactor_panel_input:
            save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)

            custom_Fields_File = bpy.path.abspath(bpy.context.scene.my_tool.customfieldsFile)
            enableCustomFields = bpy.context.scene.my_tool.enableCustomFields

            cardanoMetaDataBool = bpy.context.scene.my_tool.cardanoMetaDataBool
            solanaMetaDataBool = bpy.context.scene.my_tool.solanaMetaDataBool
            erc721MetaData = bpy.context.scene.my_tool.erc721MetaData

            cardano_description = bpy.context.scene.my_tool.cardano_description
            solana_description = bpy.context.scene.my_tool.solana_description
            erc721_description = bpy.context.scene.my_tool.erc721_description

            Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        Refactorer.reformatNFTCollection(refactor_panel_input)
        self.report({'INFO'}, "Batches Refactored, MetaData created!")

        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

# Create Data Panel:
class BMNFTS_PT_CreateData(bpy.types.Panel):
    bl_label = "Create NFT Data"
    bl_idname = "BMNFTS_PT_CreateData"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.prop(mytool, "nftName")

        row = layout.row()
        layout.label(text=f"Maximum Number Of NFTs: {combinations}")
        layout.label(text=f"Recommended limit: {recommended_limit}")

        row = layout.row()
        row.prop(mytool, "collectionSize")

        row = layout.row()
        row.prop(mytool, "nftsPerBatch")

        row = layout.row()
        row.prop(mytool, "save_path")

        row = layout.row()
        row.prop(mytool, "enableRarity")

        row = layout.row()
        row.prop(mytool, "enableLogic")

        if bpy.context.scene.my_tool.enableLogic:
            row = layout.row()
            row.prop(mytool, "logicFile")

        row = layout.row()
        self.layout.operator("create.data", icon='DISCLOSURE_TRI_RIGHT', text="Create Data")

# Generate NFTs Panel:
class BMNFTS_PT_GenerateNFTs(bpy.types.Panel):
    bl_label = "Generate NFTs"
    bl_idname = "BMNFTS_PT_GenerateNFTs"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        layout.label(text="NFT Media files:")

        row = layout.row()
        row.prop(mytool, "imageBool")
        if bpy.context.scene.my_tool.imageBool:
            row.prop(mytool, "imageEnum")

        row = layout.row()
        row.prop(mytool, "animationBool")
        if bpy.context.scene.my_tool.animationBool:
            row.prop(mytool, "animationEnum")

        row = layout.row()
        row.prop(mytool, "modelBool")
        if bpy.context.scene.my_tool.modelBool:
            row.prop(mytool, "modelEnum")

        row = layout.row()
        row.prop(mytool, "batchToGenerate")

        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)
        fail_state, failed_batch, failed_dna, failed_dna_index = Checks.check_FailedBatches(batch_json_save_path)
        if fail_state:
            row = layout.row()
            self.layout.operator("exporter.nfts", icon='RENDER_RESULT', text="Generate NFTs")

            row = layout.row()
            row.alert = True
            row.operator("exporter.resume_nfts", icon='ERROR', text="Resume Failed Batch")

        if not fail_state:
            row = layout.row()
            self.layout.operator("exporter.nfts", icon='RENDER_RESULT', text="Generate NFTs")
# Refactor Batches & create MetaData Panel:
class BMNFTS_PT_Refactor(bpy.types.Panel):
    bl_label = "Refactor Batches & create MetaData"
    bl_idname = "BMNFTS_PT_Refactor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        layout.label(text="Meta Data format:")

        row = layout.row()
        row.prop(mytool, "cardanoMetaDataBool")
        if bpy.context.scene.my_tool.cardanoMetaDataBool:
            row = layout.row()
            row.prop(mytool, "cardano_description")

            row = layout.row()
            row.operator("wm.url_open", text="Cardano Metadata Documentation",
                         icon='URL').url = "https://cips.cardano.org/cips/cip25/"

        row = layout.row()
        row.prop(mytool, "solanaMetaDataBool")
        if bpy.context.scene.my_tool.solanaMetaDataBool:
            row = layout.row()
            row.prop(mytool, "solana_description")

            row = layout.row()
            row.operator("wm.url_open", text="Solana Metadata Documentation",
                         icon='URL').url = "https://docs.metaplex.com/token-metadata/specification"

        row = layout.row()
        row.prop(mytool, "erc721MetaData")
        if bpy.context.scene.my_tool.erc721MetaData:
            row = layout.row()
            row.prop(mytool, "erc721_description")

            row = layout.row()
            row.operator("wm.url_open", text="ERC721 Metadata Documentation",
                         icon='URL').url = "https://docs.opensea.io/docs/metadata-standards"

        row = layout.row()
        row.prop(mytool, "enableCustomFields")
        if bpy.context.scene.my_tool.enableCustomFields:
            row = layout.row()
            row.prop(mytool, "customfieldsFile")

        row = layout.row()
        self.layout.operator("refactor.batches", icon='FOLDER_REDIRECT', text="Refactor Batches & Create MetaData")

# Documentation Panel:
class BMNFTS_PT_Documentation(bpy.types.Panel):
    bl_label = "Documentation"
    bl_idname = "BMNFTS_PT_Documentation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.operator("wm.url_open", text="Documentation",
                     icon='URL').url = "https://github.com/torrinworx/Blend_My_NFTs"

#Export Settings Panel
#This panel gives the user the option to export all settings from the Blend_My_NFTs addon into a config file.
#Settings will be read from the config file when running headlessly.

class export_settings(bpy.types.Operator):
    """Export your settings into a configuration file"""
    bl_idname = 'export.settings'
    bl_label = 'Export Settings'
    bl_description = 'Save your settings to a configuration file'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context): 
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        filename = "config.cfg"
        
        settings = bpy.context.scene.my_tool;

        #could probably have made this a lot cleaner looking
        with open(save_path + filename, 'w') as f:
            output =  "#This file was auto-generated from the Blend_My_NFTs addon and is used" + "\n"
            output += "#when running Blend_My_NFTs in a headless environment." + "\n"
            output += "\n"
            output += "#The name of your nft project" + "\n"
            output += "nftName=" + settings.nftName + "\n"
            output += "\n"
            output += "#The number of NFTs to generate per batch" + "\n"
            output += "nftsPerBatch=" + str(settings.nftsPerBatch) + "\n"
            output += "\n"
            output += "#Save path for your NFT files" + "\n"
            output += "save_path=" + settings.save_path + "\n"
            output += "\n"
            output += "#Enable Rarity" + "\n"
            output += "enableRarity=" + str(settings.enableRarity) + "\n"
            output += "\n"
            output += "#Enable Logic" + "\n"
            output += "enableLogic=" + str(settings.enableLogic) + "\n"
            output += "\n"
            output += "#NFT Media output type(s):" + "\n"
            output += "imageBool=" + str(settings.imageBool) + "\n"
            output += "imageEnum=" + settings.imageEnum + "\n"
            output += "animationBool=" + str(settings.animationBool) + "\n"
            output += "animationEnum=" + settings.animationEnum + "\n"
            output += "modelBool=" + str(settings.modelBool) + "\n"
            output += "modelEnum=" + settings.modelEnum + "\n"
            output += "\n"
            output += "#Batch to generate" + "\n"
            output += "batchToGenerate=" + str(settings.batchToGenerate) + "\n"
            output += "\n"
            output += "#Metadata Format" + "\n"
            output += "cardanoMetaDataBool=" + str(settings.cardanoMetaDataBool) + "\n"
            output += "cardano_description=" + settings.cardano_description + "\n"
            output += "erc721MetaData=" + str(settings.erc721MetaData) + "\n"
            output += "erc721_description=" + settings.erc721_description + "\n"
            output += "solanaMetaDataBool=" + str(settings.solanaMetaDataBool) + "\n"
            output += "solana_description=" + settings.solana_description + "\n"
            output += "\n"
            output += "#Enable Custom Fields" + "\n"
            output += "enableCustomFields=" + str(settings.enableCustomFields) + "\n"
            output += "customfieldsFile=" + settings.customfieldsFile + "\n"

            print(output, file=f)

        self.report({'INFO'}, f"Saved settings to: {save_path + filename}!")

        return {"FINISHED"}

class BMNFTS_PT_ExportSettings(bpy.types.Panel):
    bl_label = "Export Settings"
    bl_idname = "BMNFTS_PT_ExportSettings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        self.layout.operator("export.settings", icon='FOLDER_REDIRECT', text="Export BMNFT settings to a file")


# # Materials Panel:
#
# class BMNFTS_PT_MATERIALS_Panel(bpy.types.Panel):
#     bl_label = "Materials"
#     bl_idname = "BMNFTS_PT_MATERIALS_Panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Blend_My_NFTs'
#
#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool
#

def redraw_panel():
    try:
        bpy.utils.unregister_class(BMNFTS_PT_CreateData)
    except:
        pass
    bpy.utils.register_class(BMNFTS_PT_CreateData)


# Register and Unregister classes from Blender:
classes = (
    BMNFTS_PGT_MyProperties,
    BMNFTS_PT_CreateData,
    BMNFTS_PT_GenerateNFTs,
    BMNFTS_PT_Refactor,
    BMNFTS_PT_Documentation,
    BMNFTS_PT_ExportSettings,

    # Other panels:
    # BMNFTS_PT_MATERIALS_Panel,

    createData,
    exportNFTs,
    resume_failed_batch,
    refactor_Batches,
    export_settings
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=BMNFTS_PGT_MyProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.my_tool

#For use when running from the command line
from main import HeadlessUtil

def runAsHeadless():
    args, parser = HeadlessUtil.getPythonArgs()

    with open(args.config_path, 'r') as f:
        settings = [line.strip() for line in f.readlines() if not(line[0] == '#' or len(line.strip()) < 1)]

        pairs = [setting.strip().split('=') for setting in settings]

        bpy.context.scene.my_tool.nftName = pairs[0][1]
        bpy.context.scene.my_tool.nftsPerBatch = int(pairs[1][1])
        bpy.context.scene.my_tool.save_path = pairs[2][1]
        bpy.context.scene.my_tool.enableRarity = pairs[3][1] == 'True'
        bpy.context.scene.my_tool.enableLogic = pairs[4][1] == 'True'
        bpy.context.scene.my_tool.imageBool = pairs[5][1] == 'True' 
        bpy.context.scene.my_tool.imageEnum = pairs[6][1]
        bpy.context.scene.my_tool.animationBool = pairs[7][1] == 'True'
        bpy.context.scene.my_tool.animationEnum = pairs[8][1]
        bpy.context.scene.my_tool.modelBool = pairs[9][1] == 'True'
        bpy.context.scene.my_tool.modelEnum = pairs[10][1]
        bpy.context.scene.my_tool.batchToGenerate = int(pairs[11][1])
        bpy.context.scene.my_tool.cardanoMetaDataBool = pairs[12][1] == 'True'
        bpy.context.scene.my_tool.cardano_description = pairs[13][1]
        bpy.context.scene.my_tool.erc721MetaData = pairs[14][1] == 'True'
        bpy.context.scene.my_tool.erc721_description = pairs[15][1]
        bpy.context.scene.my_tool.solanaMetaDataBool = pairs[16][1] == 'True'
        bpy.context.scene.my_tool.solanaDescription = pairs[17][1]
        bpy.context.scene.my_tool.enableCustomFields = pairs[18][1] == 'True'
        bpy.context.scene.my_tool.customfieldsFile = pairs[19][1]

    if args.save_path:
        bpy.context.scene.my_tool.save_path = save_path
        
    #don't mind me, just copy-pasting code around...
    if args.operation == 'create-dna':
        nftName = bpy.context.scene.my_tool.nftName
        maxNFTs = bpy.context.scene.my_tool.collectionSize
        nftsPerBatch = bpy.context.scene.my_tool.nftsPerBatch
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        logicFile = bpy.path.abspath(bpy.context.scene.my_tool.logicFile)

        enableRarity = bpy.context.scene.my_tool.enableRarity
        enableLogic = bpy.context.scene.my_tool.enableLogic

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        DNA_Generator.send_To_Record_JSON(maxNFTs, nftsPerBatch, save_path, enableRarity, enableLogic, logicFile, Blend_My_NFTs_Output)
        Batch_Sorter.makeBatches(nftName, maxNFTs, nftsPerBatch, save_path, batch_json_save_path)
        
    elif args.operation == 'generate-nfts':
        nftName = bpy.context.scene.my_tool.nftName
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        batchToGenerate = bpy.context.scene.my_tool.batchToGenerate
        maxNFTs = bpy.context.scene.my_tool.collectionSize

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        enableImages = bpy.context.scene.my_tool.imageBool
        imageFileFormat = bpy.context.scene.my_tool.imageEnum

        enableAnimations = bpy.context.scene.my_tool.animationBool
        animationFileFormat = bpy.context.scene.my_tool.animationEnum

        enableModelsBlender = bpy.context.scene.my_tool.modelBool
        modelFileFormat = bpy.context.scene.my_tool.modelEnum

        # fail state variables, set to no fail due to resume_failed_batch() Operator in BMNFTS_PT_GenerateNFTs Panel
        fail_state = False
        failed_batch = None
        failed_dna = None
        failed_dna_index = None

        Exporter.render_and_save_NFTs(nftName, maxNFTs, batchToGenerate, batch_json_save_path, nftBatch_save_path, enableImages,
                                      imageFileFormat, enableAnimations, animationFileFormat, enableModelsBlender,
                                      modelFileFormat, fail_state, failed_batch, failed_dna, failed_dna_index
                                      )
    elif args.operation == 'refactor-batches':
        class refactorData:
            save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)

            custom_Fields_File = bpy.path.abspath(bpy.context.scene.my_tool.customfieldsFile)
            enableCustomFields = bpy.context.scene.my_tool.enableCustomFields

            cardanoMetaDataBool = bpy.context.scene.my_tool.cardanoMetaDataBool
            solanaMetaDataBool = bpy.context.scene.my_tool.solanaMetaDataBool
            erc721MetaData = bpy.context.scene.my_tool.erc721MetaData

            cardano_description = bpy.context.scene.my_tool.cardano_description
            solana_description = bpy.context.scene.my_tool.solana_description
            erc721_description = bpy.context.scene.my_tool.erc721_description

            Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        Refactorer.reformatNFTCollection(refactorData)

        
if __name__ == '__main__':
    register()
    
    runAsHeadless()
