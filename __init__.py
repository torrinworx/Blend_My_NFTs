bl_info = {
    "name": "Blend_My_NFTs",
    "author": "Torrin Leonard, This Cozy Studio Inc",
    "version": (3, 2, 0),
    "blender": (3, 1, 3),
    "location": "View3D",
    "description": "An open source, free to use Blender add-on that enables you to create thousands of unique images, animations, and 3D models.",
    "category": "Development",
}


# ======== Import handling ======== #

import bpy
from bpy.app.handlers import persistent

import os
import sys
import json
import importlib

# "a little hacky bs" - Matthew TheBrochacho ;)
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

if bpy in locals():
        importlib.reload(DNA_Generator)
        importlib.reload(Batch_Sorter)
        importlib.reload(Exporter)
        importlib.reload(Refactorer)
        importlib.reload(get_combinations)
        importlib.reload(Checks)
        importlib.reload(HeadlessUtil)
else:
    from main import \
        DNA_Generator, \
        Batch_Sorter, \
        Exporter, \
        Refactorer, \
        get_combinations, \
        Checks, \
        HeadlessUtil


# ======== Persistant UI Refresh ======== #

# Used for updating text and buttons in UI panels
combinations: int = 0
recommended_limit: int = 0

@persistent
def Refresh_UI(dummy1, dummy2):
    """
    Refreshes the UI upon user interacting with Blender (using depsgraph_update_post handler). Might be a better handler
    to use.
    """
    global combinations
    global recommended_limit

    combinations = (get_combinations.get_combinations())
    recommended_limit = int(round(combinations/2))

    # Add panel classes that require refresh to this refresh_panels tuple:
    refresh_panel_classes = (
        BMNFTS_PT_CreateData,
    )

    def redraw_panel(refresh_panel_classes):
        for i in refresh_panel_classes:
            try:
                bpy.utils.unregister_class(i)
            except:
                pass
            bpy.utils.register_class(i)

    redraw_panel(refresh_panel_classes)

bpy.app.handlers.depsgraph_update_post.append(Refresh_UI)


# ======== Helper functions ======== #
def make_directories(save_path):
    """Makes all Blend_My_NFTs Output folder directories from save_path input."""
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

