bl_info = {
    "name": "Blend_My_NFTs",
    "author": "Torrin Leonard, This Cozy Studio Inc",
    "version": (1, 0, 0),
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
        importlib.reload(Batch_Refactorer)
        importlib.reload(get_combinations)
        importlib.reload(UIList)
else:
    from .main import \
        DNA_Generator, \
        Batch_Sorter, \
        Exporter, \
        Batch_Refactorer, \
        get_combinations

    from .ui_Lists import UIList


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
offset: int = 0

@persistent
def update_combinations(dummy1, dummy2):
    global combinations
    global offset

    combinations = (get_combinations.get_combinations_from_scene()) - offset

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
        enableRarity = bpy.context.scene.my_tool.enableRarity

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        DNA_Generator.send_To_Record_JSON(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity, Blend_My_NFTs_Output)
        Batch_Sorter.makeBatches(nftName, maxNFTs, nftsPerBatch, save_path, batch_json_save_path)
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
        return {"FINISHED"}

class refactor_Batches(bpy.types.Operator):
    """Refactor your Batches? This action cannot be undone."""
    bl_idname = 'refactor.batches'
    bl_label = 'Refactor your Batches?'
    bl_description = 'This action cannot be undone.'
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, "Batches Refactored, MetaData created!")

        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)

        cardanoMetaDataBool = bpy.context.scene.my_tool.cardanoMetaDataBool
        solanaMetaDataBool = bpy.context.scene.my_tool.solanaMetaDataBool
        erc721MetaData = bpy.context.scene.my_tool.erc721MetaData

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        Batch_Refactorer.reformatNFTCollection(save_path, Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path,
                                               cardanoMetaDataBool, solanaMetaDataBool, erc721MetaData)
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

        layout.label(text=f"Maximum Number Of NFTs: {combinations}")

        row = layout.row()
        layout.label(text="")

        row = layout.row()
        row.prop(mytool, "nftName")

        row = layout.row()
        row.prop(mytool, "collectionSize")

        row = layout.row()
        row.prop(mytool, "nftsPerBatch")

        row = layout.row()
        row.prop(mytool, "save_path")

        row = layout.row()
        row.prop(mytool, "enableRarity")

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
        row.prop(mytool, "imageBool")
        if  bpy.context.scene.my_tool.imageBool == True:
            row.prop(mytool, "imageEnum")

        row = layout.row()
        row.prop(mytool, "animationBool")
        if  bpy.context.scene.my_tool.animationBool == True:
            row.prop(mytool, "animationEnum")

        row = layout.row()
        row.prop(mytool, "modelBool")
        if  bpy.context.scene.my_tool.modelBool == True:
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
        row.prop(mytool, "solanaMetaDataBool")
        row.prop(mytool, "erc721MetaData")
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

# # Logic Panel:
# class BMNFTS_PT_LOGIC_Panel(bpy.types.Panel):
#     bl_label = "Logic"
#     bl_idname = "BMNFTS_PT_LOGIC_Panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Blend_My_NFTs'
#
#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool
#
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

    # Other panels:

    # BMNFTS_PT_LOGIC_Panel,
    # BMNFTS_PT_MATERIALS_Panel,
    # BMNFTS_PT_API_Panel,

    createData,
    exportNFTs,
    refactor_Batches,

    # UIList 1:

    # UIList.CUSTOM_OT_actions,
    # UIList.CUSTOM_OT_addViewportSelection,
    # UIList.CUSTOM_OT_printItems,
    # UIList.CUSTOM_OT_clearList,
    # UIList.CUSTOM_OT_removeDuplicates,
    # UIList.CUSTOM_OT_selectItems,
    # UIList.CUSTOM_OT_deleteObject,
    # UIList.CUSTOM_UL_items,
    # UIList.CUSTOM_PT_objectList,
    # UIList.CUSTOM_PG_objectCollection,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=BMNFTS_PGT_MyProperties)

    # UIList1:

    # bpy.types.Scene.custom = bpy.props.CollectionProperty(type=UIList.CUSTOM_PG_objectCollection)
    # bpy.types.Scene.custom_index = bpy.props.IntProperty()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.my_tool

    # UIList 1:

    # del bpy.types.Scene.custom
    # del bpy.types.Scene.custom_index

if __name__ == '__main__':
    register()
