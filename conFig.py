import platform

mac = 'Darwin'
windows = 'Windows'
slash = ''
save_path = None
save_path_mac = '/Users/torrinleonard/Desktop/Blend_My_NFTs'
save_path_windows = r''

if platform.system() == mac:
    save_path = save_path_mac # The path to the "Blender_Image_Generator" folder
    slash = '/'
elif platform.system() == windows:
    save_path = save_path_windows
    slash = '\\'

nftsPerBatch = 5 # Number of NFTs per batch
renderBatch = 1 # The number of the batch to render in PNG-Generator
imageName = "ThisCozyPlace_" # The name of the NFT image produces by PNG-Generator

batch_path = save_path + slash + 'Batch_Json_files'
images_path = save_path + slash + 'Images from PNG Generator'