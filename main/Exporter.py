# Purpose:
# This file takes a given Batch created by DNA_Generator.py and tells blender to render the image or export a 3D model to
# the NFT_Output folder.

import bpy
import os
import time
import json
import datetime
from .loading_animation import Loader
from .Constants import bcolors, removeList, remove_file_by_extension


# Save info
def save_batch(batch, file_name):
    saved_batch = json.dumps(batch, indent=1, ensure_ascii=True)

    with open(os.path.join(file_name), 'w') as outfile:
        outfile.write(saved_batch + '\n')

def save_generation_state(batchToGenerate, batch_json_save_path, nftBatch_save_path, enableImages, imageFileFormat, enableAnimations,
                          animationFileFormat, enableModelsBlender, modelFileFormat):
    """Saves date and time of generation start, and generation types; Images, Animations, 3D Models, and the file types for each."""
    file_name = os.path.join(batch_json_save_path, "Batch{}.json".format(batchToGenerate))
    batch = json.load(open(file_name))

    CURRENT_TIME = datetime.datetime.now().strftime("%H:%M:%S")
    CURRENT_DATE = datetime.datetime.now().strftime("%d/%m/%Y")
    LOCAL_TIMEZONE = str(datetime.datetime.now(datetime.timezone.utc))

    if "Generation Save" in batch:
        batch_save_number = int(batch[f"Generation Save"].index(batch[f"Generation Save"][-1]))
    else:
        batch_save_number = 0

    batch["Generation Save"] = list()
    batch["Generation Save"].append({
        "Batch Save Number": batch_save_number + 1,
        "DNA Generated": None,
        "Generation Start Date and Time": [CURRENT_TIME, CURRENT_DATE, LOCAL_TIMEZONE],
        "Render_Settings": {
            "nftBatch_save_path": nftBatch_save_path,
            "enableImages": enableImages,
            "imageFileFormat": imageFileFormat,
            "enableAnimations": enableAnimations,
            "animationFileFormat": animationFileFormat,
            "enableModelsBlender": enableModelsBlender,
            "modelFileFormat": modelFileFormat,
        },
    })

    save_batch(batch, file_name)

def save_completed(single_dna, a, x, batch_json_save_path, batchToGenerate):
    """Saves progress of rendering to batch.json file."""

    file_name = os.path.join(batch_json_save_path, "Batch{}.json".format(batchToGenerate))
    batch = json.load(open(file_name))

    index = batch["BatchDNAList"].index(a)
    batch["BatchDNAList"][index][single_dna]["Complete"] = True
    batch["Generation Save"][-1]["DNA Generated"] = x

    save_batch(batch, file_name)


# Exporter functions:
def getBatchData(batchToGenerate, batch_json_save_path):
    """
    Retrieves a given batches data determined by renderBatch in config.py
    """

    file_name = os.path.join(batch_json_save_path, "Batch{}.json".format(batchToGenerate))
    batch = json.load(open(file_name))

    NFTs_in_Batch = batch["NFTs_in_Batch"]
    hierarchy = batch["hierarchy"]
    BatchDNAList = batch["BatchDNAList"]

    return NFTs_in_Batch, hierarchy, BatchDNAList

