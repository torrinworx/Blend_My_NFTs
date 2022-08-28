import logging

import bpy
import json

from main import dna_generator, exporter

log = logging.getLogger(__name__)

# TODO: migrate this code to the dna_generator.py(send_to_record) and exporter.py(render_and_save) to simplify render
#  process into one file.


def send_to_record(input, reverse_order=False):
    if input.enable_logic:
        if input.enable_logic_json and input.logic_file:
            input.logic_file = json.load(open(input.logic_file))

        if input.enable_logic_json and not input.logic_file:
            log.error(
                    f"No Logic.json file path set. Please set the file path to your Logic.json file."
            )
            raise

        if not input.enable_logic_json:
            scn = bpy.context.scene
            if reverse_order:
                input.logic_file = {}
                num = 1
                for i in range(scn.logic_fields_index, -1, -1):
                    item = scn.logic_fields[i]

                    item_list1 = item.item_list1
                    rule_type = item.rule_type
                    item_list2 = item.item_list2
                    input.logic_file[f"Rule-{num}"] = {
                        "IF": item_list1.split(','),
                        rule_type: item_list2.split(',')
                    }
                    num += 1
            else:
                input.logic_file = {}
                num = 1
                for item in scn.logic_fields:
                    item_list1 = item.item_list1
                    rule_type = item.rule_type
                    item_list2 = item.item_list2
                    input.logic_file[f"Rule-{num}"] = {
                        "IF": item_list1.split(','),
                        rule_type: item_list2.split(',')
                    }
                    num += 1

    dna_generator.send_to_record(
            input.collection_size,
            input.nfts_per_batch,
            input.save_path,
            input.enable_rarity,
            input.enable_logic,
            input.logic_file,
            input.enable_materials,
            input.materials_file,
            input.blend_my_nfts_output,
            input.batch_json_save_path,
            input.enable_debug,
            input.log_path
    )


def render_and_save_nfts(input, reverse_order=False):
    if input.enable_custom_fields:
        scn = bpy.context.scene
        if reverse_order:
            for i in range(scn.custom_metadata_fields_index, -1, -1):
                item = scn.custom_metadata_fields[i]
                if item.field_name in list(input.custom_fields.keys()):
                    log.error(
                            f"A duplicate of '{item.field_name}' was found. Ensure all Custom Metadata field "
                            f"Names are unique."
                    )
                    raise ValueError()
                else:
                    input.custom_fields[item.field_name] = item.field_value
        else:
            for item in scn.custom_metadata_fields:
                if item.field_name in list(input.custom_fields.keys()):
                    log.error(
                            f"A duplicate of '{item.field_name}' was found. Ensure all Custom Metadata field "
                            f"Names are unique."
                    )
                    raise ValueError()
                else:
                    input.custom_fields[item.field_name] = item.field_value

    exporter.render_and_save_nfts(input)
