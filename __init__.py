bl_info = {
    "name": "Blend_My_NFTs",
    "author": "Torrin Leonard, This Cozy Studio Inc",
    "version": (2, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "Blend_My_NFTs UI Edition",
    "category": "Development",
}

# Import handling:

import bpy
from bpy.app.handlers import persistent

import os
import importlib

# Import files from main directory:

importList = ['DNA_Generator', 'Batch_Sorter', 'Exporter', 'Batch_Refactorer', 'get_combinations', 'UIList']

if bpy in locals():
        importlib.reload(DNA_Generator)
        importlib.reload(Batch_Sorter)
        importlib.reload(Exporter)
        importlib.reload(Refactorer)
        importlib.reload(get_combinations)
        importlib.reload(Uploader)
else:
    from .main import \
        DNA_Generator, \
        Batch_Sorter, \
        Exporter, \
        Refactorer, \
        get_combinations, \
        Uploader

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
    openSeaMetaData: bpy.props.BoolProperty(name="OpenSea")

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
    
    openSea_description: bpy.props.StringProperty(name="Description")

    nftport_api_key: bpy.props.StringProperty(name="Nft Port API Key")

    wallet_address: bpy.props.StringProperty(name="Wallet address")

    contract_address: bpy.props.StringProperty(name="Contract address")


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

        DNA_Generator.send_To_Record_JSON(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity, enableLogic, logicFile, Blend_My_NFTs_Output)
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


        Exporter.render_and_save_NFTs(nftName, maxNFTs, batchToGenerate, batch_json_save_path, nftBatch_save_path, enableImages,
                                      imageFileFormat, enableAnimations, animationFileFormat, enableModelsBlender,
                                      modelFileFormat
                                      )

        self.report({'INFO'}, f"All NFTs generated for batch {batchToGenerate}!")

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
            openSeaMetaData = bpy.context.scene.my_tool.openSeaMetaData

            cardano_description = bpy.context.scene.my_tool.cardano_description
            solana_description = bpy.context.scene.my_tool.solana_description
            erc721_description = bpy.context.scene.my_tool.erc721_description
            openSea_description = bpy.context.scene.my_tool.openSea_description

            Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        Refactorer.reformatNFTCollection(refactor_panel_input)
        self.report({'INFO'}, "Batches Refactored, MetaData created!")

        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

class uploadNFTs(bpy.types.Operator):
    bl_idname = 'uploader.nfts'
    bl_label = 'Upload NFTs'
    bl_description = 'Upload NFTs.'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        class uploader_panel_input:
            save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
            nftport_api_key = bpy.context.scene.my_tool.nftport_api_key.strip()
            contract_address = bpy.context.scene.my_tool.contract_address.strip()
            wallet_address = bpy.context.scene.my_tool.wallet_address.strip()

        Uploader.uploadNFTCollection(uploader_panel_input)

        self.report({'INFO'}, "NFTs Uploaded")

        return {"FINISHED"}

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
        row.prop(mytool, "openSeaMetaData")
        if bpy.context.scene.my_tool.openSeaMetaData:
            row = layout.row()
            row.prop(mytool, "openSea_description")

        row = layout.row()
        row.prop(mytool, "enableCustomFields")
        if bpy.context.scene.my_tool.enableCustomFields:
            row = layout.row()
            row.prop(mytool, "customfieldsFile")

        row = layout.row()
        self.layout.operator("refactor.batches", icon='FOLDER_REDIRECT', text="Refactor Batches & create MetaData")

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

class BMNFTS_PT_NFTPORT_Uploader(bpy.types.Panel):
    bl_label = "NFTPort Uploader"
    bl_idname = "BMNFTS_PT_NFTPORT_Uploader"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.prop(mytool, "nftport_api_key")

        row = layout.row()
        row.prop(mytool, "contract_address")

        row = layout.row()
        row.prop(mytool, "wallet_address")

        row = layout.row()
        self.layout.operator("uploader.nfts", icon='DISCLOSURE_TRI_RIGHT', text="Upload To IPFS & Mint")
        row = layout.row()
        row.operator("wm.url_open", text="Documentation",
                     icon='URL').url = "https://github.com/aizwellenstan/Blend_My_NFTs_Doc"

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
# # API Panel:
# class BMNFTS_PT_API_Panel(bpy.types.Panel):
#     bl_label = "API"
#     bl_idname = "BMNFTS_PT_API_Panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Blend_My_NFTs'
#
#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool
#
#         row = layout.row()
#         row.prop(mytool, "apiKey")

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
    BMNFTS_PT_NFTPORT_Uploader,

    # Other panels:
    # BMNFTS_PT_MATERIALS_Panel,
    # BMNFTS_PT_API_Panel,

    createData,
    exportNFTs,
    refactor_Batches,
    uploadNFTs
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=BMNFTS_PGT_MyProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.my_tool


if __name__ == '__main__':
    register()
