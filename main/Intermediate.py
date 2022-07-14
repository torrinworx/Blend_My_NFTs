import json
import bpy

def send_To_Record_JSON(input):
from main import DNA_Generator, Exporter

def send_To_Record_JSON(input, reverse_order=False):
    
    DNA_Generator.send_To_Record_JSON(  input.collectionSize, 
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

