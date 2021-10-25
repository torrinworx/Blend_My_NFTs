import platform

mac = "Darwin"
windows = "Windows"
slash = ""

if platform.system() == mac:
    slash = "/"
elif platform.system() == windows:
    slash = '\\'

numNFTs = 96 # Not yet in code - does nothing

nftsPerBatch = 5 # Number of NFTs per batch
renderBatch = 1 # The number of the batch to render in PNG-Generator
imageName = "ThisCozyPlace" # The name of the NFT image produces by PNG-Generator


save_path = '/Users/torrinleonard/Desktop/Blend_My_NFTs' # The path to the "Blender_Image_Generator" folder
batch_path = save_path + slash + 'Batch_Json_files'
images_path = save_path + slash + 'Images from PNG Generator'