def runAsHeadless():
    """
    For use when running from the command line.
    """
    def dumpSettings(settings):
        output = (
            f"nftName={settings.nftName}\n"
            f"collectionSize={str(settings.collectionSize)}\n"
            f"nftsPerBatch={str(settings.nftsPerBatch)}\n"
            f"save_path={settings.save_path}\n"
            f"enableRarity={(settings.enableRarity)}\n"
            f"enableLogic={str(settings.enableLogic)}\n"
            f"imageBool={str(settings.imageBool)}\n"
            f"imageEnum={settings.imageEnum}\n"
            f"animationBool={str(settings.animationBool)}\n"
            f"animationEnum={settings.animationEnum}\n"
            f"modelBool={str(settings.modelBool)}\n"
            f"modelEnum={settings.modelEnum}\n"
            f"batchToGenerate={str(settings.batchToGenerate)}\n"
            f"cardanoMetaDataBool={str(settings.cardanoMetaDataBool)}\n"
            f"cardano_description={settings.cardano_description}\n"
            f"erc721MetaData={str(settings.erc721MetaData)}\n"
            f"erc721_description={settings.erc721_description}\n"
            f"solanaMetaDataBool={str(settings.solanaMetaDataBool)}\n"
            f"solana_description={settings.solana_description}\n"
            f"enableCustomFields={str(settings.enableCustomFields)}\n"
            f"customfieldsFile={settings.customfieldsFile}\n"
        )
        print(output)

    args, parser = HeadlessUtil.getPythonArgs()

    settings = bpy.context.scene.input_tool

    # dumpSettings(settings)

    with open(args.config_path, 'r') as f:
        configs = [line.strip() for line in f.readlines() if not (line[0] == '#' or len(line.strip()) < 1)]

        pairs = [config.strip().split('=') for config in configs]

        # print(pairs)

        settings.nftName = pairs[0][1]
        settings.collectionSize = int(pairs[1][1])
        settings.nftsPerBatch = int(pairs[2][1])
        settings.save_path = pairs[3][1]
        settings.enableRarity = pairs[4][1] == 'True'
        settings.enableLogic = pairs[5][1] == 'True'
        settings.imageBool = pairs[6][1] == 'True'
        settings.imageEnum = pairs[7][1]
        settings.animationBool = pairs[8][1] == 'True'
        settings.animationEnum = pairs[9][1]
        settings.modelBool = pairs[10][1] == 'True'
        settings.modelEnum = pairs[11][1]
        settings.batchToGenerate = int(pairs[12][1])
        settings.cardanoMetaDataBool = pairs[13][1] == 'True'
        settings.cardano_description = pairs[14][1]
        settings.erc721MetaData = pairs[15][1] == 'True'
        settings.erc721_description = pairs[16][1]
        settings.solanaMetaDataBool = pairs[17][1] == 'True'
        settings.solanaDescription = pairs[18][1]
        settings.enableCustomFields = pairs[19][1] == 'True'
        settings.customfieldsFile = pairs[20][1]

    if args.save_path:
        settings.save_path = args.save_path

    if args.batch_number:
        settings.batchToGenerate = args.batch_number

    # dumpSettings(settings)

    # don't mind me, just copy-pasting code around...
    if args.operation == 'create-dna':
        nftName = settings.nftName
        maxNFTs = settings.collectionSize
        nftsPerBatch = settings.nftsPerBatch
        save_path = bpy.path.abspath(settings.save_path)
        logicFile = bpy.path.abspath(settings.logicFile)

        enableRarity = settings.enableRarity
        enableLogic = settings.enableLogic

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        DNA_Generator.send_To_Record_JSON(maxNFTs, nftsPerBatch, save_path, enableRarity, enableLogic, logicFile,
                                          Blend_My_NFTs_Output)
        Batch_Sorter.makeBatches(nftName, maxNFTs, nftsPerBatch, save_path, batch_json_save_path)

    elif args.operation == 'generate-nfts':
        nftName = settings.nftName
        save_path = bpy.path.abspath(settings.save_path)
        batchToGenerate = settings.batchToGenerate
        maxNFTs = settings.collectionSize

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        if args.batch_data_path:
            batch_json_save_path = args.batch_data_path;

        enableImages = settings.imageBool
        imageFileFormat = settings.imageEnum

        enableAnimations = settings.animationBool
        animationFileFormat = settings.animationEnum

        enableModelsBlender = settings.modelBool
        modelFileFormat = settings.modelEnum

        # fail state variables, set to no fail due to resume_failed_batch() Operator in BMNFTS_PT_GenerateNFTs Panel
        fail_state = False
        failed_batch = None
        failed_dna = None
        failed_dna_index = None

        Exporter.render_and_save_NFTs(nftName, maxNFTs, batchToGenerate, batch_json_save_path, nftBatch_save_path,
                                      enableImages,
                                      imageFileFormat, enableAnimations, animationFileFormat, enableModelsBlender,
                                      modelFileFormat, fail_state, failed_batch, failed_dna, failed_dna_index
                                      )
    elif args.operation == 'refactor-batches':
        class refactorData:
            save_path = bpy.path.abspath(settings.save_path)

            custom_Fields_File = bpy.path.abspath(settings.customfieldsFile)
            enableCustomFields = settings.enableCustomFields

            cardanoMetaDataBool = settings.cardanoMetaDataBool
            solanaMetaDataBool = settings.solanaMetaDataBool
            erc721MetaData = settings.erc721MetaData

            cardano_description = settings.cardano_description
            solana_description = settings.solana_description
            erc721_description = settings.erc721_description

            Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        Refactorer.reformatNFTCollection(refactorData)


# ======== User input Property Group ======== #
class BMNFTS_PGT_Input_Properties(bpy.types.PropertyGroup):

    # Create NFT Data Panel:

    nftName: bpy.props.StringProperty(name="NFT Name")

    collectionSize: bpy.props.IntProperty(name="NFT Collection Size", default=1, min=1)  # max=(combinations - offset)
    nftsPerBatch: bpy.props.IntProperty(name="NFTs Per Batch", default=1, min=1)  # max=(combinations - offset)

    save_path: bpy.props.StringProperty(
                        name="Save Path",
                        description="Save path for NFT files",
                        default="",
                        maxlen=1024,
                        subtype="DIR_PATH"
    )

    enableRarity: bpy.props.BoolProperty(name="Enable Rarity")

    enableLogic: bpy.props.BoolProperty(name="Enable Logic")
    logicFile: bpy.props.StringProperty(
                        name="Logic File",
                        description="Path where Logic.json is located.",
                        default="",
                        maxlen=1024,
                        subtype="FILE_PATH"
    )

    # Generate NFTs Panel:
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

    batchToGenerate: bpy.props.IntProperty(name="Batch To Generate", default=1, min=1)  # max=(collectionSize / nftsPerBatch)

    # Refactor Batches & Create Metadata Panel:
    cardanoMetaDataBool: bpy.props.BoolProperty(name="Cardano Cip")
    cardano_description: bpy.props.StringProperty(name="Cardano description")

    solanaMetaDataBool: bpy.props.BoolProperty(name="Solana Metaplex")
    solana_description: bpy.props.StringProperty(name="Solana description")

    erc721MetaData: bpy.props.BoolProperty(name="ERC721")
    erc721_description: bpy.props.StringProperty(name="ERC721 description")

    enableCustomFields: bpy.props.BoolProperty(name="Enable Custom Metadata Fields")
    customfieldsFile: bpy.props.StringProperty(
                        name="Custom Fields File",
                        description="Path where Custom_Fields.json is located.",
                        default="",
                        maxlen=1024,
                        subtype="FILE_PATH"
    )

    # Other Panel:

    # API Panel properties:
    apiKey: bpy.props.StringProperty(name="API Key", subtype='PASSWORD')


