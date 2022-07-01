from main import DNA_Generator

def send_To_Record_JSON(input):
    
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