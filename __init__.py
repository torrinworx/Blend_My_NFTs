bl_info = {
    "name": "Blend_My_NFTs",
    "author": "Torrin Leonard, This Cozy Studio Inc.",
    "version": (4, 5, 1),
    "blender": (3, 2, 2),
    "location": "View3D",
    "description": "A free and opensource Blender add-on that enables you to create thousands of unique images, "
                   "animations, and 3D models.",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/torrinworx/Blend_My_NFTs",
    "tracker_url": "https://github.com/torrinworx/Blend_My_NFTs/issues/new",
    "category": "Development",
}

BMNFTS_VERSION = "v4.5.1"
LAST_UPDATED = "01:02PM, Aug 24th, 2022"

# ======== Import handling ======== #

import bpy
from bpy.app.handlers import persistent
from bpy.props import (IntProperty,
                       BoolProperty,
                       CollectionProperty)
# Python modules:
import os
import sys
import json
import importlib
import traceback
from typing import Any
from dataclasses import dataclass
from datetime import datetime, timezone

# "a little hacky bs" - matt159 ;)
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Local file imports:
from main import \
    helpers, \
    dna_generator, \
    exporter, \
    headless_util, \
    intermediate, \
    logic, \
    material_generator, \
    metadata_templates, \
    refactorer

from UILists import \
    custom_metadata_ui_list, \
    logic_ui_list

if "bpy" in locals():
    modules = {
        "helpers": helpers,
        "dna_generator": dna_generator,
        "exporter": exporter,
        "headless_util": headless_util,
        "intermediate": intermediate,
        "logic": logic,
        "material_generator": material_generator,
        "metadata_templates": metadata_templates,
        "refactorer": refactorer,
        "custom_metadata_ui_list": custom_metadata_ui_list,
        "logic_ui_list": logic_ui_list,
    }

    for i in modules:
        if i in locals():
            importlib.reload(modules[i])

# ======== Persistent UI Refresh ======== #
# Used for updating text and buttons in UI panels

combinations: int = 0
recommended_limit: int = 0
dt = datetime.now(timezone.utc).astimezone()  # Date Time in UTC local


@persistent
def Refresh_UI(dummy1, dummy2):
    """
    Refreshes the UI upon user interacting with Blender (using depsgraph_update_post handler). Might be a better handler
    to use.
    """
    global combinations
    global recommended_limit

    combinations = (helpers.get_combinations())
    recommended_limit = int(round(combinations / 2))

    # Add panel classes that require refresh to this refresh_panels tuple:
    refresh_panel_classes = (
        BMNFTS_PT_CreateData,
    )

    def redraw_panel(panels):
        for i in panels:
            try:
                bpy.utils.unregister_class(i)
            except Exception:
                print(traceback.format_exc())
            bpy.utils.register_class(i)

    redraw_panel(refresh_panel_classes)


bpy.app.handlers.depsgraph_update_post.append(Refresh_UI)


# ======== Defining BMNFTs Data ======== #
@dataclass
class BMNFTData:
    nft_name: str
    save_path: str
    nfts_per_batch: int
    batch_to_generate: int
    collection_size: int

    blend_my_nfts_output: str
    batch_json_save_path: str
    nft_batch_save_path: str

    enable_images: bool
    image_file_format: str

    enable_animations: bool
    animation_file_format: str

    enable_models: bool
    model_file_format: str

    enable_custom_fields: bool

    cardano_metadata_bool: bool
    solana_metadata_bool: bool
    erc721_metadata: bool

    cardano_description: str
    solana_description: str
    erc721_description: str

    enable_materials: bool
    materials_file: str

    enable_logic: bool
    enable_logic_json: bool
    logic_file: str

    enable_rarity: bool

    enable_auto_shutdown: bool

    specify_time_bool: bool
    hours: int
    minutes: int

    email_notification_bool: bool
    sender_from: str
    email_password: str
    receiver_to: str

    enable_debug: bool
    log_path: str

    custom_fields: dict = None
    fail_state: Any = False
    failed_batch: Any = None
    failed_dna: Any = None
    failed_dna_index: Any = None

    def __post_init__(self):
        self.custom_fields = {}


