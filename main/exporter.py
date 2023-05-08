# Purpose:
# This file takes a given Batch created by dna_generator.py and tells blender to render the image or export a 3D model
# to the NFT_Output folder.

import bpy
import os
import ssl
import time
import json
import smtplib
import logging
import datetime
import platform
import traceback
import subprocess
import shutil
from subprocess import run
from glob import glob

from .helpers import TextColors, Loader
from .metadata_templates import create_cardano_metadata, createSolanaMetaData, create_erc721_meta_data

log = logging.getLogger(__name__)


# Save info
def save_batch(batch, file_name):
    saved_batch = json.dumps(batch, indent=1, ensure_ascii=True)

    with open(os.path.join(file_name), 'w') as outfile:
        outfile.write(saved_batch + '\n')


def save_generation_state(input):
    """
    Saves date and time of generation start, and generation types; Images, Animations, 3D Models, and the file types for
    each.
    """
    file_name = os.path.join(input.batch_json_save_path, "Batch{}.json".format(input.batch_to_generate))
    batch = json.load(open(file_name))

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%d/%m/%Y")
    local_timezone = str(datetime.datetime.now(datetime.timezone.utc))

    if "Generation Save" in batch:
        batch_save_number = int(batch[f"Generation Save"].index(batch[f"Generation Save"][-1]))
    else:
        batch_save_number = 0

    batch["Generation Save"] = list()
    batch["Generation Save"].append({
            "Batch Save Number": batch_save_number + 1,
            "DNA Generated": None,
            "Generation Start Date and Time": [current_time, current_date, local_timezone],
            "Render_Settings": {
                    "nft_name": input.nft_name,
                    "save_path": input.save_path,
                    "nfts_per_batch": input.nfts_per_batch,
                    "batch_to_generate": input.batch_to_generate,
                    "collection_size": input.collection_size,

                    "blend_my_nfts_output": input.blend_my_nfts_output,
                    "batch_json_save_path": input.batch_json_save_path,
                    "nft_batch_save_path": input.nft_batch_save_path,

                    "enable_images": input.enable_images,
                    "image_file_format": input.image_file_format,

                    "enable_animations": input.enable_animations,
                    "animation_file_format": input.animation_file_format,

                    "enable_models": input.enable_models,
                    "model_file_format": input.model_file_format,

                    "enable_custom_fields": input.enable_custom_fields,

                    "cardano_metadata_bool": input.cardano_metadata_bool,
                    "solana_metadata_bool": input.solana_metadata_bool,
                    "erc721_metadata": input.erc721_metadata,

                    "cardano_description": input.cardano_description,
                    "solana_description": input.solana_description,
                    "erc721_description": input.erc721_description,

                    "enable_materials": input.enable_materials,
                    "materials_file": input.materials_file,

                    "enable_logic": input.enable_logic,
                    "enable_logic_json": input.enable_logic_json,
                    "logic_file": input.logic_file,

                    "enable_rarity": input.enable_rarity,

                    "enable_auto_shutdown": input.enable_auto_shutdown,

                    "specify_time_bool": input.specify_time_bool,
                    "hours": input.hours,
                    "minutes": input.minutes,

                    "email_notification_bool": input.email_notification_bool,
                    "sender_from": input.sender_from,
                    "email_password": input.email_password,
                    "receiver_to": input.receiver_to,

                    "enable_debug": input.enable_debug,
                    "log_path": input.log_path,

                    "enable_dry_run": input.enable_dry_run,

                    "custom_fields": input.custom_fields,
            },
    })

    save_batch(batch, file_name)


def save_completed(full_single_dna, a, x, batch_json_save_path, batch_to_generate):
    """Saves progress of rendering to batch.json file."""

    file_name = os.path.join(batch_json_save_path, "Batch{}.json".format(batch_to_generate))
    batch = json.load(open(file_name))
    index = batch["batch_dna_list"].index(a)
    batch["batch_dna_list"][index][full_single_dna]["complete"] = True
    batch["Generation Save"][-1]["DNA Generated"] = x

    save_batch(batch, file_name)


