import platform

# NFT configurations:
maxNFTs = 0    # The maximum number of NFTs you want to generate
nftsPerBatch = 0    # Number of NFTs per batch
renderBatch = 0     # The batch number to render in PNG-Generator
imageName = "ThisCozyPlace_"    # The name of the NFT image produces by PNG-Generator

# Save path of Blend_My_NFTs folder:
# Example mac: /Users/Path/to/Blend_My_NFTs
# Example windows: C:\Users\Path\to\Blend_My_NFTs
save_path_mac = ''
save_path_windows = r''

mac = 'Darwin' # Mac OS
windows = 'Windows' # Windows
slash = '' # Leave empty
save_path = None # Leave empty

# Save_path utilities and os compatibility
if platform.system() == mac:
    save_path = save_path_mac
    slash = '/'
elif platform.system() == windows:
    save_path = save_path_windows
    slash = '\\'

# Paths to folders
batch_path = save_path + slash + 'Batch_Json_files'
images_path = save_path + slash + 'Images from PNG Generator'