def getBMNFTData():
    _save_path = bpy.path.abspath(bpy.context.scene.input_tool.save_path)
    _Blend_My_NFTs_Output, _batch_json_save_path, _nftBatch_save_path = make_directories(_save_path)

    data = BMNFTData(
        nft_name=bpy.context.scene.input_tool.nft_name,
        save_path=_save_path,
        nfts_per_batch=bpy.context.scene.input_tool.nfts_per_batch,
        batch_to_generate=bpy.context.scene.input_tool.batch_to_generate,
        collection_size=bpy.context.scene.input_tool.collection_size,

        enable_rarity=bpy.context.scene.input_tool.enable_rarity,

        blend_my_nfts_output=_Blend_My_NFTs_Output,
        batch_json_save_path=_batch_json_save_path,
        nft_batch_save_path=_nftBatch_save_path,

        enable_logic=bpy.context.scene.input_tool.enable_logic,
        enable_logic_json=bpy.context.scene.input_tool.enable_logic_json,
        logic_file=bpy.context.scene.input_tool.logic_file,

        enable_images=bpy.context.scene.input_tool.image_bool,
        image_file_format=bpy.context.scene.input_tool.image_enum,

        enable_animations=bpy.context.scene.input_tool.animation_bool,
        animation_file_format=bpy.context.scene.input_tool.animation_enum,

        enable_models=bpy.context.scene.input_tool.model_bool,
        model_file_format=bpy.context.scene.input_tool.model_enum,

        enable_custom_fields=bpy.context.scene.input_tool.enable_custom_fields,

        cardano_metadata_bool=bpy.context.scene.input_tool.cardano_metadata_bool,
        solana_metadata_bool=bpy.context.scene.input_tool.solana_metadata_bool,
        erc721_metadata=bpy.context.scene.input_tool.erc721_metadata,

        cardano_description=bpy.context.scene.input_tool.cardano_description,
        solana_description=bpy.context.scene.input_tool.solana_description,
        erc721_description=bpy.context.scene.input_tool.erc721_description,

        enable_materials=bpy.context.scene.input_tool.enable_materials,
        materials_file=bpy.path.abspath(bpy.context.scene.input_tool.materials_file),

        enable_auto_shutdown=bpy.context.scene.input_tool.enable_auto_shutdown,

        specify_time_bool=bpy.context.scene.input_tool.specify_time_bool,
        hours=bpy.context.scene.input_tool.hours,
        minutes=bpy.context.scene.input_tool.minutes,

        email_notification_bool=bpy.context.scene.input_tool.email_notification_bool,
        sender_from=bpy.context.scene.input_tool.sender_from,
        email_password=bpy.context.scene.input_tool.email_password,
        receiver_to=bpy.context.scene.input_tool.receiver_to,

        enable_debug=bpy.context.scene.input_tool.enable_debug,
        log_path=bpy.context.scene.input_tool.log_path,
    )

    return data


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

    # force CUDA device usage with cycles renderer
    cprefs = bpy.context.preferences.addons['cycles'].preferences
    cprefs.compute_device_type = 'CUDA'
    cprefs.get_devices()
    print(cprefs.devices.keys())

    for key in cprefs.devices.keys():
        cprefs.devices[key].use = True

    print('Using {} devices for rendering!'.format(cprefs.get_num_gpu_devices()))

    # def dumpSettings(settings):
    #     output = (
    #         f"nft_name={settings.nft_name}\n"
    #         f"collection_size={str(settings.collection_size)}\n"
    #         f"nfts_per_batch={str(settings.nfts_per_batch)}\n"
    #         f"save_path={settings.save_path}\n"
    #         f"enable_rarity={(settings.enable_rarity)}\n"
    #         f"enable_logic={str(settings.enable_logic)}\n"
    #         f"image_bool={str(settings.image_bool)}\n"
    #         f"image_enum={settings.image_enum}\n"
    #         f"animation_bool={str(settings.animation_bool)}\n"
    #         f"animation_enum={settings.animation_enum}\n"
    #         f"model_bool={str(settings.model_bool)}\n"
    #         f"model_enum={settings.model_enum}\n"
    #         f"batch_to_generate={str(settings.batch_to_generate)}\n"
    #         f"cardano_metadata_bool={str(settings.cardano_metadata_bool)}\n"
    #         f"cardano_description={settings.cardano_description}\n"
    #         f"erc721_metadata={str(settings.erc721_metadata)}\n"
    #         f"erc721_description={settings.erc721_description}\n"
    #         f"solana_metadata_bool={str(settings.solana_metadata_bool)}\n"
    #         f"solana_description={settings.solana_description}\n"
    #         f"enable_custom_fields={str(settings.enable_custom_fields)}\n"
    #         f"custom_fields_file={settings.custom_fields_file}\n"
    #         f"enable_materials={str(settings.custom_fields_file)}\n"
    #         f"materials_file={settings.materials_file}\n"
    #     )
    #     print(output)

    args, parser = headless_util.get_python_args()

    settings = bpy.context.scene.input_tool

    # dumpSettings(settings)

    with open(args.config_path, 'r') as f:
        configs = [line.strip() for line in f.readlines() if not (line[0] == '#' or len(line.strip()) < 1)]

        pairs = [config.strip().split('=') for config in configs]

        # print(pairs)

        settings.nft_name = pairs[0][1]
        settings.collection_size = int(pairs[1][1])
        settings.nfts_per_batch = int(pairs[2][1])
        settings.save_path = pairs[3][1]
        settings.enable_rarity = pairs[4][1]=='True'
        settings.enable_logic = pairs[5][1]=='True'
        settings.enableLogicJson = pairs[6][1] == 'True'
        settings.logic_file = pairs[7][1]
        settings.image_bool = pairs[8][1]=='True'
        settings.image_enum = pairs[9][1]
        settings.animation_bool = pairs[10][1]=='True'
        settings.animation_enum = pairs[11][1]
        settings.model_bool = pairs[12][1]=='True'
        settings.model_enum = pairs[13][1]
        settings.batch_to_generate = int(pairs[14][1])
        settings.cardano_metadata_bool = pairs[15][1]=='True'
        settings.cardano_description = pairs[16][1]
        settings.erc721_metadata = pairs[17][1]=='True'
        settings.erc721_description = pairs[18][1]
        settings.solana_metadata_bool = pairs[19][1]=='True'
        settings.solanaDescription = pairs[20][1]
        settings.enable_custom_fields = pairs[21][1]=='True'
        settings.custom_fields_file = pairs[22][1]
        settings.enable_materials = pairs[23][1]=='True'
        settings.materials_file = pairs[24][1]

    if args.save_path:
        settings.save_path = args.save_path

    if args.batch_number:
        settings.batch_to_generate = args.batch_number

    input = getBMNFTData()

    if args.batch_data_path:
        input.batch_json_save_path = args.batch_data_path

    if args.operation == 'create-dna':
        intermediate.send_to_record(input)

    elif args.operation == 'generate-nfts':
        intermediate.render_and_save_nfts(input)

    elif args.operation == 'refactor-batches':
        refactorer.reformat_nft_collection(input)


