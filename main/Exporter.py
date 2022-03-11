# Purpose:
# This file takes a given Batch created by DNA_Generator.py and tells blender to render the image or export a 3D model to
# the NFT_Output folder.

import bpy
import os
import time
import json


enableGeneration = False
colorList = []
generationType = None

class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR


def stripColorFromName(name):
   return "_".join(name.split("_")[:-1])
   
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
                                      modelFileFormat
                                      ):
    """
    Renders the NFT DNA in a Batch#.json, where # is renderBatch in config.py. Turns off the viewport camera and
    the render camera for all items in hierarchy.
    """

    NFTs_in_Batch, hierarchy, BatchDNAList = getBatchData(batchToGenerate, batch_json_save_path)

    time_start_1 = time.time()

    x = 1
    for a in BatchDNAList:
        for i in hierarchy:
            for j in hierarchy[i]:
                if enableGeneration:
                    """
                     Remove Color code so blender recognises the collection
                    """
                    j = stripColorFromName(j)
                bpy.data.collections[j].hide_render = True
                bpy.data.collections[j].hide_viewport = True

        def match_DNA_to_Variant(a):
            """
            Matches each DNA number separated by "-" to its attribute, then its variant.
            """

            listAttributes = list(hierarchy.keys())
            listDnaDecunstructed = a.split('-')
            dnaDictionary = {}

            for i, j in zip(listAttributes, listDnaDecunstructed):
                dnaDictionary[i] = j

            for x in dnaDictionary:
                for k in hierarchy[x]:
                    kNum = hierarchy[x][k]["number"]
                    if kNum == dnaDictionary[x]:
                        dnaDictionary.update({x: k})
            return dnaDictionary

        dnaDictionary = match_DNA_to_Variant(a)
        name = nftName + "_" + str(x)

        print(f"\n{bcolors.OK}|---Generating NFT {x}/{NFTs_in_Batch} ---|{bcolors.RESET}")
        print(f"DNA attribute list:\n{dnaDictionary}\nDNA Code:{a}")

        for c in dnaDictionary:
            collection = dnaDictionary[c]
            if not enableGeneration:
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

        # Material handling:
        if enableGeneration:
            for c in dnaDictionary:
                collection = dnaDictionary[c]
                if stripColorFromName(collection) in colorList:
                    colorVal = int(collection.rsplit("_", 1)[1])-1
                    collection = stripColorFromName(collection)
                    bpy.data.collections[collection].hide_render = False
                    bpy.data.collections[collection].hide_viewport = False
                    if generationType == 'color':
                        for activeObject in bpy.data.collections[collection].all_objects: 
                            mat = bpy.data.materials.new("PKHG")
                            mat.diffuse_color = colorList[collection][colorVal]
                            activeObject.active_material = mat
                    if generationType == 'material':
                        for activeObject in bpy.data.collections[collection].all_objects: 
                            activeObject.material_slots[0].material = bpy.data.materials[colorList[collection][colorVal]]
                else:
                    collection = stripColorFromName(collection)
                    bpy.data.collections[collection].hide_render = False
                    bpy.data.collections[collection].hide_viewport = False

        if enableImages:
            print(f"{bcolors.OK}Rendering Image{bcolors.RESET}")

            if not os.path.exists(imageFolder):
                os.makedirs(imageFolder)

            bpy.context.scene.render.filepath = imagePath
            bpy.context.scene.render.image_settings.file_format = imageFileFormat
            bpy.ops.render.render(write_still=True)

        if enableAnimations:
            print(f"{bcolors.OK}Rendering Animation{bcolors.RESET}")
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

        if enableModelsBlender:
            print(f"{bcolors.OK}Generating 3D Model{bcolors.RESET}")
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
                                         use_selection=True,)
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

        if not os.path.exists(metaDataFolder):
            os.makedirs(metaDataFolder)

        for b in dnaDictionary:
            if dnaDictionary[b] == "0":
                dnaDictionary[b] = "Empty"

        metaDataDict = {"name": name, "NFT_DNA": a, "NFT_Variants": dnaDictionary}

        jsonMetaData = json.dumps(metaDataDict, indent=1, ensure_ascii=True)

        with open(os.path.join(metaDataFolder, "Data_" + name + ".json"), 'w') as outfile:
            outfile.write(jsonMetaData + '\n')

        print("Completed {} render in ".format(name) + "%.4f seconds" % (time.time() - time_start_2))
        x += 1

    for a in BatchDNAList:
        for i in hierarchy:
            for j in hierarchy[i]:
                if enableGeneration:
                    j = stripColorFromName(j)
                bpy.data.collections[j].hide_render = False
                bpy.data.collections[j].hide_viewport = False

    print(f"\nAll NFTs successfully generated and sent to {nftBatch_save_path}")
    print("Completed all renders in Batch{}.json in ".format(batchToGenerate) + "%.4f seconds" % (time.time() - time_start_1) + "\n")


if __name__ == '__main__':
    render_and_save_NFTs()