# Exporter functions:
def get_batch_data(batch_to_generate, batch_json_save_path):
    """
    Retrieves a given batches data determined by renderBatch in config.py
    """

    file_name = os.path.join(batch_json_save_path, "Batch{}.json".format(batch_to_generate))
    batch = json.load(open(file_name))

    nfts_in_batch = batch["nfts_in_batch"]
    hierarchy = batch["hierarchy"]
    batch_dna_list = batch["batch_dna_list"]

    return nfts_in_batch, hierarchy, batch_dna_list


# Convert PNG's into GIF using Gifski
def pngs_2_gifs(context, abspath, frames_folder):
    """Convert the PNGs to Animated GIF"""

    o_file = ''.join([abspath])
    gifski = "gifski"
    if not context.gifski_path.strip() == "":
        gifski = bpy.path.abspath(context.gifski_path.strip())

    command = [gifski]

    if context.gifski_quality:
        command.append("--quality")
        command.append(str(context.gifski_quality))

    if context.gifski_fps:
        command.append("--fps")
        command.append(str(context.gifski_fps))

    if context.gifski_loop:
        command.append("--repeat")
        command.append(str(context.gifski_loop)) 

    if context.gifski_width:
        command.append("-W")
        command.append(str(context.gifski_width))

    if context.gifski_height:
        command.append("-H")
        command.append(str(context.gifski_height))       

    # Need to figure out why subprocess hates *.png calls and remove this manual file injection
    # for file in os.listdir(frames_folder): 
    #     if file.endswith(".png"):
    #         command.append(os.path.join(frames_folder, file))
    # subprocess.call(command)
    
    run(' '.join(command) + ' -o "' + o_file + '" "' + frames_folder + '/"*.png')