# ======== User input Property Group ======== #
class BMNFTS_PGT_Input_Properties(bpy.types.PropertyGroup):
    # Create NFT Data Panel:

    nft_name: bpy.props.StringProperty(name="NFT Name")

    collection_size: bpy.props.IntProperty(
            name="NFT Collection Size",
            default=1,
            min=1
    )  # max=(combinations - offset)
    nfts_per_batch: bpy.props.IntProperty(
            name="NFTs Per Batch",
            default=1,
            min=1
    )  # max=(combinations - offset)

    save_path: bpy.props.StringProperty(
        name="Save Path",
        description="Save path for NFT files",
        default="",
        maxlen=1024,
        subtype="DIR_PATH"
    )

    enable_rarity: bpy.props.BoolProperty(
            name="Enable Rarity"
    )

    enable_logic: bpy.props.BoolProperty(
            name="Enable Logic"
    )
    enable_logic_json: bpy.props.BoolProperty(
            name="Use Logic.json instead"
    )
    logic_file: bpy.props.StringProperty(
        name="Logic File Path",
        description="Path where Logic.json is located.",
        default="",
        maxlen=1024,
        subtype="FILE_PATH"
    )

    enable_materials: bpy.props.BoolProperty(
            name="Enable Materials"
    )
    materials_file: bpy.props.StringProperty(
        name="Materials File",
        description="Path where Materials.json is located.",
        default="",
        maxlen=1024,
        subtype="FILE_PATH"
    )

    # Generate NFTs Panel:
    image_bool: bpy.props.BoolProperty(
            name="Image"
    )
    image_enum: bpy.props.EnumProperty(
        name="Image File Format",
        description="Select Image file format",
        items=[
            ('PNG', ".PNG", "Export NFT as PNG"),
            ('JPEG', ".JPEG", "Export NFT as JPEG")
        ]
    )

    animation_bool: bpy.props.BoolProperty(
            name="Animation"
    )
    animation_enum: bpy.props.EnumProperty(
        name="Animation File Format",
        description="Select Animation file format",
        items=[
            ('AVI_JPEG', '.avi (AVI_JPEG)', 'Export NFT as AVI_JPEG'),
            ('AVI_RAW', '.avi (AVI_RAW)', 'Export NFT as AVI_RAW'),
            ('FFMPEG', '.mkv (FFMPEG)', 'Export NFT as FFMPEG'),
            ('MP4', '.mp4', 'Export NFT as .mp4'),
            ('PNG', '.png', 'Export NFT as PNG'),
            ('TIFF', '.tiff', 'Export NFT as TIFF')
        ]
    )

    model_bool: bpy.props.BoolProperty(
            name="3D Model"
    )
    model_enum: bpy.props.EnumProperty(
        name="3D Model File Format",
        description="Select 3D Model file format",
        items=[
            ('GLB', '.glb', 'Export NFT as .glb'),
            ('GLTF_SEPARATE', '.gltf + .bin + textures',
             'Export NFT as .gltf with separated textures in .bin + textures.'),
            ('GLTF_EMBEDDED', '.gltf', 'Export NFT as embedded .gltf file that contains textures.'),
            ('FBX', '.fbx', 'Export NFT as .fbx'),
            ('OBJ', '.obj', 'Export NFT as .obj'),
            ('X3D', '.x3d', 'Export NFT as .x3d'),
            ('STL', '.stl', 'Export NFT as .stl'),
            ('VOX', '.vox (Experimental)',
             'Export NFT as .vox, requires the voxwriter add on: https://github.com/Spyduck/voxwriter')
        ]
    )

    batch_to_generate: bpy.props.IntProperty(
            name="Batch To Generate",
            default=1,
            min=1
    )

    # Refactor Batches & Create Metadata Panel:
    cardano_metadata_bool: bpy.props.BoolProperty(
            name="Cardano Cip"
    )
    cardano_description: bpy.props.StringProperty(
            name="Cardano description"
    )

    solana_metadata_bool: bpy.props.BoolProperty(
            name="Solana Metaplex"
    )
    solana_description: bpy.props.StringProperty(
            name="Solana description"
    )

    erc721_metadata: bpy.props.BoolProperty(
            name="ERC721"
    )
    erc721_description: bpy.props.StringProperty(
            name="ERC721 description"
    )

    enable_custom_fields: bpy.props.BoolProperty(
            name="Enable Custom Metadata Fields"
    )
    custom_fields_file: bpy.props.StringProperty(
        name="Custom Fields File",
        description="Path where Custom_Fields.json is located.",
        default="",
        maxlen=1024,
        subtype="FILE_PATH"
    )

    # TODO: Add 'Other' panel inputs to Headless functionality.

    # Other Panel:
    enable_auto_save: bpy.props.BoolProperty(
            name="Auto Save Before Generation",
            description="Automatically saves your Blender file when 'Generate NFTs & Create Metadata' button is clicked"
    )

    enable_auto_shutdown: bpy.props.BoolProperty(
            name="Auto Shutdown",
            description="Automatically shuts down your computer after a Batch is finished Generating"
    )

    specify_time_bool: bpy.props.BoolProperty(
            name="Shutdown in a Given Amount of Time",
            description="Wait a given amount of time after a Batch is generated before Automatic Shutdown"
    )
    hours: bpy.props.IntProperty(
            default=0, min=0
    )
    minutes: bpy.props.IntProperty(
            default=0, min=0
    )

    email_notification_bool: bpy.props.BoolProperty(
            name="Email Notifications",
            description="Receive Email Notifications from Blender once a batch is finished generating"
    )
    sender_from: bpy.props.StringProperty(
            name="From",
            default="from@example.com"
    )
    email_password: bpy.props.StringProperty(
            name="Password",
            subtype='PASSWORD'
    )
    receiver_to: bpy.props.StringProperty(
            name="To",
            default="to@example.com"
    )

    enable_debug: bpy.props.BoolProperty(
            name="Enable Debug Mode",
            description="Allows you to run Blend_My_NFTs without generating any content files and includes more "
                        "console information."
    )
    log_path: bpy.props.StringProperty(
        name="Debug Log Path",
        description="Path where BMNFT_Log.txt is located.",
        default="",
        maxlen=1024,
        subtype="FILE_PATH"
    )

    # API Panel properties:
    api_key: bpy.props.StringProperty(
            name="API Key",
            subtype='PASSWORD'
    )  # Test code for future features


