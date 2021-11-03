import platform

# NFT configurations:
maxNFTs = 0    # The maximum number of NFTs you want to generate - doesn't do anything yet
nftsPerBatch = 2   # Number of NFTs per batch
renderBatch = 1     # The batch number to render in PNG-Generator
imageName = "ThisCozyPlace_"    # The name of the NFT image produces by PNG-Generator
fileFormat = 'JPEG' # Dictate the image extension when Blender renders the images
# Visit https://docs.blender.org/api/current/bpy.types.Image.html#bpy.types.Image.file_format
# for a list of file formats supported by Blender. Enter the file extension exactly as specified in
# the Blender API documentation above.

includeRarity = False
# True = include weighted rarity percentages in NFTRecord.json calculations,
# False = Pure random selection of variants

resetViewport = True # Turns all viewport and render cameras on after Image_Generator

generateColors = True # When set to true this applies the sets of colors listed below to the objects in the collections named below 

# The collections below are RGBA Color values. You can put as many or as little color values in these lists as you would like.
# You can create any number of rgbaColorLists and assign them to any number of collections that you would like.
# Each set of rgbaColorList1 assigned to an object by collection name in the colorList will act like an attribute and create a unique variant of that item.
rgbaColorList1 = [(1,0,0,1),(0,1,0,1),(0,0,1,1),(1,1,1,1),(.5,0,0,1)] 
rgbaColorList2 = [(1,1,0,1),(0,1,1,1),(.5,0,1,1),(.5,1,1,1),(0,.5,0,1)]
# The following color list can be as long or as short as you want it to be.
# To use this all you need to do is place the name of the collection you want colored in the "" and the set of colors you want to apply to it after the :
# The collection named can only contain objects and not sub collections. Every object in the collection will be set to the colors you assigned above for each attribute
colorList = {"Cube_2_0":rgbaColorList1,"Sphere_1_0":rgbaColorList2} 

# The path to Blend_My_NFTs folder:
save_path_mac = '/Users/torrinleonard/Desktop/Blend_My_NFTs'
save_path_windows = r''
# Example mac: /Users/Path/to/Blend_My_NFTs
# Example windows: C:\Users\Path\to\Blend_My_NFTs

# Utilities - DO NOT TOUCH:
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
images_path = save_path + slash + 'NFT_Image_Output'