# ======== Main Operators ======== #
class createData(bpy.types.Operator):
    bl_idname = 'create.data'
    bl_label = 'Create Data'
    bl_description = 'Creates NFT Data. Run after any changes were made to scene.'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        nftName = bpy.context.scene.input_tool.nftName
        collectionSize = bpy.context.scene.input_tool.collectionSize
        nftsPerBatch = bpy.context.scene.input_tool.nftsPerBatch
        save_path = bpy.path.abspath(bpy.context.scene.input_tool.save_path)
        logicFile = bpy.path.abspath(bpy.context.scene.input_tool.logicFile)

        enableRarity = bpy.context.scene.input_tool.enableRarity
        enableLogic = bpy.context.scene.input_tool.enableLogic

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        DNA_Generator.send_To_Record_JSON(collectionSize, nftsPerBatch, save_path, enableRarity, enableLogic, logicFile, Blend_My_NFTs_Output)
        Batch_Sorter.makeBatches(nftName, collectionSize, nftsPerBatch, save_path, batch_json_save_path)

        self.report({'INFO'}, f"NFT Data created!")

        return {"FINISHED"}

class exportNFTs(bpy.types.Operator):
    bl_idname = 'exporter.nfts'
    bl_label = 'Export NFTs'
    bl_description = 'Generate and export a given batch of NFTs.'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        nftName = bpy.context.scene.input_tool.nftName
        save_path = bpy.path.abspath(bpy.context.scene.input_tool.save_path)
        batchToGenerate = bpy.context.scene.input_tool.batchToGenerate
        collectionSize = bpy.context.scene.input_tool.collectionSize

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        enableImages = bpy.context.scene.input_tool.imageBool
        imageFileFormat = bpy.context.scene.input_tool.imageEnum

        enableAnimations = bpy.context.scene.input_tool.animationBool
        animationFileFormat = bpy.context.scene.input_tool.animationEnum

        enableModelsBlender = bpy.context.scene.input_tool.modelBool
        modelFileFormat = bpy.context.scene.input_tool.modelEnum

        # fail state variables, set to no fail due to resume_failed_batch() Operator in BMNFTS_PT_GenerateNFTs Panel
        fail_state = False
        failed_batch = None
        failed_dna = None
        failed_dna_index = None

        Exporter.render_and_save_NFTs(nftName, collectionSize, batchToGenerate, batch_json_save_path, nftBatch_save_path, enableImages,
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
        nftName = bpy.context.scene.input_tool.nftName
        save_path = bpy.path.abspath(bpy.context.scene.input_tool.save_path)
        batchToGenerate = bpy.context.scene.input_tool.batchToGenerate
        collectionSize = bpy.context.scene.input_tool.collectionSize

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

        Exporter.render_and_save_NFTs(nftName, collectionSize, failed_batch, batch_json_save_path, nftBatch_save_path, enableImages,
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
            save_path = bpy.path.abspath(bpy.context.scene.input_tool.save_path)

            custom_Fields_File = bpy.path.abspath(bpy.context.scene.input_tool.customfieldsFile)
            enableCustomFields = bpy.context.scene.input_tool.enableCustomFields

            cardanoMetaDataBool = bpy.context.scene.input_tool.cardanoMetaDataBool
            solanaMetaDataBool = bpy.context.scene.input_tool.solanaMetaDataBool
            erc721MetaData = bpy.context.scene.input_tool.erc721MetaData

            cardano_description = bpy.context.scene.input_tool.cardano_description
            solana_description = bpy.context.scene.input_tool.solana_description
            erc721_description = bpy.context.scene.input_tool.erc721_description

            Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        Refactorer.reformatNFTCollection(refactor_panel_input)
        self.report({'INFO'}, "Batches Refactored, MetaData created!")

        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

class export_settings(bpy.types.Operator):
    """Export your settings into a configuration file."""
    bl_idname = 'export.settings'
    bl_label = 'Export Settings'
    bl_description = 'Save your settings to a configuration file'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        save_path = bpy.path.abspath(bpy.context.scene.input_tool.save_path)
        filename = "config.cfg"

        settings = bpy.context.scene.input_tool

        with open(save_path + filename, 'w') as config:
            output = (
                "#This file was auto-generated from the Blend_My_NFTs addon and is used\n"
                "#when running Blend_My_NFTs in a headless environment.\n"
                "\n"
                "#The name of your nft project\n"
                f"nftName={settings.nftName}\n"
                "\n"
                "#NFT Collection Size\n"
                f"collectionSize={settings.collectionSize}\n"
                "\n"
                "#The number of NFTs to generate per batch\n"
                f"nftsPerBatch={str(settings.nftsPerBatch)}\n"
                "\n"
                "#Save path for your NFT files\n"
                f"save_path={settings.save_path}\n"
                "\n"
                "#Enable Rarity\n"
                f"enableRarity={(settings.enableRarity)}\n"
                "\n"
                "#Enable Logic\n"
                f"enableLogic={str(settings.enableLogic)}\n"
                "\n"
                "#NFT Media output type(s):\n"
                f"imageBool={str(settings.imageBool)}\n"
                f"imageEnum={settings.imageEnum}\n"
                f"animationBool={str(settings.animationBool)}\n"
                f"animationEnum={settings.animationEnum}\n"
                f"modelBool={str(settings.modelBool)}\n"
                f"modelEnum={settings.modelEnum}\n"
                "\n"
                "#Batch to generate\n"
                f"batchToGenerate={str(settings.batchToGenerate)}\n"
                "\n"
                "#Metadata Format\n"
                f"cardanoMetaDataBool={str(settings.cardanoMetaDataBool)}\n"
                f"cardano_description={settings.cardano_description}\n"
                f"erc721MetaData={str(settings.erc721MetaData)}\n"
                f"erc721_description={settings.erc721_description}\n"
                f"solanaMetaDataBool={str(settings.solanaMetaDataBool)}\n"
                f"solana_description={settings.solana_description}\n"
                "\n"
                "#Enable Custom Fields\n"
                f"enableCustomFields={str(settings.enableCustomFields)}\n"
                f"customfieldsFile={settings.customfieldsFile}\n"
            )

            print(output, file=config)

        self.report({'INFO'}, f"Saved settings to: {save_path + filename}!")

        return {"FINISHED"}


# ======== UI Panels ======== #
class BMNFTS_PT_CreateData(bpy.types.Panel):
    bl_label = "Create NFT Data"
    bl_idname = "BMNFTS_PT_CreateData"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        input_tool_scene = scene.input_tool

        row = layout.row()
        row.prop(input_tool_scene, "nftName")

        row = layout.row()
        layout.label(text=f"Maximum Number Of NFTs: {combinations}")
        layout.label(text=f"Recommended limit: {recommended_limit}")

        row = layout.row()
        row.prop(input_tool_scene, "collectionSize")

        row = layout.row()
        row.prop(input_tool_scene, "nftsPerBatch")

        row = layout.row()
        row.prop(input_tool_scene, "save_path")

        row = layout.row()
        row.prop(input_tool_scene, "enableRarity")

        row = layout.row()
        row.prop(input_tool_scene, "enableLogic")

        if bpy.context.scene.input_tool.enableLogic:
            row = layout.row()
            row.prop(input_tool_scene, "logicFile")

        row = layout.row()
        self.layout.operator("create.data", icon='DISCLOSURE_TRI_RIGHT', text="Create Data")

class BMNFTS_PT_GenerateNFTs(bpy.types.Panel):
    bl_label = "Generate NFTs"
    bl_idname = "BMNFTS_PT_GenerateNFTs"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        input_tool_scene = scene.input_tool

        row = layout.row()
        layout.label(text="NFT Media files:")

        row = layout.row()
        row.prop(input_tool_scene, "imageBool")
        if bpy.context.scene.input_tool.imageBool:
            row.prop(input_tool_scene, "imageEnum")

        row = layout.row()
        row.prop(input_tool_scene, "animationBool")
        if bpy.context.scene.input_tool.animationBool:
            row.prop(input_tool_scene, "animationEnum")

        row = layout.row()
        row.prop(input_tool_scene, "modelBool")
        if bpy.context.scene.input_tool.modelBool:
            row.prop(input_tool_scene, "modelEnum")

        row = layout.row()
        row.prop(input_tool_scene, "batchToGenerate")

        save_path = bpy.path.abspath(bpy.context.scene.input_tool.save_path)
        Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFTs Output", "NFT_Data")
        batch_json_save_path = os.path.join(Blend_My_NFTs_Output, "Batch_Data")
        nftBatch_save_path = os.path.join(save_path, "Blend_My_NFTs Output", "Generated NFT Batches")

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

class BMNFTS_PT_Refactor(bpy.types.Panel):
    bl_label = "Refactor Batches & Create Metadata"
    bl_idname = "BMNFTS_PT_Refactor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        input_tool_scene = scene.input_tool

        row = layout.row()
        layout.label(text="Meta Data format:")

        row = layout.row()
        row.prop(input_tool_scene, "cardanoMetaDataBool")
        if bpy.context.scene.input_tool.cardanoMetaDataBool:
            row = layout.row()
            row.prop(input_tool_scene, "cardano_description")

            row = layout.row()
            row.operator("wm.url_open", text="Cardano Metadata Documentation",
                         icon='URL').url = "https://cips.cardano.org/cips/cip25/"

        row = layout.row()
        row.prop(input_tool_scene, "solanaMetaDataBool")
        if bpy.context.scene.input_tool.solanaMetaDataBool:
            row = layout.row()
            row.prop(input_tool_scene, "solana_description")

            row = layout.row()
            row.operator("wm.url_open", text="Solana Metadata Documentation",
                         icon='URL').url = "https://docs.metaplex.com/token-metadata/specification"

        row = layout.row()
        row.prop(input_tool_scene, "erc721MetaData")
        if bpy.context.scene.input_tool.erc721MetaData:
            row = layout.row()
            row.prop(input_tool_scene, "erc721_description")

            row = layout.row()
            row.operator("wm.url_open", text="ERC721 Metadata Documentation",
                         icon='URL').url = "https://docs.opensea.io/docs/metadata-standards"

        row = layout.row()
        row.prop(input_tool_scene, "enableCustomFields")
        if bpy.context.scene.input_tool.enableCustomFields:
            row = layout.row()
            row.prop(input_tool_scene, "customfieldsFile")

        row = layout.row()
        self.layout.operator("refactor.batches", icon='FOLDER_REDIRECT', text="Refactor Batches & Create Metadata")

class BMNFTS_PT_Other(bpy.types.Panel):
    bl_label = "Other"
    bl_idname = "BMNFTS_PT_Other"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        input_tool_scene = scene.input_tool

        """
        Export Settings:
        This panel gives the user the option to export all settings from the Blend_My_NFTs addon into a config file. Settings 
        will be read from the config file when running heedlessly.
        """
        layout.label(text=f"Running Blend_My_NFTs Headless:")

        save_path = bpy.path.abspath(bpy.context.scene.input_tool.save_path)

        if save_path and os.path.isdir(save_path):
            row = layout.row()
            self.layout.operator("export.settings", icon='FOLDER_REDIRECT', text="Export BMNFTs Settings to a File")
        else:
            row = layout.row()
            layout.label(text=f"**Set a Save Path in Create NFT Data to Export Settings")

        row = layout.row()
        row.operator("wm.url_open", text="Blend_My_NFTs Documentation",
                     icon='URL').url = "https://github.com/torrinworx/Blend_My_NFTs"

        row = layout.row()
        row.operator("wm.url_open", text="YouTube Tutorials",
                     icon='URL').url = "https://www.youtube.com/watch?v=ygKJYz4BjRs&list=PLuVvzaanutXcYtWmPVKu2bx83EYNxLRsX"


# ======== Blender add-on register/unregister handling ======== #
classes = (
    # Property Group Classes:
    BMNFTS_PGT_Input_Properties,

    # Operator Classes:
    createData,
    exportNFTs,
    resume_failed_batch,
    refactor_Batches,
    export_settings,

    # Panel Classes:
    BMNFTS_PT_CreateData,
    BMNFTS_PT_GenerateNFTs,
    BMNFTS_PT_Refactor,
    BMNFTS_PT_Other,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.input_tool = bpy.props.PointerProperty(type=BMNFTS_PGT_Input_Properties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.input_tool


if __name__ == '__main__':
    register()
    runAsHeadless()