# ======== Main Operators ======== #
class Createdata(bpy.types.Operator):
    bl_idname = 'create.data'
    bl_label = 'Create Data'
    bl_description = 'Creates NFT Data. Run after any changes were made to scene. All previous data will be ' \
                     'overwritten and cannot be recovered.'
    bl_options = {"REGISTER", "UNDO"}

    reverse_order: BoolProperty(
        default=False,
        name="Reverse Order")

    def execute(self, context):
        # Handling Custom Fields UIList input:
        input = getBMNFTData()

        if input.enable_logic:
            if input.enable_logic_json and not input.logic_file:
                self.report({'ERROR'},
                            f"No Logic.json file path set. Please set the file path to your Logic.json file.")

        intermediate.send_to_record(input)

        self.report({'INFO'}, f"NFT Data created!")
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class ExportNFTs(bpy.types.Operator):
    bl_idname = 'exporter.nfts'
    bl_label = 'Export NFTs'
    bl_description = 'Generate and export a given batch of NFTs.'
    bl_options = {"REGISTER", "UNDO"}

    reverse_order: BoolProperty(
        default=False,
        name="Reverse Order")

    def execute(self, context):
        input = getBMNFTData()
        # Handling Custom Fields UIList input:

        intermediate.render_and_save_nfts(input)

        self.report({'INFO'}, f"All NFTs generated for batch {input.batch_to_generate}!")

        return {"FINISHED"}