def render_and_save_NFTs(nftName, maxNFTs, batchToGenerate, batch_json_save_path, nftBatch_save_path, enableImages,
                                      imageFileFormat, enableAnimations, animationFileFormat, enableModelsBlender,
                                      modelFileFormat, fail_state, failed_batch, failed_dna, failed_dna_index
                                      ):
    """
    Renders the NFT DNA in a Batch#.json, where # is renderBatch in config.py. Turns off the viewport camera and
    the render camera for all items in hierarchy.
    """

    NFTs_in_Batch, hierarchy, BatchDNAList = getBatchData(batchToGenerate, batch_json_save_path)

    time_start_1 = time.time()

    if fail_state:
        for a in range(failed_dna):
            del BatchDNAList[0]
        x = failed_dna + 1

    else:
        save_generation_state(batchToGenerate, batch_json_save_path, nftBatch_save_path, enableImages, imageFileFormat,
                              enableAnimations,
                              animationFileFormat, enableModelsBlender, modelFileFormat)
        x = 1

    for a in BatchDNAList:
        single_dna = list(a.keys())[0]
        for i in hierarchy:
            for j in hierarchy[i]:
                bpy.data.collections[j].hide_render = True
                bpy.data.collections[j].hide_viewport = True

        def match_DNA_to_Variant(single_dna):
            """
            Matches each DNA number separated by "-" to its attribute, then its variant.
            """

            listAttributes = list(hierarchy.keys())
            listDnaDecunstructed = single_dna.split('-')
            dnaDictionary = {}

            for i, j in zip(listAttributes, listDnaDecunstructed):
                dnaDictionary[i] = j

            for x in dnaDictionary:
                for k in hierarchy[x]:
                    kNum = hierarchy[x][k]["number"]
                    if kNum == dnaDictionary[x]:
                        dnaDictionary.update({x: k})
            return dnaDictionary

        dnaDictionary = match_DNA_to_Variant(single_dna)
        name = nftName + "_" + str(x)

        print(f"\n{bcolors.OK}|---Generating NFT {x}/{NFTs_in_Batch} ---|{bcolors.RESET}")
        print(f"DNA attribute list:\n{dnaDictionary}\nDNA Code:{single_dna}")

        for c in dnaDictionary:
            collection = dnaDictionary[c]
            if collection != '0':
                bpy.data.collections[collection].hide_render = False
                bpy.data.collections[collection].hide_viewport = False


        time_start_2 = time.time()

        batchFolder = os.path.join(nftBatch_save_path, "Batch" + str(batchToGenerate))

        imagePath = os.path.join(batchFolder, "Images", name)
        animationPath = os.path.join(batchFolder, "Animations", name)
        modelPath = os.path.join(batchFolder, "Models", name)

        imageFolder = os.path.join(batchFolder, "Images")
        animationFolder = os.path.join(batchFolder, "Animations")
        modelFolder = os.path.join(batchFolder, "Models")
        metaDataFolder = os.path.join(batchFolder, "BMNFT_metaData")

        # Generation/Rendering:
        if enableImages:
            print(f"{bcolors.OK}---Image---{bcolors.RESET}")

            image_render_time_start = time.time()

            def render_image():
                if not os.path.exists(imageFolder):
                    os.makedirs(imageFolder)

                bpy.context.scene.render.filepath = imagePath
                bpy.context.scene.render.image_settings.file_format = imageFileFormat
                bpy.ops.render.render(write_still=True)

            # Loading Animation:
            loading = Loader(f'Rendering Image {x}/{NFTs_in_Batch}...', '').start()
            render_image()
            loading.stop()

            image_render_time_end = time.time()

            print(
                f"{bcolors.OK}Rendered image in {image_render_time_end - image_render_time_start}s.\n{bcolors.RESET}"
            )

        if enableAnimations:
            print(f"{bcolors.OK}---Animation---{bcolors.RESET}")

            animation_render_time_start = time.time()

            def render_animation():
                if not os.path.exists(animationFolder):
                    os.makedirs(animationFolder)

                bpy.context.scene.render.filepath = animationPath

                if animationFileFormat == 'MP4':
                    bpy.context.scene.render.image_settings.file_format = "FFMPEG"

                    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
                    bpy.context.scene.render.ffmpeg.codec = 'H264'
                    bpy.ops.render.render(animation=True)

                else:
                    bpy.context.scene.render.image_settings.file_format = animationFileFormat
                    bpy.ops.render.render(animation=True)

            # Loading Animation:
            loading = Loader(f'Rendering Animation {x}/{NFTs_in_Batch}...', '').start()
            render_animation()
            loading.stop()

            animation_render_time_end = time.time()

            print(
                f"{bcolors.OK}Rendered animation in {animation_render_time_end - animation_render_time_start}s.\n{bcolors.RESET}"
            )

        if enableModelsBlender:
            print(f"{bcolors.OK}---3D Model---{bcolors.RESET}")

            model_generation_time_start = time.time()

            def generate_models():
                if not os.path.exists(modelFolder):
                    os.makedirs(modelFolder)

                for i in dnaDictionary:
                    coll = dnaDictionary[i]
                    if coll != '0':
                        for obj in bpy.data.collections[coll].all_objects:
                            obj.select_set(True)

                for obj in bpy.data.collections['Script_Ignore'].all_objects:
                    obj.select_set(True)

                if modelFileFormat == 'GLB':
                    bpy.ops.export_scene.gltf(filepath=f"{modelPath}.glb",
                                              check_existing=True,
                                              export_format='GLB',
                                              use_selection=True)
                if modelFileFormat == 'GLTF_SEPARATE':
                    bpy.ops.export_scene.gltf(filepath=f"{modelPath}",
                                              check_existing=True,
                                              export_format='GLTF_SEPARATE',
                                              use_selection=True)
                if modelFileFormat == 'GLTF_EMBEDDED':
                    bpy.ops.export_scene.gltf(filepath=f"{modelPath}.gltf",
                                              check_existing=True,
                                              export_format='GLTF_EMBEDDED',
                                              use_selection=True)
                elif modelFileFormat == 'FBX':
                    bpy.ops.export_scene.fbx(filepath=f"{modelPath}.fbx",
                                             check_existing=True,
                                             use_selection=True)
                elif modelFileFormat == 'OBJ':
                    bpy.ops.export_scene.obj(filepath=f"{modelPath}.obj",
                                             check_existing=True,
                                             use_selection=True, )
                elif modelFileFormat == 'X3D':
                    bpy.ops.export_scene.x3d(filepath=f"{modelPath}.x3d",
                                             check_existing=True,
                                             use_selection=True)
                elif modelFileFormat == 'STL':
                    bpy.ops.export_mesh.stl(filepath=f"{modelPath}.stl",
                                            check_existing=True,
                                            use_selection=True)
                elif modelFileFormat == 'VOX':
                    bpy.ops.export_vox.some_data(filepath=f"{modelPath}.vox")

            # Loading Animation:
            loading = Loader(f'Rendering Animation {x}/{NFTs_in_Batch}...', '').start()
            generate_models()
            loading.stop()

            model_generation_time_end = time.time()

            print(
                f"{bcolors.OK}Generated model in {model_generation_time_end - model_generation_time_start}s.\n{bcolors.RESET}"
            )

        if not os.path.exists(metaDataFolder):
            os.makedirs(metaDataFolder)

        for b in dnaDictionary:
            if dnaDictionary[b] == "0":
                dnaDictionary[b] = "Empty"

        metaDataDict = {"name": name, "NFT_DNA": a, "NFT_Variants": dnaDictionary}

        jsonMetaData = json.dumps(metaDataDict, indent=1, ensure_ascii=True)

        with open(os.path.join(metaDataFolder, "Data_" + name + ".json"), 'w') as outfile:
            outfile.write(jsonMetaData + '\n')

        print(f"Completed {name} render in {time.time() - time_start_2}s")

        save_completed(single_dna, a, x, batch_json_save_path, batchToGenerate)

        x += 1

    for i in hierarchy:
        for j in hierarchy[i]:
            bpy.data.collections[j].hide_render = False
            bpy.data.collections[j].hide_viewport = False

    print(f"\nAll NFTs successfully generated and sent to {nftBatch_save_path}"
          f"\nCompleted all renders in Batch{batchToGenerate}.json in {time.time() - time_start_1}s\n")
