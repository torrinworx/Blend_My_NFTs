<p align="center">
  <img src="https://user-images.githubusercontent.com/82110564/152652811-e7f7ea86-d7a8-4148-8f61-add6a5491e65.png" align="center" />
  <h1 align="center">Blend_My_NFTs</h1>
</p>
<p align="center">
<a href="https://twitter.com/LeonardTorrin" rel="nofollow"><img src="https://img.shields.io/badge/created%20by-@LeonardTorrin-4BBAAB.svg" alt="Created by Torrin Leonard"></a>
<a href="https://www.gnu.org/licenses/gpl-3.0.en.html" rel="nofollow"><img src="https://img.shields.io/badge/license-GPL%20v3.0-brightgreen" alt="License"></a>
<a href="https://www.paypal.com/paypalme/TorrinLeonard" rel="nofollow"><img src="https://img.shields.io/badge/donate-PayPal-blue" alt="Donate"></a>
<a href="" rel="nofollow"><img src="https://img.shields.io/github/stars/torrinworx/blend_my_nfts" alt="stars"></a>
<a href="" rel="nofollow"><img src="https://visitor-badge.glitch.me/badge?page_id=torrinworx.Blend_My_NFTs" alt=""></a>
</p>

## Description
Blend_My_NFTs is an open source, free to use Blender add on that enables you to automatically generate thousands of 3D Models, Animations, and Images. This add on's primary purpose is to aid in the creation of large generative 3D NFT collections. 

For support, help, and questions, please join our wonderful Discord community: https://discord.gg/UpZt5Un57t 

Checkout the newest tutorial on YouTube that goes along with this documentation: https://www.youtube.com/watch?v=SwU4iVy1XpU