class ResumeFailedBatch(bpy.types.Operator):
    bl_idname = 'exporter.resume_nfts'
    bl_label = 'Resume Failed Batch'
    bl_description = 'Failed Batch detected. Generate NFTs where the previous batch failed?'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        _save_path = bpy.path.abspath(bpy.context.scene.input_tool.save_path)
        _Blend_My_NFTs_Output, _batch_json_save_path, _nftBatch_save_path = make_directories(_save_path)

        _batchToGenerate = bpy.context.scene.input_tool.batch_to_generate

        file_name = os.path.join(_batch_json_save_path, "Batch{}.json".format(_batchToGenerate))
        batchData = json.load(open(file_name))

        _fail_state, _failed_batch, _failed_dna, _failed_dna_index = helpers.check_failed_batches(_batch_json_save_path)

        render_settings = batchData["Generation Save"][-1]["Render_Settings"]

        input = BMNFTData(
            nft_name=render_settings["nft_name"],
            save_path=_save_path,
            nfts_per_batch=render_settings["nfts_per_batch"],
            batch_to_generate=render_settings["batch_to_generate"],
            collection_size=render_settings["collection_size"],

            blend_my_nfts_output=_Blend_My_NFTs_Output,
            batch_json_save_path=_batch_json_save_path,
            nft_batch_save_path=render_settings["nft_batch_save_path"],

            enable_images=render_settings["enable_images"],
            image_file_format=render_settings["image_file_format"],

            enable_animations=render_settings["enable_animations"],
            animation_file_format=render_settings["animation_file_format"],

            enable_models=render_settings["enable_models"],
            model_file_format=render_settings["model_file_format"],

            enable_custom_fields=render_settings["enable_custom_fields"],

            cardano_metadata_bool=render_settings["cardano_metadata_bool"],
            solana_metadata_bool=render_settings["solana_metadata_bool"],
            erc721_metadata=render_settings["erc721_metadata"],

            cardano_description=render_settings["cardano_description"],
            solana_description=render_settings["solana_description"],
            erc721_description=render_settings["erc721_description"],

            enable_materials=render_settings["enable_materials"],
            materials_file=render_settings["materials_file"],

            enable_logic=render_settings["enable_logic"],
            enable_logic_json=render_settings["enable_logic_json"],
            logic_file=render_settings["logic_file"],

            enable_rarity=render_settings["enable_rarity"],

            enable_auto_shutdown=render_settings["enable_auto_shutdown"],

            specify_time_bool=render_settings["specify_time_bool"],
            hours=render_settings["hours"],
            minutes=render_settings["minutes"],

            email_notification_bool=render_settings["email_notification_bool"],
            sender_from=render_settings["sender_from"],
            email_password=render_settings["email_password"],
            receiver_to=render_settings["receiver_to"],

            enable_debug=render_settings["enable_debug"],
            log_path=render_settings["log_path"],

            fail_state=_fail_state,
            failed_batch=_failed_batch,
            failed_dna=_failed_dna,
            failed_dna_index=_failed_dna_index,

            custom_fields=render_settings["custom_fields"],
        )

        exporter.render_and_save_nfts(input)

        self.report({'INFO'}, f"Resuming Failed Batch Generation!")

        return {"FINISHED"}