def render_and_save_nfts(input):
    """
    Renders the NFT DNA in a Batch#.json, where # is renderBatch in config.py. Turns off the viewport camera and
    the render camera for all items in hierarchy.
    """

    time_start_1 = time.time()

    # If failed Batch is detected and user is resuming its generation:
    if input.fail_state:
        log.info(
                f"{TextColors.OK}\nResuming Batch #{input.failed_batch}{TextColors.RESET}"
        )
        nfts_in_batch, hierarchy, batch_dna_list = get_batch_data(input.failed_batch, input.batch_json_save_path)
        for a in range(input.failed_dna):
            del batch_dna_list[0]
        x = input.failed_dna + 1

    # If user is generating the normal way:
    else:
        log.info(
                f"{TextColors.OK}\n======== Generating Batch #{input.batch_to_generate} ========{TextColors.RESET}"
        )
        nfts_in_batch, hierarchy, batch_dna_list = get_batch_data(input.batch_to_generate, input.batch_json_save_path)
        save_generation_state(input)
        x = 1

    if input.enable_materials:
        materials_file = json.load(open(input.materials_file))

    for a in batch_dna_list:
        full_single_dna = list(a.keys())[0]
        order_num_offset = input.order_num_offset
        order_num = a[full_single_dna]['order_num'] + order_num_offset

        # Material handling:
        if input.enable_materials:
            single_dna, material_dna = full_single_dna.split(':')

        if not input.enable_materials:
            single_dna = full_single_dna

        def match_dna_to_variant(single_dna):
            """
            Matches each DNA number separated by "-" to its attribute, then its variant.
            """

            list_attributes = list(hierarchy.keys())
            list_dna_deconstructed = single_dna.split('-')
            dna_dictionary = {}

            for i, j in zip(list_attributes, list_dna_deconstructed):
                dna_dictionary[i] = j

            for x in dna_dictionary:
                for k in hierarchy[x]:
                    k_num = hierarchy[x][k]["number"]
                    if k_num == dna_dictionary[x]:
                        dna_dictionary.update({x: k})
            return dna_dictionary

        def match_material_dna_to_material(single_dna, material_dna, materials_file):
            """
            Matches the Material DNA to it's selected Materials unless a 0 is present meaning no material for that variant was selected.
            """
            list_attributes = list(hierarchy.keys())
            list_dna_deconstructed = single_dna.split('-')
            list_material_dna_deconstructed = material_dna.split('-')

            full_dna_dict = {}

            for attribute, variant, material in zip(
                    list_attributes,
                    list_dna_deconstructed,
                    list_material_dna_deconstructed
            ):

                for var in hierarchy[attribute]:
                    if hierarchy[attribute][var]['number'] == variant:
                        variant = var

                if material != '0':  # If material is not empty
                    for variant_m in materials_file:
                        if variant == variant_m:
                            # Getting Materials name from Materials index in the Materials List
                            materials_list = list(materials_file[variant_m]["Material List"].keys())

                            material = materials_list[int(material) - 1]  # Subtract 1 because '0' means empty mat
                            break

                full_dna_dict[variant] = material

            return full_dna_dict

        metadata_material_dict = {}

        if input.enable_materials:
            material_dna_dictionary = match_material_dna_to_material(single_dna, material_dna, materials_file)

            for var_mat in list(material_dna_dictionary.keys()):
                if material_dna_dictionary[var_mat]!='0':
                    if not materials_file[var_mat]['Variant Objects']:
                        """
                        If objects to apply material to not specified, apply to all objects in Variant collection.
                        """
                        metadata_material_dict[var_mat] = material_dna_dictionary[var_mat]

                        for obj in bpy.data.collections[var_mat].all_objects:
                            selected_object = bpy.data.objects.get(obj.name)
                            selected_object.active_material = bpy.data.materials[material_dna_dictionary[var_mat]]

                    if materials_file[var_mat]['Variant Objects']:
                        """
                        If objects to apply material to are specified, apply material only to objects specified withing 
                        the Variant collection.
                        """
                        metadata_material_dict[var_mat] = material_dna_dictionary[var_mat]

                        for obj in materials_file[var_mat]['Variant Objects']:
                            selected_object = bpy.data.objects.get(obj)
                            selected_object.active_material = bpy.data.materials[material_dna_dictionary[var_mat]]

        # Turn off render camera and viewport camera for all collections in hierarchy
        for i in hierarchy:
            for j in hierarchy[i]:
                try:
                    bpy.data.collections[j].hide_render = True
                    bpy.data.collections[j].hide_viewport = True
                except KeyError:
                    log.error(
                            f"\n{traceback.format_exc()}"
                            f"\n{TextColors.ERROR}Blend_My_NFTs Error:\n"
                            f"The Collection '{j}' appears to be missing or has been renamed. If you made any changes "
                            f"to your .blend file scene, ensure you re-create your NFT Data so Blend_My_NFTs can read "
                            f"your scene. For more information see:{TextColors.RESET}"
                            f"\nhttps://github.com/torrinworx/Blend_My_NFTs#blender-file-organization-and-structure\n"
                    )
                    raise TypeError()

        dna_dictionary = match_dna_to_variant(single_dna)
        name = input.nft_name + "_" + str(order_num)

        # Change Text Object in Scene to match DNA string:
        # Variables that can be used: full_single_dna, name, order_num
        # ob = bpy.data.objects['Text']  # Object name
        # ob.data.body = str(f"DNA: {full_single_dna}")  # Set text of Text Object ob

        log.info(
                f"\n{TextColors.OK}======== Generating NFT {x}/{nfts_in_batch}: {name} ========{TextColors.RESET}"
                f"\nVariants selected:"
                f"\n{dna_dictionary}"
        )
        if input.enable_materials:
            log.info(
                    f"\nMaterials selected:"
                    f"\n{material_dna_dictionary}"
            )

        log.info(f"\nDNA Code:{full_single_dna}")

        for c in dna_dictionary:
            collection = dna_dictionary[c]
            if collection != '0':
                bpy.data.collections[collection].hide_render = False
                bpy.data.collections[collection].hide_viewport = False

        time_start_2 = time.time()

        # Main paths for batch sub-folders:
        batch_folder = os.path.join(input.nft_batch_save_path, "Batch" + str(input.batch_to_generate))

        image_folder = os.path.join(batch_folder, "Images")
        animation_folder = os.path.join(batch_folder, "Animations")
        model_folder = os.path.join(batch_folder, "Models")
        bmnft_data_folder = os.path.join(batch_folder, "BMNFT_data")

        image_path = os.path.join(image_folder, name)
        animation_path = os.path.join(animation_folder, name)
        model_path = os.path.join(model_folder, name)

        cardano_metadata_path = os.path.join(batch_folder, "Cardano_metadata")
        solana_metadata_path = os.path.join(batch_folder, "Solana_metadata")
        erc721_metadata_path = os.path.join(batch_folder, "Erc721_metadata")

        def check_failed_exists(file_path):
            """
            Delete a file if a fail state is detected and if the file being re-generated already exists. Prevents
            animations from corrupting.
            """
            if input.fail_state:
                if os.path.exists(file_path):
                    os.remove(file_path)

        # Generation/Rendering:
        if input.enable_images:

            log.info(f"\n{TextColors.OK}-------- Image --------{TextColors.RESET}")

            image_render_time_start = time.time()

            check_failed_exists(image_path)

            def render_image():
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)

                bpy.context.scene.render.filepath = image_path
                bpy.context.scene.render.image_settings.file_format = input.image_file_format

                if not input.enable_debug:
                    bpy.ops.render.render(write_still=True)

            # Loading Animation:
            loading = Loader(f'Rendering Image {x}/{nfts_in_batch}...', '').start()
            render_image()
            loading.stop()

            image_render_time_end = time.time()

            log.info(
                    f"{TextColors.OK}TIME [Rendered Image]: {image_render_time_end - image_render_time_start}s."
                    f"\n{TextColors.RESET}"
            )

        if input.enable_animations:
            log.info(f"\n{TextColors.OK}-------- Animation --------{TextColors.RESET}")

            animation_render_time_start = time.time()

            check_failed_exists(animation_path)

            def render_animation():
                if not os.path.exists(animation_folder):
                    os.makedirs(animation_folder)

                if not input.enable_debug:
                    if input.animation_file_format == 'MP4':
                        bpy.context.scene.render.filepath = animation_path
                        bpy.context.scene.render.image_settings.file_format = "FFMPEG"

                        bpy.context.scene.render.ffmpeg.format = 'MPEG4'
                        bpy.context.scene.render.ffmpeg.codec = 'H264'
                        bpy.ops.render.render(animation=True)

                    elif input.animation_file_format == 'PNG':
                        if not os.path.exists(animation_path):
                            os.makedirs(animation_path)

                        bpy.context.scene.render.filepath = os.path.join(animation_path, name)
                        bpy.context.scene.render.image_settings.file_format = input.animation_file_format
                        bpy.ops.render.render(animation=True)

                    elif input.animation_file_format == 'TIFF':
                        if not os.path.exists(animation_path):
                            os.makedirs(animation_path)

                        bpy.context.scene.render.filepath = os.path.join(animation_path, name)
                        bpy.context.scene.render.image_settings.file_format = input.animation_file_format
                        bpy.ops.render.render(animation=True)

                    elif input.animation_file_format == 'GIF':
                        if not os.path.exists(animation_path):
                            os.makedirs(animation_path)

                        bpy.context.scene.render.filepath = os.path.join(animation_path, name)
                        bpy.context.scene.render.image_settings.file_format = 'PNG'
                        bpy.ops.render.render(animation=True)

                        i_file = os.path.join(animation_folder, name + '.gif')

                        # Not sure where to store / add the generated image path to?
                        pngs_2_gifs(input, i_file, animation_path)

                        if input.gifski_delete_frames:
                            shutil.rmtree(animation_path)

                    else:
                        bpy.context.scene.render.filepath = animation_path
                        bpy.context.scene.render.image_settings.file_format = input.animation_file_format
                        bpy.ops.render.render(animation=True)

            # Loading Animation:
            loading = Loader(f'Rendering Animation {x}/{nfts_in_batch}...', '').start()
            render_animation()
            loading.stop()

            animation_render_time_end = time.time()

            log.info(
                    f"\n{TextColors.OK}TIME [Rendered Animation]: "
                    f"{animation_render_time_end - animation_render_time_start}s.{TextColors.RESET}"
            )

        if input.enable_models:
            log.info(f"\n{TextColors.OK}-------- 3D Model --------{TextColors.RESET}")

            model_generation_time_start = time.time()

            def generate_models():
                if not os.path.exists(model_folder):
                    os.makedirs(model_folder)

                for i in dna_dictionary:
                    coll = dna_dictionary[i]
                    if coll != '0':
                        for obj in bpy.data.collections[coll].all_objects:
                            obj.select_set(True)

                for obj in bpy.data.collections['Script_Ignore'].all_objects:
                    obj.select_set(True)

                # Remove objects from 3D model export:
                # remove_objects: list = [
                # ]
                #
                # for obj in bpy.data.objects:
                #     if obj.name in remove_objects:
                #         obj.select_set(False)

                if not input.enable_debug:
                    if input.model_file_format == 'GLB':
                        check_failed_exists(f"{model_path}.glb")
                        bpy.ops.export_scene.gltf(
                                filepath=f"{model_path}.glb",
                                check_existing=True,
                                export_format='GLB',
                                export_keep_originals=True,
                                use_selection=True
                        )
                    if input.model_file_format == 'GLTF_SEPARATE':
                        check_failed_exists(f"{model_path}.gltf")
                        check_failed_exists(f"{model_path}.bin")
                        bpy.ops.export_scene.gltf(
                                filepath=f"{model_path}",
                                check_existing=True,
                                export_format='GLTF_SEPARATE',
                                export_keep_originals=True,
                                use_selection=True
                        )
                    if input.model_file_format == 'GLTF_EMBEDDED':
                        check_failed_exists(f"{model_path}.gltf")
                        bpy.ops.export_scene.gltf(
                                filepath=f"{model_path}.gltf",
                                check_existing=True,
                                export_format='GLTF_EMBEDDED',
                                export_keep_originals=True,
                                use_selection=True
                        )
                    elif input.model_file_format == 'FBX':
                        check_failed_exists(f"{model_path}.fbx")
                        bpy.ops.export_scene.fbx(
                                filepath=f"{model_path}.fbx",
                                check_existing=True,
                                use_selection=True
                        )
                    elif input.model_file_format == 'OBJ':
                        check_failed_exists(f"{model_path}.obj")
                        bpy.ops.export_scene.obj(
                                filepath=f"{model_path}.obj",
                                check_existing=True,
                                use_selection=True,
                        )
                    elif input.model_file_format == 'X3D':
                        check_failed_exists(f"{model_path}.x3d")
                        bpy.ops.export_scene.x3d(
                                filepath=f"{model_path}.x3d",
                                check_existing=True,
                                use_selection=True
                        )
                    elif input.model_file_format == 'STL':
                        check_failed_exists(f"{model_path}.stl")
                        bpy.ops.export_mesh.stl(
                                filepath=f"{model_path}.stl",
                                check_existing=True,
                                use_selection=True
                        )
                    elif input.model_file_format == 'VOX':
                        check_failed_exists(f"{model_path}.vox")
                        bpy.ops.export_vox.some_data(filepath=f"{model_path}.vox")

            # Loading Animation:
            loading = Loader(f'Generating 3D model {x}/{nfts_in_batch}...', '').start()
            generate_models()
            loading.stop()

            model_generation_time_end = time.time()

            log.info(
                    f"\n{TextColors.OK}TIME [Generated 3D Model]: "
                    f"{model_generation_time_end - model_generation_time_start}s.{TextColors.RESET}"
            )

        # Generating Metadata:
        if input.cardano_metadata_bool:
            if not os.path.exists(cardano_metadata_path):
                os.makedirs(cardano_metadata_path)
            create_cardano_metadata(
                    name,
                    order_num,
                    full_single_dna,
                    dna_dictionary,
                    metadata_material_dict,
                    input.custom_fields,
                    input.enable_custom_fields,
                    input.cardano_description,
                    cardano_metadata_path
            )

        if input.solana_metadata_bool:
            if not os.path.exists(solana_metadata_path):
                os.makedirs(solana_metadata_path)
            createSolanaMetaData(
                    name,
                    order_num,
                    full_single_dna,
                    dna_dictionary,
                    metadata_material_dict,
                    input.custom_fields,
                    input.enable_custom_fields,
                    input.solana_description,
                    solana_metadata_path
            )

        if input.erc721_metadata:
            if not os.path.exists(erc721_metadata_path):
                os.makedirs(erc721_metadata_path)
            create_erc721_meta_data(
                    name,
                    order_num,
                    full_single_dna,
                    dna_dictionary,
                    metadata_material_dict,
                    input.custom_fields,
                    input.enable_custom_fields,
                    input.erc721_description,
                    erc721_metadata_path
            )

        if not os.path.exists(bmnft_data_folder):
            os.makedirs(bmnft_data_folder)

        for b in dna_dictionary:
            if dna_dictionary[b] == "0":
                dna_dictionary[b] = "Empty"

        meta_data_dict = {
                "name": name,
                "nft_dna": a,
                "nft_variants": dna_dictionary,
                "material_attributes": metadata_material_dict
        }

        json_meta_data = json.dumps(meta_data_dict, indent=1, ensure_ascii=True)

        with open(os.path.join(bmnft_data_folder, "Data_" + name + ".json"), 'w') as outfile:
            outfile.write(json_meta_data + '\n')

        log.info(f"{TextColors.OK}\nTIME [NFT {name} Generated]: {time.time() - time_start_2}s")

        save_completed(full_single_dna, a, x, input.batch_json_save_path, input.batch_to_generate)

        x += 1

    for i in hierarchy:
        for j in hierarchy[i]:
            bpy.data.collections[j].hide_render = False
            bpy.data.collections[j].hide_viewport = False

    batch_complete_time = time.time() - time_start_1

    log.info(
            f"\nAll NFTs in Batch {input.batch_to_generate} successfully generated and saved at:"
            f"\n{input.nft_batch_save_path}"
            f"\nTIME [Batch {input.batch_to_generate} Generated]: {batch_complete_time}s\n"
    )

    batch_info = {"Batch Render Time": batch_complete_time, "Number of NFTs generated in Batch": x - 1,
                  "Average time per generation": batch_complete_time / x - 1}

    batch_info_folder = os.path.join(
            input.nft_batch_save_path,
            "Batch" + str(input.batch_to_generate),
            "batch_info.json"
    )

    save_batch(batch_info, batch_info_folder)

    # Send Email that Batch is complete:
    if input.email_notification_bool:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = input.sender_from  # Enter your address
        receiver_email = input.receiver_to  # Enter receiver address
        password = input.email_password

        # Get batch info for message:
        if input.fail_state:
            batch = input.fail_state
            batch_data = get_batch_data(input.failed_batch, input.batch_json_save_path)

        else:
            batch_data = get_batch_data(input.batch_to_generate, input.batch_json_save_path)

            batch = input.batch_to_generate

        generation_time = str(datetime.timedelta(seconds=batch_complete_time))

        message = f"""\
        Subject: Batch {batch} completed {x - 1} NFTs in {generation_time} (h:m:s)

        Generation Time:
        {generation_time.split(':')[0]} Hours, 
        {generation_time.split(':')[1]} Minutes, 
        {generation_time.split(':')[2]} Seconds
        Batch Data:

            {batch_data}

        This message was sent from an instance of the Blend_My_NFTs Blender add-on.
        """

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    # Automatic Shutdown:
    # If user selects automatic shutdown but did not specify time after Batch completion
    def shutdown(time):
        if platform.system() == "Windows":
            os.system(f"shutdown /s /t {time}")
        if platform.system() == "Darwin":
            os.system(f"shutdown /s /t {time}")

    if input.enable_auto_shutdown and not input.specify_time_bool:
        shutdown(0)

    # If user selects automatic shutdown and specify time after Batch completion
    if input.enable_auto_shutdown and input.specify_time_bool:
        hours = (int(input.hours) / 60) / 60
        minutes = int(input.minutes) / 60
        total_sleep_time = hours + minutes

        # time.sleep(total_sleep_time)

        shutdown(total_sleep_time)
