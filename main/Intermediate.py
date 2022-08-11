import json
import bpy

from main import DNA_Generator, Exporter


def send_To_Record_JSON(input, reverse_order=False):
    if input.enableLogic:
        if input.enable_Logic_Json and input.logicFile:
            input.logicFile = json.load(open(input.logicFile))

        if input.enable_Logic_Json and not input.logicFile:
            print({'ERROR'}, f"No Logic.json file path set. Please set the file path to your Logic.json file.")

        if not input.enable_Logic_Json:
            scn = bpy.context.scene
            if reverse_order:
                input.logicFile = {}
                num = 1
                for i in range(scn.logic_fields_index, -1, -1):
                    item = scn.logic_fields[i]

                    item_list1 = item.item_list1
                    rule_type = item.rule_type
                    item_list2 = item.item_list2
                    input.logicFile[f"Rule-{num}"] = {
                        "IF": item_list1.split(','),
                        rule_type: item_list2.split(',')
                    }
                    print(rule_type)
                    num += 1
            else:
                input.logicFile = {}
                num = 1
                for item in scn.logic_fields:
                    item_list1 = item.item_list1
                    rule_type = item.rule_type
                    item_list2 = item.item_list2
                    input.logicFile[f"Rule-{num}"] = {
                        "IF": item_list1.split(','),
                        rule_type: item_list2.split(',')
                    }
                    print(rule_type)

                    num += 1

    DNA_Generator.send_To_Record_JSON(input.collectionSize,
                                      input.nftsPerBatch,
                                      input.save_path,
                                      input.enableRarity,
                                      input.enableLogic,
                                      input.logicFile,
                                      input.enableMaterials,
                                      input.materialsFile,
                                      input.Blend_My_NFTs_Output,
                                      input.batch_json_save_path
                                      )


def render_and_save_NFTs(input, reverse_order=False):
    if input.enableCustomFields:
        scn = bpy.context.scene
        if reverse_order:
            for i in range(scn.custom_metadata_fields_index, -1, -1):
                item = scn.custom_metadata_fields[i]
                if item.field_name in list(input.custom_Fields.keys()):
                    raise ValueError(
                        f"A duplicate of '{item.field_name}' was found. Please ensure all Custom Metadata field Names are unique.")
                else:
                    input.custom_Fields[item.field_name] = item.field_value
        else:
            for item in scn.custom_metadata_fields:
                if item.field_name in list(input.custom_Fields.keys()):
                    raise ValueError(
                        f"A duplicate of '{item.field_name}' was found. Please ensure all Custom Metadata field Names are unique.")
                else:
                    input.custom_Fields[item.field_name] = item.field_value

    Exporter.render_and_save_NFTs(input)