class RefactorBatches(bpy.types.Operator):
    """Refactor your collection? This action cannot be undone."""
    bl_idname = 'refactor.batches'
    bl_label = 'Refactor your Batches?'
    bl_description = 'This action cannot be undone.'
    bl_options = {'REGISTER', 'INTERNAL'}

    reverse_order: BoolProperty(
        default=False,
        name="Reverse Order")

    def execute(self, context):
        # Passing info to main functions for refactoring:
        refactorer.reformat_nft_collection(getBMNFTData())
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class ExportSettings(bpy.types.Operator):
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
                f"nft_name={settings.nft_name}\n"
                "\n"
                "#NFT Collection Size\n"
                f"collection_size={settings.collection_size}\n"
                "\n"
                "#The number of NFTs to generate per batch\n"
                f"nfts_per_batch={str(settings.nfts_per_batch)}\n"
                "\n"
                "#Save path for your NFT files\n"
                f"save_path={settings.save_path}\n"
                "\n"
                "#Enable Rarity\n"
                f"enable_rarity={settings.enable_rarity}\n"
                "\n"
                "#Enable Logic\n"
                f"enable_logic={str(settings.enable_logic)}\n"
                f"enableLogicJson={str(settings.enable_logic_json)}\n"
                f"logicFilePath={settings.logic_file}\n"
                "\n"
                "#NFT Media output type(s):\n"
                f"image_bool={str(settings.image_bool)}\n"
                f"image_enum={settings.image_enum}\n"
                f"animation_bool={str(settings.animation_bool)}\n"
                f"animation_enum={settings.animation_enum}\n"
                f"model_bool={str(settings.model_bool)}\n"
                f"model_enum={settings.model_enum}\n"
                "\n"
                "#Batch to generate\n"
                f"batch_to_generate={str(settings.batch_to_generate)}\n"
                "\n"
                "#Metadata Format\n"
                f"cardano_metadata_bool={str(settings.cardano_metadata_bool)}\n"
                f"cardano_description={settings.cardano_description}\n"
                f"erc721_metadata={str(settings.erc721_metadata)}\n"
                f"erc721_description={settings.erc721_description}\n"
                f"solana_metadata_bool={str(settings.solana_metadata_bool)}\n"
                f"solana_description={settings.solana_description}\n"
                "\n"
                "#Enable Custom Fields\n"
                f"enable_custom_fields={str(settings.enable_custom_fields)}\n"
                f"custom_fields_file={settings.custom_fields_file}\n"
                "\n"
                "#Enable Materials\n"
                f"enable_materials={str(settings.enable_materials)}\n"
                f"materials_file={settings.materials_file}\n"
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
        row.prop(input_tool_scene, "nft_name")

        row = layout.row()
        layout.label(text=f"Maximum Number Of NFTs: {combinations}")
        layout.label(text=f"Recommended limit: {recommended_limit}")

        row = layout.row()
        row.prop(input_tool_scene, "collection_size")

        row = layout.row()
        row.prop(input_tool_scene, "nfts_per_batch")

        row = layout.row()
        row.prop(input_tool_scene, "save_path")

        row = layout.row()
        row.prop(input_tool_scene, "enable_rarity")

        row = layout.row()
        row.prop(input_tool_scene, "enable_logic")

        # Logic_UIList implementation:
        if bpy.context.scene.input_tool.enable_logic:
            layout = self.layout
            scn = bpy.context.scene

            rows = 2
            row = layout.row()
            row.template_list("CUSTOM_UL_logic_items", "", scn, "logic_fields", scn,
                              "logic_fields_index", rows=rows)

            col = row.column(align=True)
            col.operator("logic_uilist.logic_list_action", icon='ZOOM_IN', text="").action = 'ADD'
            col.operator("logic_uilist.logic_list_action", icon='ZOOM_OUT', text="").action = 'REMOVE'
            col.separator()
            col.operator("logic_uilist.logic_list_action", icon='TRIA_UP', text="").action = 'UP'
            col.operator("logic_uilist.logic_list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

            row = layout.row()
            col = row.column(align=True)
            row = col.row(align=True)
            row.operator("logic_uilist.logic_clear_list", icon="X")
            row = col.row(align=True)
            row.label(text=f"*Field Names must be unique.")

            row = layout.row()
            row.prop(input_tool_scene, "enable_logic_json")

            if bpy.context.scene.input_tool.enable_logic_json:
                row = layout.row()
                row.prop(input_tool_scene, "logic_file")

        row = layout.row()
        row.prop(input_tool_scene, "enable_materials")

        if bpy.context.scene.input_tool.enable_materials:
            row = layout.row()
            row.prop(input_tool_scene, "materials_file")

        row = layout.row()
        self.layout.operator("create.data", icon='DISCLOSURE_TRI_RIGHT', text="Create Data")
        row = layout.row()
        layout.label(text=f"{BMNFTS_VERSION}")


class BMNFTS_PT_GenerateNFTs(bpy.types.Panel):
    bl_label = "Generate NFTs & Create Metadata"
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
        row.prop(input_tool_scene, "image_bool")
        if bpy.context.scene.input_tool.image_bool:
            row.prop(input_tool_scene, "image_enum")

        row = layout.row()
        row.prop(input_tool_scene, "animation_bool")
        if bpy.context.scene.input_tool.animation_bool:
            row.prop(input_tool_scene, "animation_enum")

        row = layout.row()
        row.prop(input_tool_scene, "model_bool")
        if bpy.context.scene.input_tool.model_bool:
            row.prop(input_tool_scene, "model_enum")

        row = layout.row()
        layout.label(text="Meta Data format:")

        row = layout.row()
        row.prop(input_tool_scene, "cardano_metadata_bool")
        if bpy.context.scene.input_tool.cardano_metadata_bool:
            row = layout.row()
            row.prop(input_tool_scene, "cardano_description")

            row = layout.row()
            row.operator("wm.url_open", text="Cardano Metadata Documentation",
                         icon='URL').url = "https://cips.cardano.org/cips/cip25/"

        row = layout.row()
        row.prop(input_tool_scene, "solana_metadata_bool")
        if bpy.context.scene.input_tool.solana_metadata_bool:
            row = layout.row()
            row.prop(input_tool_scene, "solana_description")

            row = layout.row()
            row.operator("wm.url_open", text="Solana Metadata Documentation",
                         icon='URL').url = "https://docs.metaplex.com/token-metadata/specification"

        row = layout.row()
        row.prop(input_tool_scene, "erc721_metadata")
        if bpy.context.scene.input_tool.erc721_metadata:
            row = layout.row()
            row.prop(input_tool_scene, "erc721_description")

            row = layout.row()
            row.operator("wm.url_open", text="ERC721 Metadata Documentation",
                         icon='URL').url = "https://docs.opensea.io/docs/metadata-standards"

        row = layout.row()
        row.prop(input_tool_scene, "enable_custom_fields")

        # Custom Metadata Fields UIList:
        if bpy.context.scene.input_tool.enable_custom_fields:
            layout = self.layout
            scn = bpy.context.scene

            rows = 2
            row = layout.row()
            row.template_list("CUSTOM_UL_custom_metadata_fields_items", "", scn, "custom_metadata_fields", scn,
                              "custom_metadata_fields_index", rows=rows)

            col = row.column(align=True)
            col.operator("custom_metadata_fields_uilist.list_action", icon='ZOOM_IN', text="").action = 'ADD'
            col.operator("custom_metadata_fields_uilist.list_action", icon='ZOOM_OUT', text="").action = 'REMOVE'
            col.separator()
            col.operator("custom_metadata_fields_uilist.list_action", icon='TRIA_UP', text="").action = 'UP'
            col.operator("custom_metadata_fields_uilist.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

            row = layout.row()
            col = row.column(align=True)
            row = col.row(align=True)
            row.label(text=f"*Field Names must be unique.")
            row = col.row(align=True)
            row.operator("custom_metadata_fields_uilist.clear_list", icon="X")

        row = layout.row()
        row.prop(input_tool_scene, "batch_to_generate")

        save_path = bpy.path.abspath(bpy.context.scene.input_tool.save_path)
        Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFTs Output", "NFT_Data")
        batch_json_save_path = os.path.join(Blend_My_NFTs_Output, "Batch_Data")
        nftBatch_save_path = os.path.join(save_path, "Blend_My_NFTs Output", "Generated NFT Batches")

        fail_state, failed_batch, failed_dna, failed_dna_index = helpers.check_failed_batches(batch_json_save_path)

        if fail_state:
            row = layout.row()
            self.layout.operator("exporter.nfts", icon='RENDER_RESULT', text="Generate NFTs & Create Metadata")

            row = layout.row()
            row.alert = True
            row.operator("exporter.resume_nfts", icon='ERROR', text="Resume Failed Batch")

        if not fail_state:
            row = layout.row()
            self.layout.operator("exporter.nfts", icon='RENDER_RESULT', text="Generate NFTs & Create Metadata")


class BMNFTS_PT_Refactor(bpy.types.Panel):
    bl_label = "Refactor Batches"
    bl_idname = "BMNFTS_PT_Refactor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        input_tool_scene = scene.input_tool

        row = layout.row()
        layout.label(text="Ensure all batches have been created before refactoring.")
        layout.label(text="Refactoring combines all batches into one easy to manage folder.")

        row = layout.row()
        self.layout.operator("refactor.batches", icon='FOLDER_REDIRECT', text="Refactor Batches")


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
        Other:
        A place to store miscellaneous settings, features, and external links that the user may find useful but doesn't 
        want to get in the way of their work flow.
        
        Export Settings:
        This panel gives the user the option to export all settings from the Blend_My_NFTs addon into a config file. Settings 
        will be read from the config file when running heedlessly.
        """

        row = layout.row()
        row.prop(input_tool_scene, "enable_auto_save")

        # Auto Shutdown:
        row = layout.row()
        row.prop(input_tool_scene, "enable_auto_shutdown")
        row.label(text="*Must Run Blender as Admin")

        if bpy.context.scene.input_tool.enable_auto_shutdown:
            row = layout.row()
            row.prop(input_tool_scene, "specify_time_bool")

            time_row1 = layout.row()
            time_row1.label(text=f"Hours")
            time_row1.prop(input_tool_scene, "hours", text="")

            time_row2 = layout.row()
            time_row2.label(text=f"Minutes")
            time_row2.prop(input_tool_scene, "minutes", text="")

            if not bpy.context.scene.input_tool.specify_time_bool:
                time_row1.enabled = False
                time_row2.enabled = False
            else:
                time_row1.enabled = True
                time_row2.enabled = True
            layout.separator()

        row = layout.row()
        row.prop(input_tool_scene, "email_notification_bool")
        row.label(text="*Windows 10+ only")

        if bpy.context.scene.input_tool.email_notification_bool:
            row = layout.row()
            row.prop(input_tool_scene, "sender_from")
            row = layout.row()
            row.prop(input_tool_scene, "email_password")

            layout.separator()
            row = layout.row()
            row.prop(input_tool_scene, "receiver_to")

        layout.separator()

        layout.label(text=f"Running Blend_My_NFTs Headless:")

        save_path = bpy.path.abspath(bpy.context.scene.input_tool.save_path)

        if save_path and os.path.isdir(save_path):
            row = layout.row()
            self.layout.operator("export.settings", icon='FOLDER_REDIRECT', text="Export BMNFTs Settings to a File")
        else:
            row = layout.row()
            layout.label(text=f"**Set a Save Path in Create NFT Data to Export Settings")

        row = layout.row()
        row.prop(input_tool_scene, "enable_debug")
        if bpy.context.scene.input_tool.enable_debug:
            row.prop(input_tool_scene, "log_path")

        row = layout.row()

        row = layout.row()
        layout.label(text=f"Looking for help?")

        row = layout.row()
        row.operator("wm.url_open", text="Blend_My_NFTs Documentation",
                     icon='URL').url = "https://github.com/torrinworx/Blend_My_NFTs"

        row = layout.row()
        row.operator(
                "wm.url_open",
                text="YouTube Tutorials",
                icon='URL'
        ).url = "https://www.youtube.com/watch?v=ygKJYz4BjRs&list=PLuVvzaanutXcYtWmPVKu2bx83EYNxLRsX"

        row = layout.row()
        row.operator("wm.url_open", text="Join Our Discord Community!",
                     icon='URL').url = "https://discord.gg/UpZt5Un57t"

        row = layout.row()
        layout.label(text=f"{BMNFTS_VERSION}, {LAST_UPDATED}")


# ======== Blender add-on register/unregister handling ======== #
classes = (
      # Property Group Classes:
      BMNFTS_PGT_Input_Properties,

      # Operator Classes:
      Createdata,
      ExportNFTs,
      ResumeFailedBatch,
      RefactorBatches,
      ExportSettings,

      # Panel Classes:
      BMNFTS_PT_CreateData,
      BMNFTS_PT_GenerateNFTs,
      BMNFTS_PT_Refactor,
      BMNFTS_PT_Other,
) + custom_metadata_ui_list.classes_Custom_Metadata_UIList + logic_ui_list.classes_Logic_UIList


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.input_tool = bpy.props.PointerProperty(type=BMNFTS_PGT_Input_Properties)

    bpy.types.Scene.custom_metadata_fields = CollectionProperty(
        type=custom_metadata_ui_list.CUSTOM_custom_metadata_fields_objectCollection)
    bpy.types.Scene.custom_metadata_fields_index = IntProperty()

    bpy.types.Scene.logic_fields = CollectionProperty(type=logic_ui_list.CUSTOM_logic_objectCollection)
    bpy.types.Scene.logic_fields_index = IntProperty()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.input_tool

    del bpy.types.Scene.custom_metadata_fields
    del bpy.types.Scene.custom_metadata_fields_index

    del bpy.types.Scene.logic_fields
    del bpy.types.Scene.logic_fields_index


if __name__ == '__main__':
    register()
    runAsHeadless()
