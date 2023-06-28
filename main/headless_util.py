# adding CLI arguments
# Used this as a basis:
# https://developer.blender.org/diffusion/B/browse/master/release/scripts/templates_py/background_job.py

import sys
import argparse


def get_python_args():

    argv = sys.argv

    if "--" not in argv:
        argv = []  # as if no args are passed
    else:
        argv = argv[argv.index("--") + 1:]  # get all args after "--"

    usage_text = (
        "Run Blend_My_NFTs heedlessly from the command line\n"
        "usage:\n"
        "blender -background --python <Path to BMNFTs __init__.py> -- --config-file <path to config file>"
    )
    
    parser = argparse.ArgumentParser(description=usage_text)
    
    parser.add_argument("--config-file",
                        dest="config_path",
                        metavar='FILE',
                        required=True,
                        help="Provide the full file path of the config.cfg file generated from the addon"
                        )

    parser.add_argument("--operation",
                        dest="operation",
                        choices=['create-dna', 'generate-nfts', 'refactor-batches'],
                        required=True,
                        help="Choose which operation you want to perform"
                        )

    parser.add_argument("--save-path",
                        dest="save_path",
                        metavar='FOLDER',
                        required=False,
                        help="Overwrite the save path in the config file"
                        )

    parser.add_argument("--batch-number",
                        dest="batch_number",
                        type=int,
                        required=False,
                        help="Overwrite the batch number in the config file"
                        )

    parser.add_argument("--batch-data",
                        dest="batch_data_path",
                        metavar='FOLDER',
                        required=False,
                        help="Use pre-existing batch data for rendering"
                        )

    parser.add_argument("--logic-file",
                        dest="logic_file",
                        metavar='FILE',
                        required=False,
                        help="Overwrite the logic file path in the config file"
                        )

    parser.add_argument("--resume-failed-batch",
                        dest="resume_failed_batch",
                        action="store_true",
                        required=False,
                        help="Resume failed batch"
                        )

    parser.add_argument("--cycles-device",
                        dest="cycles-device",
                        choices=["OPTIX", "CUDA"],
                        required=False,
                        help="set cycles device to either OptiX or CUDA"
                        )

    return parser.parse_args(argv), parser