This add on was developed to create the This Cozy Place NFT project which is now availabe to mint on [ThisCozyStudio.com](https://thiscozystudio.com/)


https://user-images.githubusercontent.com/82110564/147833465-965be08b-ca5f-47ba-a159-b92ff775ee14.mov

The video above illustrates the first 10 Cozy Place NFTs generated with Blend_My_NFts.


## Official Links: 

Website: https://thiscozystudio.com/

Discord: https://discord.gg/UpZt5Un57t

Youtube: https://www.youtube.com/c/ThisCozyStudio

Twitter: https://twitter.com/ThisCozyStudio

Instagram: https://www.instagram.com/this_cozy_studio/

Reddit: https://www.reddit.com/r/ThisCozyPlace/


## Case Studies
This document has a list of projects that use Blend_My_NFTs to help facilitate them in the creation of their collection: 
https://docs.google.com/document/d/e/2PACX-1vSHZS4GRu8xXDYpVPEaxyBeTzms9yrJEC9IoAcP38_U8x0C1kVrbtNZgh0zUmkzBoZQVwNvBf3ldRij/pub


## Donations

Blend_My_NFTs, this readme documentation, YouTube tutorials, live stream Q/As, and the Discord community are all provided for free by This Cozy Studio for anyone to use and access. We only ask in return that you credit this software and kindly share what our team has built. A direct link to the Blend_My_NFTs Github page on your projects website (or equivalent social platform) would suffice. We ask you to share this tool because we feel there are many out there that would benefit from it, our only goal is to help those in need. It warms our hearts that so many people use this add-on.

Any donations to the following methods will be put towards developing Blend_My_NFTs and future related Metaverse/Blockchain projects. This Cozy Studio has big plans for Blend_My_NFTs in 2022 and we value your support! 

  - PayPal: https://www.paypal.com/paypalme/TorrinLeonard

Crypto Addresses: 

  - Cardano: `addr1qxzuqz0c32ucga8amwk53unt7vhyf56q73x55aec2lm8esv9cqyl3z4es360mkadfrexhuewgnf5pazdffmns4lk0nqsfylz24`

  - Solana: `A7NuHB79DKfkdZMvqVzBrYN4NXRqP7LVFjMdVoKRfVmo`

  - Ethereum: `0x335408858ce319Cb411090792Ba4BCEE6a2d10CB`

  - USDC (ETH Network): `0x335408858ce319Cb411090792Ba4BCEE6a2d10CB`

We at This Cozy Studio really appreciate all the support our community has given us, you push us forward and inspire us to accomplish great things. We are nothing without you. 

Thank you, 

- This Cozy Studio team

## Quick Disclaimer
Blend_My_NFTs works with Blender 3.0.0 on Windows 10 or macOS Big Sur 11.6. Linux is supported, however I haven't had the chance to test this functionality and guarantee this. Any rendering engine works; Cycles, Eevee, and Octane have all been used by the community without issue. This add-on only works in Blender, a Cinema 4D port will be investigated in the future.

## Example Files
The YouTube tutorials use three different .blend example files. This repository has all three and includes a readme.md file that outlines which videos use which files and by what date: https://github.com/torrinworx/BMNFTs_Examples

## Table of Contents 

- [Blend_My_NFTs](#blend_my_nfts)
  - [Description](#description)
  - [Official Links](#official-links)
  - [Case Studies](#case-studies)
  - [Donations](#donations)
  - [Quick Disclaimer](#quick-disclaimer)
  - [Example Files](#example-files)
  - [Table of Contents](#table-of-contents)
- [Setup and Installation](#setup-and-installation)
- [Important Terminology](#important-terminology)
- [Blender File Organization and Structure](#blender-file-organization-and-structure)
  - [Example of Proper BMNFTs Compatable Blender Scene](#example-of-proper-bmnfts-compatable-blender-scene)
- [Steps to Generate NFTs](#steps-to-generate-nfts)
  - [Step 1. Create NFT Data](#step-1---create-nft-data)
  - [Step 2. Generating NFTs](#step-2---generate-nfts)
  - [Step 3. Refactor Batches & Create MetaData](#step-3---refactor-batches--create-metadata)
- [Custom Metadata Fields](#custom-metadata-fields)
  - [Custom Fields Schema](#custom-fields-schema)
- [Logic](#logic)
  - [Logic JSON Schema](#logic-json-schema)
    - [Schema Definition](#schema-definition)
    - [Rule Types](#rule-types)
  - [Example Logic.json File](#example-logicjson-file)
    - [Never with, Logic Rule Examples](#never-with-logic-rule-examples)
    - [Only with, Logic Rule Examples](#only-with-logic-rule-examples)
- [Notes on Rarity and Weighted Variants](#notes-on-rarity-and-weighted-variants)
  - [.Blend File Rarity Example](#blend-file-rarity-examples)
  - [More complex Rarity Example](#more-complex-rarity-example)
- [Notes on Meta Data and Standards](#notes-on-meta-data-and-standards)
- [Calculating Maximum Number of NFTs (Max Combinations)](#calculating-maximum-number-of-nfts-max-combinations)
- [I have my NFTs, what next?](#i-have-my-nfts-what-next)
- [Running Blend_My_NFTs Headlessly](#running-blend_my_nfts-headlessly)


# Setup and Installation

Here are the steps you need to take to get the Blend_My_NFTs add-on installed in Blender:

1. Click the green `Code` button at the top of this page.

<img width="328" alt="Screen Shot 2022-02-03 at 4 53 16 PM" src="https://user-images.githubusercontent.com/82110564/152435516-bf49bec3-a00f-4c3f-b632-cdf8028d64c8.png">

2. From the drop down click `Download ZIP`. This will download Blend_My_NFTs-main.zip to your Downloads folder:

<img width="397" alt="Screen Shot 2022-02-03 at 5 17 21 PM" src="https://user-images.githubusercontent.com/82110564/152438471-060f7af7-0624-42be-943a-57bb44b02482.png">

3. Move the Blend_My_NFTs-main.zip file to your desktop:

![Screen Shot 2022-02-03 at 4 57 02 PM](https://user-images.githubusercontent.com/82110564/152436030-bccf33ca-25d4-45f7-997a-89bf2ac858e4.png)

4. Open Blender and navigate to `Edit` -> `Preferences` -> `Add-ons`:

<img width="466" alt="Screen Shot 2022-02-03 at 5 00 27 PM" src="https://user-images.githubusercontent.com/82110564/152436377-b042234e-a791-4e2a-8ffa-f3694d819b4b.png">

<img width="666" alt="Screen Shot 2022-02-03 at 5 00 43 PM" src="https://user-images.githubusercontent.com/82110564/152436410-e02fe611-49b1-45e8-a1b8-336b67e9ecd4.png">

5. Click the `Install` button: 

![Screen Shot 2022-02-03 at 5 05 08 PM](https://user-images.githubusercontent.com/82110564/152436908-8f7d5d8f-eb9c-431f-8ca1-c9a022b1b4eb.png)

6. In the `Blender File View` window, navigate to the Blend_My_NFTs-main.zip file downloaded in step 1., select it, then click `Install Add-on`:

![Screen Shot 2022-02-03 at 5 07 16 PM](https://user-images.githubusercontent.com/82110564/152438040-513222ea-8297-4771-8bf3-3b6af74bb54b.png)


7. Navigate back to the `Add-ons` window in step 4., and search for Blend_My_NFTs:

![Screen Shot 2022-02-03 at 5 02 59 PM](https://user-images.githubusercontent.com/82110564/152436664-e8e135e5-2d36-487a-bf43-4ea200210a4c.png)

8. Click the `Checkbox` to enable the Blend_My_NFTs add-on:

![Screen Shot 2022-02-03 at 5 22 43 PM 1](https://user-images.githubusercontent.com/82110564/152439275-c590db7a-8b5c-48a4-96f5-ac1ce372be38.png)


Now that Blend_My_NFTs is installed in your instance of Blender you can find the main panel in the `3D View` tab in `Layout`, once you are there tap `N` on your keyboard to open the side panel:

![Screen Shot 2022-02-03 at 5 27 41 PM](https://user-images.githubusercontent.com/82110564/152439730-21da93e3-6816-419a-b9d8-5b146dfe3e6e.png)


# Important Terminology

Before you can continue further, there are terms used in this documenation to describe the process of this software. This makes it easier to understand how you need to organize your .blend file to generate NFTs. Refer to this section if you come accross an unfamiliar term. 

Let's say you are creating an NFT collection, the artwork is a .png of a person wearing a hat:

1. ``Attribute`` - A part of the .png that can be changed. The idea of a `Hat` on a man is an Attribute, there are many types of Hats, but the `Hat` itself I will refer to it as an Attribute.

2. ``Variants`` - These are the types of Hats; Red Hat, Blue Hat, Green Hat, Cat Hat, etc. These can be swapped into the `Hat` Attribute to create unique .png NFTs.

3. ``DNA`` - A sequence of numbers that determins what ``Variant`` from every ``Attribute`` to include in a single NFT .png. Blend_My_NFTs creates and stores a uniqe DNA sequence for each NFT you create. These numbers are stored in the ``NFTRecord``.

4. ``NFTRecord`` - The "Ledger" of all ``DNA`` for your NFT collection. This will be generated after you create all the Attribtues and Variants that make up your NFT collection in Blender.

5. ``Batch`` - A randomly selected subset of ``DNA``, taken from the ``NFTRecord``. Blend_My_NFTs can split the ``NFTRecord`` into multiple Batches; This allows you to render or create NFTs on multiple computers, or at seperate instances in time.


# Blender File Organization and Structure
**Important** - Every object, model, texture, camera, light etc. must be in the same .blend file! If you have mulitiple .blend files, Blend_My_NFTs is unable to open and process them. It's recommended to keep your file's total size 5gb, so if you have multiple files created already, reduce the size and then merge them to a master file. 

Organizing your NFTs Attributes and Varariants in Blender is essential to generate files with Blend_My_NFTs. Follow the organizational rules below when making your NFT .blend file: 

1. Your .blend file scene must contain a `Script_Ignore` collection. Make sure the name is exactly `Script_Ignore`, include the underscore and capitalization. 
  -  Any objects (Lights, Cameras, Background images, etc.) that stay constant throughout every NFT file are to be placed in this `Script_Ignore` collection. `Script_Ignore` may contain sub collections and all naming conventions are not required withing this collection.
2. Every Attribute is represented by a collection placed directly in the Scene collection. The name of these attribute collections **can not** contain numbers or the underscore (`_`) symbol. The name can contain spaces

3. Every Variant of each Attribute is represented by a collection. These collections are to be placed in the corresponding Attribute colleciton. The naming convention of these Variant collections is as follows:
  - <`Name of Variant`>`_`<`Order Number`>`_`<`Rarity Percentage`>
    - `Name of Variant` ==> Any string/number/symbol combination, must not include the underscore (`_`) symbol. Can contain spaces. 
    - `Order Number` ==> An incrementing number. Must increment for each Variant added to a given Attribute starting at `1`, numbers cannot repeat and must be unique for each Variant. Can only be in a single number format, do not use 001 or 0001 formats.
    - `Rarity Percentage` ==> A percentage that determins the chance that the given variant will be selected. Must be a number, can contain decimals, cannot contain the percentage (`%`) symbol. See `Notes on Rarity and Weighted Variants` section for more details.
  - Each Variant collection can contain everything that makes up an individual Variant; it can contain objects, lights, meshes, planes, and every other object type.

## Example of Proper BMNFTs Compatable Blender Scene
<img width="527" alt="Screen Shot 2022-02-06 at 5 40 39 PM" src="https://user-images.githubusercontent.com/82110564/152704567-378ee98f-34a7-4cd7-8f62-441b7e1891b0.png">

In this example, notice how the main components in `Script_Ignore` can be any type of object. The collections `Body` and `Arms` are both Attribute collections; `Silver Body_1_75` and `Gold Body_2_25` are Variants of the `Body` Attribute, and have a 75% and 25% generation chance. `Silver Arms_1_75` and `Gold Arms_2_25` are Variants of the `Arm` Attribute and have the same weighted distribution as the `Body` Variants. Notice how the Variant collections in the `Arm` Attribute can contain more than one object and object type, this principle can be applied to any Variant collections.

This repository contains three .blend example files that are compatable with Blend_My_NFTs: https://github.com/torrinworx/BMNFTs_Examples


# Steps to Generate NFTs

After you have formatted and organized your NFT collection in Blender to the rules outlined above in [Blender File Organization and Structure
](#blender-file-organization-and-structure) you can now go about generating your NFT collection. By the end of this process you will have a folder continaing the following: 

1. NFT media files; images, animations, or 3D models in any format that you specify.
2. Json metadata files; one fore each NFT content filem, formatted to the blockchain standard that you set. 

Before you get started, open the .blend of your NFT collection and open the side panel of the `Layout` tab so that Blend_My_NFTs is visible: 

<img width="1440" alt="Screen Shot 2022-02-06 at 9 53 29 PM" src="https://user-images.githubusercontent.com/82110564/152717227-5c0f430e-5d35-452f-b593-28569a144064.png">

Each Step below is represented by one panel; everything you have to do for that one step, is in the corosponding panel in Blend_My_NFTs. 

## Step 1. - Create NFT Data

Blend_My_NFTs needs data to understand your .blend file, in this step you will create that data. 

1. Isolate or open the `Create NFT Data` panel in Blend_My_NFTs:

<img width="463" alt="Screen Shot 2022-02-06 at 9 56 12 PM" src="https://user-images.githubusercontent.com/82110564/152717434-92fa39a9-6f3a-4a43-b755-95b7c082c35c.png">

2. Set the name of your NFT collection in the `NFT Name:` text field:

<img width="429" alt="Screen Shot 2022-02-06 at 10 01 19 PM" src="https://user-images.githubusercontent.com/82110564/152717855-078fed04-ab77-4362-95de-f7af12cc01d0.png">

This name will be in the metadata and in the name of each NFT content file. 

3. Note - `Maximum Number Of NFTs: ###` is the maximum number of NFTs your collection can contain with it's current number of Attirbutes and Variants.

<img width="420" alt="Screen Shot 2022-02-06 at 9 59 42 PM" src="https://user-images.githubusercontent.com/82110564/152717757-ea58e112-a79e-43c1-b91a-49acf23b7662.png">

4. Note - `Recommended Limit: ##` is the recommended number of NFTs Blend_My_NFTs is able to generate. Higher than this, e.i. closer to `Maximum Number of NFTs` can result it loss of NFT count and weighted Variants not appear as often as you expect them to. It is recommended that you keep your `NFT Collection Size` below this number.

<img width="382" alt="Screen Shot 2022-03-13 at 5 30 31 PM" src="https://user-images.githubusercontent.com/82110564/158080032-6e48fb2e-2d41-4224-b108-02035cf20246.png">

5. Set your NFT collection size with the `NFT Collection Size` field:

<img width="421" alt="Screen Shot 2022-02-06 at 10 03 46 PM" src="https://user-images.githubusercontent.com/82110564/152718041-a7043edc-56bf-41ba-bbee-4b439b648e46.png">

**Important:** This number must be greater than 0 and less than `Maximum Number Of NFTs` shown at the top of the `Create NFT Data` panel. 

6. Set the NFTs per batch with the `NFTs Per Batch` field:

<img width="368" alt="Screen Shot 2022-03-13 at 5 34 09 PM" src="https://user-images.githubusercontent.com/82110564/158080174-b19c2fc7-af0c-4c05-8987-8f518f384850.png">

**Important:** This number must be greater than 0 and less than or equal to `Maximum Number Of NFTs` shown at the top of the `Create NFT Data` panel. 


7. Set the `Save Path` of your `Blend_My_NFTs Output` folder by clicking on the file icon and navigating to a directory: 

<img width="418" alt="Screen Shot 2022-02-06 at 10 04 43 PM" src="https://user-images.githubusercontent.com/82110564/152718246-a52cb8ce-9af3-480c-ae82-aa665196b6e6.png">

Then click the `Accept` button. 

Desktop is recommended for easy access, but any directory will do. 

8. Enable or Disable Rarity and Weighted Variants with the checkbox `Enable Rarity`. For more information on what affect this has on your NFT collection, see [Blender File Organization and Structure](#blender-file-organization-and-structure)and [Notes on Rarity and Weighted Variants](#notes-on-rarity-and-weighted-variants). 

<img width="428" alt="Screen Shot 2022-02-06 at 10 10 55 PM" src="https://user-images.githubusercontent.com/82110564/152718643-d1580692-eac4-47bf-a41a-0e4748517b0d.png">

9. Enable or Disable Logic with the checkbox `Enable Logic`. For more information on what affect this has on your NFT collection, see [Logic](#logic).

<img width="380" alt="Screen Shot 2022-03-13 at 5 37 02 PM" src="https://user-images.githubusercontent.com/82110564/158080236-318135ab-a87c-40bf-b9d7-2bd9a70653e8.png">

  - If you enabled Logic, set the location of the Logic.json file you created in the ``Logic File`` field. Click on the file icon and navigate to the location of the json file. To create a Logic.json file, see the [Logic](#logic) section. 

10. Lastly click the `Create Data` button:

<img width="425" alt="Screen Shot 2022-02-06 at 10 12 37 PM" src="https://user-images.githubusercontent.com/82110564/152718783-8ee0d72a-9223-4168-9664-c55b9cb6d84f.png">

After completeing the `Create NFT Data` step, you should have the following files and folders located at the `Save Path` set in step 6. above; 

- `Blend_My_NFTs Outuput` folder. A directory that contains all output files from Blend_My_NFTs. 
  - `NFT_Data` folder. This contains the following `NFTRecord.json` and `Batch#.json` files. 
    - `NFTRecord.json` file. A ledger that contains the NFT DNA of your collection.
    - `Batch_Data` folder. Contains all `Batch#.json files`. 
      - `Batch#.json` files. Smaller chuncks of the `NFTRecord.json` that contain unique DNA.
  - `Generated NFTs` folder. This directory will be empty, but is where your NFT content files will be exported to. once you've completed [Step 2. Generate NFTs](#step-2---generate-nfts).

## Step 2. - Generate NFTs

In this step, you will select the types of NFT content files you wish to generate, as well as the formats you want them in. You will then generate these files in batches, or all at once. 

1. Isolate or open the `Generate NFTs` panel in Blend_My_NFTs:

<img width="429" alt="Screen Shot 2022-02-06 at 10 22 35 PM" src="https://user-images.githubusercontent.com/82110564/152719611-541d94e7-5526-4bd5-9c22-7aa1a885d16b.png">

2. Check the NFT content files you wish to generate (you can select more than one):

<img width="429" alt="Screen Shot 2022-02-06 at 10 37 42 PM" src="https://user-images.githubusercontent.com/82110564/152720692-130cbb34-a2f7-44c3-b517-9f93b26d20d1.png">

- If you check `Image`, choose the file format you want the NFT content files to be exported as from the `Image drop-down`: 

<img width="422" alt="Screen Shot 2022-02-06 at 10 55 28 PM" src="https://user-images.githubusercontent.com/82110564/152722173-9cf2f6aa-334c-4a3d-ae01-fc8edae15428.png">

  - `.png` --> Exports image as .png
  - `.jpeg` --> Exports image as .jpeg
 

- If you check `Animation`, choose the file format you want the NFT content files to be exported as from the `Animation drop-down`:

<img width="443" alt="Screen Shot 2022-02-06 at 10 47 49 PM" src="https://user-images.githubusercontent.com/82110564/152722010-258d479a-1168-41d5-840b-8a11ef58a15e.png">

  - `.avi (AVI_JPEG)` --> Exports animations in AVI_JPEG encoding to .avi file format. See [Blender API](https://docs.blender.org/api/current/bpy.types.Image.html#bpy.types.Image.file_format) for more information.
  - `.avi (AVI_RAW)` --> Exports animations in AVI_RAW encoding to .avi file format. See [Blender API](https://docs.blender.org/api/current/bpy.types.Image.html#bpy.types.Image.file_format) for more information.
  - `.mkv (FFMPEG)` --> Exports animations in FFMPEG Blender default encoding and container to .mkv file format. See [Blender API](https://docs.blender.org/api/current/bpy.types.Image.html#bpy.types.Image.file_format) for more information.


- If you check `3D Model`, choose the file format you want the NFT content files to be exported as from the `3D Model drop-down`: 

<img width="443" alt="Screen Shot 2022-02-06 at 10 40 10 PM" src="https://user-images.githubusercontent.com/82110564/152720946-3b17a8cb-28be-4c7e-84d1-4479188e2da8.png">

  - `.glb` --> Exports .glb 3D models
  - `.gltf + .bin + textures` --> Exports .gltf 3D models with seperated textures
  - `.gltf` --> Exports .gltf 3D models with embeded textures
  - `.fbx` --> Exports .fbx 3D models
  - `.obj` --> Exports .obj 3D models
  - `.x3d` --> Exports .x3d 3D models
  - `.stl` --> Exports .stl 3D models
  - `.vox` --> Exports .vox MagicVoxel 3D models. **Experimental:** This file format is still in development and might not work as intended. **Important:** You must install the [voxwritter Blender add-on](https://github.com/Spyduck/voxwriter) for this feature to work. 

3. Select number of the Batch you wish to generate in the `Batch to Generate` feild:

<img width="423" alt="Screen Shot 2022-02-06 at 10 58 56 PM" src="https://user-images.githubusercontent.com/82110564/152722424-6244f975-955b-4e4f-9314-3725db918a59.png">

4. Click the `Generate NFTs` Button. This will generate the NFT content files from the Batch set in above step 3:

<img width="425" alt="Screen Shot 2022-02-06 at 11 00 11 PM" src="https://user-images.githubusercontent.com/82110564/152722526-72473e53-89fe-4ee3-ab62-e164c871c889.png">

5. To generate the rest of the Batches you have, repeat steps 3. to 4. and increment the `Batch To Generate` number. 


After completeing the `Create NFT Data` step, you should have the following files and folders located at the `Save Path` set in [Step 1. Create NFT Data](#step-1---create-nft-data) above;

- `Blend_My_NFTs Outuput` folder. A directory that contains all output files from Blend_My_NFTs. 
  - `NFT_Data` folder. This contains the following `NFTRecord.json` and `Batch#.json` files. 
    - `NFTRecord.json` file. A ledger that contains the NFT DNA of your collection.
    - `Batch_Data` folder. Contains all `Batch#.json files`. 
      - `Batch#.json` files. Smaller chuncks of the `NFTRecord.json` that contain unique DNA.
  - `Generated NFTs` folder. This directory will be empty, but is where your NFT content files will be exported to. once you've completed [Step 2. Generate NFTs](#step-2---generate-nfts).
    - `Batch#.json` folder. There should be one folder for each batch that you generated. 
      - `Image` folder. The folder where all the NFT Image content files are stored for a given `Batch#.json`. 
        - `Image` files. These images will contain have the name you specified in [Step 1. Create Data](#step-1---create-nft-data), an incrementing number, and the file extension you specified above. 
      - `Animation` folder. The folder where all the NFT Animation content files are stored for a given `Btach#.json`. 
        - `Animation` files. These animations will have the name you specified in [Step 1. Create Data](#step-1---create-nft-data), an incrementing number, and the file extension you specified above. 
      - `3D Model` folder. The folder where all the NFT 3D Model content files are stored.
        - `3D Model` files. These 3D models will have the name you specified in [Step 1. Create Data](#step-1---create-nft-data), an incrementing number, and the file extension you specified above. 
      - `BMNFTs_metaData` folder.
        - `Data_#.json` files. These files are used by Blend_My_NFTs backend in [Step 3. - Refactor Batches & Create MetaData](#step-3---refactor-batches--create-metadata). These can be ignored, unless you are customizing the metaData.py script.

## Step 3. - Refactor Batches & Create MetaData

In this step you will combine the batch files created in [Step 2. - Generate NFTs](#step-2---generate-nfts) into one cohesive folder that is ready to be uploaded to the blockchain of your choice. This step will also generate the metadata needed for smart contract minting sites.

This step is to be done after you have completely rendered and generated all of your NFT batches; once you complete this step, you cannot undo the changes. 

1. Isolate or open the `Refactor Batches & Create MetaData` panel in Blend_My_NFTs:

<img width="344" alt="Screen Shot 2022-02-08 at 4 23 32 PM" src="https://user-images.githubusercontent.com/82110564/153078455-3b995cdd-20df-46ca-8c0e-940e49979181.png">

2. Check off the metadata templates you wish to generate (You can create more than one): 

<img width="338" alt="Screen Shot 2022-02-08 at 4 28 19 PM" src="https://user-images.githubusercontent.com/82110564/153078686-6aa555c0-c2f3-4a40-8e3a-cb1588afdf2b.png">

For more information on the metadata generated by Blend_My_NFTs and the standards that are followed see [Notes on Meta Data and Standards](#notes-on-meta-data-and-standards).

3. For each metadata template standard you can set a description, this will appear in the metadata json file of the given template. 

<img width="512" alt="Screen Shot 2022-03-13 at 5 40 37 PM" src="https://user-images.githubusercontent.com/82110564/158080364-c88e77d1-06f2-47b4-b869-ba66d289117e.png">

4. If you want custom metadata fields, check the `Enable Custom Metadata Fields` checkbox and set `Custom Fields File` to the Custom_Fields.json file you create in the [Custom Metadata Fields](#custom-metadata-fields) section.

5. Click the `Refactor Batches & Create MetaData` button:

<img width="343" alt="Screen Shot 2022-02-08 at 4 32 46 PM" src="https://user-images.githubusercontent.com/82110564/153079285-93ef31af-633a-4d39-bd35-44a4412f3660.png">

6. Confirm you wish to refactor your batches by clicking the `Refactor your Batches?` button in the popup dialogue: 

<img width="456" alt="Screen Shot 2022-02-08 at 4 34 30 PM" src="https://user-images.githubusercontent.com/82110564/153079554-e4a359a6-9ca9-45eb-81a3-6e74c54dd697.png">

After completeing the `Refactor Batches & Create MetaData` step, you should have the following files and folders located at the `Save Path` set in [Step 1. Create NFT Data](#step-1---create-nft-data) above:

- `Blend_My_NFTs Outuput` folder. A directory that contains all output files from Blend_My_NFTs. 
  - `NFT_Data` folder. This contains the following `NFTRecord.json` and `Batch#.json` files. 
    - `NFTRecord.json` file. A ledger that contains the NFT DNA of your collection.
    - `Batch_Data` folder. Contains all `Batch#.json files`. 
      - `Batch#.json` files. Smaller chuncks of the `NFTRecord.json` that contain unique DNA.
  - `Complete_Collection` folder. A refactored version of the `Generated NFTs` folder, with all batches reordered and refactored and generated metadata templates. 
 
    - `Image` folder. The folder where all the NFT Image content files are stored. 
      - `Image` files. These images will contain have the name you specified in [Step 1. Create Data](#step-1---create-nft-data), an incrementing number, and the file extension you specified above. 
    - `Animation` folder. The folder where all the NFT Animation content files are stored. 
      - `Animation` files. These animations will have the name you specified in [Step 1. Create Data](#step-1---create-nft-data), an incrementing number, and the file extension you specified above. 
    - `3D Model` folder. The folder where all the NFT 3D Model content files are stored.
      - `3D Model` files. These 3D models will have the name you specified in [Step 1. Create Data](#step-1---create-nft-data), an incrementing number, and the file extension you specified above. 
    - `BMNFTs_metaData` folder.
      - `Data_#.json` files. These files are used by Blend_My_NFTs backend in [Step 3. - Refactor Batches & Create MetaData](#step-3---refactor-batches--create-metadata). These can be ignored, unless you are customizing the metaData.py script.
    - `Cardano_metaData` folder; will appear if specified in Step 2. above.
      - `Cardano_Data_#.json` files. Will contain metadata template in Cardano CIP 25 format. 
    - `Solana_metaData` folder; will appear if specified in step 2. above.
      - `Solana_Data_#.json` files. Will contain metadata template in Solana Metaplex format. 
    - `ERC721_metaData` folder; will appear if specified in Step 2. above.
      - `Erc721_Data_#.json` files. Will contain metadata template in ERC721 format. 


Congratulations!! You now have a complete 3D NFT collection that is ready to upload to the blockchain of your choice!

# Custom Metadata Fields
This section will cover how to implement custom metadata fields. The method is the same for the Cardano CIP-25, Solana, and ERC721 standards. 

These fields are determined by a .json file that you manually create. For the pruposes of this documentation, just think of JSON as a text file (.txt) that we can use to store information. You can name this file anything, but for this tutorial lets call it `Custom_Fields.json`.

If you need help creating a JSON file, checkout this tutorial: [How to Create JSON File?](https://codebeautify.org/blog/how-to-create-json-file/)

To learn more about JSON files and how to structure data read this article: [Working with JSON](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON)

## Custom Fields Schema
If you'd like, copy and paste this template into the JSON file you created above: 

```
{
  "<item 1>": "<content of item 1>", 
  "<item 2>": "<content of item 2>", 
  "<item 3>": "<content of item 3>", 
  "<item 4>": "<content of item 4>"
  ...
}
```

Each item in this dictionary will be sent to the attributes feild of a given metadata standard. For example, this is what a Cardano template would look like once these fields are applied:

```
{
 "721": {
  "<policy_id>": {
   "Logic Test_1": {
    "name": "Logic Test_1",
    "image": "",
    "mediaType": "",
    "description": "",
    "Cube": "Red Cube",
    "Sphere": "Red Sphere",
    "<item 1>": "<content of item 1>", 
    "<item 2>": "<content of item 2>", 
    "<item 3>": "<content of item 3>", 
    "<item 4>": "<content of item 4>"
   }
  },
  "version": "1.0"
 }
}
```

# Logic 

This section will go over the process of creating and using rules for your NFT collection, we will refer to this process as Logic.

Logic is deterimened by a .json file that you manually create. For the purposes of this documentation, just think of JSON as a text file (.txt) that we can use to store information. You can name this file anything, but for this tutorial lets call it `Logic.json`.

If you need help creating a JSON file, checkout this tutorial: [How to Create JSON File?](https://codebeautify.org/blog/how-to-create-json-file/)

To learn more about JSON files and how to structure data read this article: [Working with JSON](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON)

## Logic JSON Schema
If you'd like, copy and paste this template into the JSON file you created above:

```
{
    "Rule-1":{
        "Items-1": [
            "<collection name>"
        ],
        "Rule-Type": "<rule type>", 
        "Items-2":[
            "<collection name>"
        ]
    },
    "Rule-2":{
        "Items-1": [
            "<collection name>"
        ],
        "Rule-Type": "<rule type>", 
        "Items-2":[
            "<collection name>"
        ]
    }
}
```

### Schema Definition
- ``Rule-#`` A dictionary representing the information of a single defined Rule of an NFT collection. There can be as many as you choose. Increment the ``#`` when you create a new rule.
- ``Items-1`` A list of strings representing the names of Attribute(s) or Variant(s).
- ``Rule-Type`` The rule that governs the relation between ``Items-1`` and ``Items-2``. Has two possible values: ``Never with`` and ``Only with``.
- ``Items-2`` A list of strings representing the names of Attribute(s) or Variant(s).

### Rule Types
There are two rule types:
- ``Never with`` --> If selected, ``Items-1`` will never appear if ``Items-2`` are selected. For each NFT DNA that is generated, either ``Items-1`` or ``Items-2`` are randomly selected. That selected ``Items List`` is then acted upon depending on if the items in the list are Attributes or Variants: 
  - If ``Items List`` contains complete Attribute(s), those Attribute(s) will be set to Empty automatically.
  - If ``Items List`` contains Variant(s), the other Variants in that Variants Attribute will be randomly or weightedly selected depending on if you have ``Enable Rarity`` selected when you create NFT data.
 
- ``Only with`` --> If selected, ``Items-1`` will only appear if ``Items-2`` are selected. If ``Items-1`` contains complete Attribute(s), those Attribute(s) will be set to Empty automatically. Meaning they will not appear if you export images, animations, or 3D models.

- ``Always with`` --> If selected, ``Items-1`` will always appear if ``Items-2`` are selected.``Items-1`` CANNOT contain complete Attribute(s) and is limited to single Variants. The list can contain multiple Variants, however they must be from seperate Attributes.

The best way to understand how Logic works is to think of it as a sentence, example: ``"Items-1 Never goes with Items-2"`` or ``"Items-1 Only goes with Items-2"``.

**Important:** The more rules you add the higher the chance a rule conflict may arise, and you may see Attribute and Variant behaviour that you do not desire. 

## Example Logic.json File
Say we have the following scene in a .blend file: 
<img width="420" alt="Screen Shot 2022-03-13 at 4 21 52 PM" src="https://user-images.githubusercontent.com/82110564/158077693-86f961cf-c121-4d0e-8a84-1d6a39e7cafc.png">
Note that we have two Attributes, ``Cube`` and ``Sphere``, and that they have 4 Variants. If you'd like to follow along with this example I'd recommend downloading the [Logic_Example.blend](https://github.com/torrinworx/BMNFTs_Examples/blob/main/Logic_Example.blend).

### Never with, Logic Rule Examples
- **Never with, Variants example:**
  In this example, the Variant ``Red Cube_1_25`` never appears with ``Red Sphere_1_25``:
  ```
  {
    "Rule-1":{
        "Items-1": [
            "Red Cube_1_25"
        ],
        "Rule-Type": "Never with", 
        "Items-2":[
            "Red Sphere_1_25"
        ]
    }
   }
  ```
  

- **Never with, Attributes example:**
  In this example, the Attribute ``Cube`` never appears with ``Red Sphere_1_25``. When ``Red Sphere_1_25`` is selected, no Variants in the Cube Attribute are selected, and hence the Attribute is set to "Empty": 
  ```
  {
    "Rule-1":{
        "Items-1": [
            "Cube"
        ],
        "Rule-Type": "Never with", 
        "Items-2":[
            "Red Sphere_1_25"
        ]
    }
   }
  ```

### Only with, Logic Rule Examples
- **Only with, Variants example:**
  In this example, the Variant ``Red Cube_1_25`` only appears with ``Red Sphere_1_25``:
  ```
  {
    "Rule-1":{
        "Items-1": [
            "Red Cube_1_25"
        ],
        "Rule-Type": "Only with", 
        "Items-2":[
            "Red Sphere_1_25"
        ]
    }
   }
  ```

- **Only with, Attributes example:**
  In this example, the Attribute ``Cube`` only appears with ``Red Sphere_1_25``:
  ```
  {
    "Rule-1":{
        "Items-1": [
            "Cube"
        ],
        "Rule-Type": "Never with", 
        "Items-2":[
            "Red Sphere_1_25"
        ]
    }
   }
  ```

Now that you have a completed Logic.json file, you can now go back and complete [Step 1. Create Data](#step-1---create-nft-data)!


# Common Issues and Problems

- The most common issues people face are naming convention issues (See [Blender File Organization and Structure](#blender-file-organization-and-structure)). People often miss the naming convention on one or two collections and this typically throws up an error. The best way to resolve this is by reviewing the Blender File Organization and Structure standards and go through each collection in your Blender scene.

- Remember that each Attribute and each Variant are represented by a `collection` if this is not the case your `Max Number of NFTs` will be a negative number or 0.

- If you make **ANY** changes to your Blender scene, you need to [re-Create NFT Data](#step-1---create-nft-data), otherwise Blend_My_NFTs wont be able to recognize the changes. 


# Notes on Rarity and Weighted Variants

Rarity is a percentage value and accepts fractions like 0.001%, but they must be specified with decimals in the naming (fraction like 1/2 or 3/5 are not permitted in the naming structure). For ease of use the percentages should add up to 100%:

```
33% + 33% + 33% + 1% = 100% 

Variant 1 = 33% chance
Variant 2 = 33% chance
Variant 3 = 33% chance
Variant 4 = 1% chance
```

If you have 20 variants with 50 set as the rarity percentage for each, Blend_My_NFTs will add up the percentages then treat the sum as 100%:

```
50% + 50% + 50% + 50% + 50%....
= 1,000%

Out of 100%:

(50/1,000)*100 = 5% chance of 1 variant
```

Rarity is dependent on both the number of NFTs you generate, as well as the maximum number of possible combinations of the Attributes and Variants in your .blend file. 

This results in the following two scenarios, say, at a fixed number of 10,000 NFTs to generate;

1. Your .blend file has 1,000,000,000 possible combinations (trust me that's a small number, our collection for This Cozy Place has over 11 Trillion possible combinations). Generating 10,000 will be more representative of the rarity numbers you set as the script will simply have more combinations to choose from.

2. Your .blend file has 10,000 possible combinations. This means all possible combinations of your NFT will be generated, meaning that no rarity can be taken into account.

This happens for the following reasons:

1. The rarity is determined pseudo randomly, but is weighted based on each Variants rarity percentage.

2. The scripts generally prioritize the number of NFTs to generate (`maxNFTs`) over rarity percentage

This behaviour is a fundamental mathematical result, not an issue with the code. I've researched various ways of creating and enforcing rarity, this is the only way I have found that works. If you have found a better method, feel free to make a pull request explaining it and I'd be happy to review and merge it to the main Github repo for BMNFTs.

## .blend file Rarity examples: 

1. With Rarity percentage (50% 50% split)
```
  Hat <-- Attribute
  |-Green Hat_1_50
  |-Red Hat_2_50
```

2. Since it's 50/50 it can also be expressed like this: 
```
  Hat <-- Attribute
  |-Green Hat_1_0
  |-Red Hat_2_0
```

Leaving the rarity number as 0 will randomly select 1 of the variants you set in your .blend file. Note that this only works if every variant's rarity is set to 0. For an attribute its rarity or random, not both. You can have different attributes, where some are using rarity and others are randomly selected, but you cannot mix these with variants of one attribute. 

### More complex Rarity Example: 

```
  Hat <-- Attribute
  |-Green Hat_1_24.75
  |-Red Hat_2_24.75
  |-Blue Hat_2_24.75
  |-Orange Hat_2_24.57
  |-Purple Hat_2_0.5
  |-Yellow Hat_2_0.5
```

In the example above, Green, Red, Blue, and Orange hats all have an equal chance of getting selected. However Purple and Yellow hats will only appear on average 0.5% of the time. We recommend rounding to about 5 decimal places for simplicity, as numbers of more accuracy aren't really needed for NFT collections 10,000 or smaller.

The code that determines rarity can be found the `Rarity_Sorter.py`.

## Calculating Maximum Number of NFTs (Max Combinations)

Mutliply the number of Variants in each Attribute by each other. 

### Example:

<img width="527" alt="Screen Shot 2022-02-06 at 5 40 39 PM" src="https://user-images.githubusercontent.com/82110564/152704567-378ee98f-34a7-4cd7-8f62-441b7e1891b0.png">

In the image above there are two `Attributes`; `Body`, and `Arms`. Each attribute has 2 `Variants`, so in order to find the Maximum Number of NFTs we do the following: 

```
Number of Variants in Arm Attribute = 2 
Number of Variants in Body Attribute = 2 

(Number of Variants in Arm Attribute)*(Number of Variants in Body Attribute) = Maximum Number of NFTs

2*2 = 4

∴ The Maximum Number of NFTs is 4
```

The formula for this equation can be simplified to the following: 


N <sub>1</sub> *N <sub>2</sub> *N <sub>3</sub> *... = Max <sub>NFTs</sub>



## Notes on Meta Data and Standards

Blend_My_NFTs can export Cardano, Solana, and ERC721 formatted metadata templates. After running `Refactor Batches & Create MetaData` a template will be generated for each NFT you have created; These templates will include properly formated names for each Attribute and Variant that was selected to create that NFT. 

Blend_My_NFTs can only provide this information in the templates, you will have to add Policy ID and URL when you upload and mint your NFT collection. For more information on how to do this see [I have my NFTs, what next?](#i-have-my-nfts-what-next)

### Meta Data Template Sources

The list of meta data standard sources used to create the templates: 

- `Cardano CIP25` --> https://cips.cardano.org/cips/cip25/
- `Solana Metaplex` --> https://docs.metaplex.com/token-metadata/specification
- `ERC721` --> https://docs.opensea.io/docs/metadata-standards

The Blend_My_NFTs code implementation for the above standards can be found in `main>metaData.py`.

### Meta Data Disclaimer
These meta data templates are based on the common standards for the given blockchain, you will have to modify and fill them in with a script of your own when you mint your NFT collection. These metadata templates are only provided for your convenience and are as accurate to the standards above that I could make them.


## I have my NFTs, what next? 

### Bulk file renaming

OpenSea and other NFT marketplaces and tools might require a specific naming convention for NFT media and metadata files. Blend_My_NFTs doesn't currently follow these file naming conventions, but this will be added in a future version. For now, the best no code workaround is to use a bulk file renamer suggested by `itachimoonshot | Kaavan Labs` in the This Cozy Studio Discord server: 

[Microsoft Power Toys - Power Rename](https://docs.microsoft.com/en-us/windows/powertoys/#powerrename)


## Running Blend_My_NFTs Headlessly

If you are working with Blender in an environment where you can't use the user interface to change settings within the addon, such as Google Colab, you can instead pass in a config file containing the settings from your local instance.

In order to generate this config file, you can use the `Export BMNFT settings to a file` button.
![image](https://user-images.githubusercontent.com/16054364/162890685-142ebefe-9ec1-4ff9-9f28-60e800345444.png)
This file will be saved in the folder indicated by the `Save Path` field.

Once you have this config file, you can run this addon in Blender headlessly by running this command from the directory of your Blender installation:

On Windows
```
.\blender.exe --background <path to your .blend file> --python <path to Blend_My_NFTs __init__.py> -- --config-file <path to the generated config.cfg> --operation create-dna
```

On Linux
```
./blender --background <path to your .blend file> --python <Path to Blend_My_NFTs __init__.py> -- --config-file <path to the generated config.cfg> --operation create-dna
```

There are two mandatory arguments that you need to run this script from the terminal/command line:
  - Config file location
    
    This argument tells Blend_My_NFTs where to find your `config.cfg` file in order to load your desired settings.
    
    `--config-file`
  - Operation
    
    This argument tells Blend_My_NFTs which operation you want to perform.
    
    `--operation` with one of the following three options afterwards:
    ```
    create-dna
    generate-nfts
    refactor-batches
    ```

There are also additional optional arguments that you can use:
  - Change Save Location
    
    This argument takes priority over the save path indicated in `config.cfg`.
    
    `--save-path`
   
  - Change Batch Number
    
    This argument takes priority over the batch number specified in `config.cfg`.
    
    `--batch-number`
    
  - Use Batch Data in a non standard location
  
    Use batch data from a separate folder rather than the folder Blend My NFTs uses by default.
    
    `--batch-data`

You can also view this information from your terminal/command line by running:

On Windows
```
.\blender.exe --background --python <path to Blend_My_NFTs __init__.py> -- --help
```

On Linux
```
./blender --background --python <Path to Blend_My_NFTs __init__.py> -- --help
```

It is important that you place the python arguments after the `--` because of how blender parses arguments from the command line. More info about blender command line arguments can be found [here](https://docs.blender.org/manual/en/3.0/advanced/command_line/arguments.html).

More coming soon...

