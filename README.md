# Blend_My_NFTs

**This tutorial page is not finished! I don't know how long it will take to make this page, but I'm still working on it. This page will be updated as I commit/merge new changes to the main branch. (Last updated Nov 6th, 2021)** 

## Description

Blend_My_NFTs is a work-in-progress Blender add on that can automatically generate thousands of images or 3D objects that can be used to create NFTs. It is bing developed to create the NFT project This Cozy Place. This Cozy Place will be an NFT image collection with a total of 10000 unique NFTs all rendered in Blender via Blend_My_NFTs. If you would like to learn more about Blend_My_NFTs or This Cozy Place, please visit our discord server: https://discord.gg/UpZt5Un57t 


## Disclaimer

Nothing in this repository is financial advice. Create an NFT project/collection at your own risk, we are simply providing a means of acomplishing a goal, not investment/financial information about that goal. Do your own research before spending money on NFTs or any asset for that matter. 

I do not garuntee this software will work with your setup. There are many variables and factors that go into running the software provided, it differs from system to system, and from blend file to blend file.

I encourage you to do some trouble shooting, read the Blender API documentation, read this tutorial, review the scripts, and do your own research before reaching out for help on our discord. If you are really stuck and are out of options I am available on our disord channel above for consulting. However! I am not a toutor. Although I enjoy teaching people, I simply do not have the time to work, build this project, teach people Blender/Python, and live my life. So please respect my time, I'd love to help! 

If building an NFT collection in blender is something you really want to do and you have experience with Blender, I suggest you get familiar with some basic Python functionality and the how to run scripts in the Belnder Text Editor (an indepth knowledge is not required). However, if you don't use Blender but have a coding background, I would suggest watching some basic tutorials just to get a feel for the software (an indepth knowledge is not required).

To be honest I have no idea how to use Blender. I know some basic things, but I know the API and Python a lot better. This is my first Blender/Python project, so you may be wondering "how is he making a NFT collection with Blender??" Well I'm not, I write the code for the Blend_My_NFTs, and my team has three other members; Devlin and Caelin, who create the scenes and models in Blender, and the third is Quinn who is the lead web developer for our site. 

I garuntee this will eventually be an add on to Blender and not just a script you run through the script editor. (I mostly just put this in here for motivation, please don't pester me about the date lol)

# Blend_My_NFTs Tutorial Guide

## Blender API

This Blender add on heaviliy relies on the Blender API and its documentation which you can find here: https://docs.blender.org/api/current/index.html

If you are interested in python I highly recomend getting familiar with some of the basic commands such as bpy.data, bpy.context, and bpy.ops. Also read the Quick Start, very helpful. 

## Important Terminology 

Before we can continue there are terms that I will be using to describe the process of this software and make it a bit easier to understand. Refer to this section if you come accross an unfamiliar term. 

For the following terms, lets say you are creating an NFT collection where the image is of a person wearing a hat:

**- Attribute** - A part of an NFT that can be changed. The hat on a man is an Attribute, there are many types of hats, but the hat itself I will refer to it as an attribute.

**- Variants** - These are the types of hats; red hat, blue hat, green hat, cat hat, etc. These can be swapped into the hat Attribute with one another to create different NFTs. 

**- DNA** - DNA is a sequence of numbers that determins what Variant from every Attribute in an NFT collection to include in a single NFT image. This program generates a uniqe DNA sequence for every possible combination of Variants in Attributes. 

**- Batch** - A Batch is a randomly selected subset of NFT DNA. It is a smaller portion of the total number of NFTs you want to generate. This makes the work load of rendering thousands of images easier to manage. It also gives you the option to render on multiple computers and ensures each computer renders seperate images with no overlap.

## Getting started

Follow these steps to setup Blend_My_NFTs:

1. Scroll up on this page and click the green "Code" button at the top of this page
2. Click "Download Zip" - This will download the Blend_My_NFTs folder to your Downloads folder in zip format
3. In your download folder, move Blend_My_NFTs-main.zip to your desktop
4. Unzip the file:
- How to unzip a file on Mac: https://support.apple.com/en-ca/guide/mac-help/mchlp2528/mac
- How to unzip a file on Windows: https://support.microsoft.com/en-us/windows/zip-and-unzip-files-f6dde0a7-0fec-8294-e1d3-703ed85e7ebc
5. Ensure the Blend_My_NFTs-main folder is located on your Desktop for easy access (recomended)
6. Rename the Blend_My_NFTs-main folder to Blend_My_NFTs

## How to set up your .Blend file 

In order for Blend_My_NFTs to read your .blend file, you need to structure your scene in a specific way. Please follow all naming and collection conventions exactly, otherwise the scripts might not run properly. 

**Important Note**

Your .blend file must be moved to the Blend_My_NFTs folder. When you run the script, the .blend file must have the same directory of the Blend_My_NFTs folder. The Blender text editor has some weird quirks that make finding the right directory a bit tricky, I suggest reading about it in the Blender API above. This is the only work around I could find. 

Rules for .blend structure: 

- All Objects, collections, light sources, cameras, or anything else you want to stay constant for each NFT insert it into a collection named "Script_Ignore" exactly. This collection should be located directly beneath the 'Scene Collection' in your .blend file. Every thing in this Script_Ignore collection will be ignored by the collection (Attribute) fetcher. The state of the render and viewport camera of any objects/collections in Script_Ignore will remain unchanged during the scripts operation. The script will not turn the cameras of anything located in Script_Ignore on or off.

- Every Attribute of your NFT must be represented by a collection directly beneath the 'Scene Collection' in your .blend file. DO NOT USE NUMBERS  OR UNDERSCORES IN THE NAME OF THESE COLLECTIONS, this will mess with the scripts. Only use capital letters and lowercase letters, no numbers(0-9) or the underscore symbol( _ ). 

- For each Variant of each Attribute create a collection containing everything that makes up that Variant. This Variant collection must be placed within the Attribute collection and named with the following format: VariantName_(variant number begining at 1)_0 (e.g. Cube_1_0, Cube_2_0, etc.). The VariantName CANNOT CONTAIN NUMBERS OR UNDERSCORES. Like above, this will mess with the scripts.

Here is an example of the collection format I used to create this script in my .blend file:

<img width="422" alt="Screen Shot 2021-10-24 at 8 37 35 PM" src="https://user-images.githubusercontent.com/82110564/138619320-80a9f2a7-719a-46bc-b1cf-0e19dd4d640d.png">

## How to run scripts in Blender

If you have no experience with Blender, python, or the Blender API, please watch this tutorial for basic Blender Python information: https://www.youtube.com/watch?v=cyt0O7saU4Q 

There is also helpful documentation in the Blender API about running scripts here: 
https://docs.blender.org/api/current/info_quickstart.html#running-scripts

Note - You will need to install the Icon Viewer add on for Blender: https://docs.blender.org/manual/en/latest/addons/development/icon_viewer.html 

In the Blend_My_NFTs open the config.py file. Here you can customize some aspects of Blend_My_NFTs. The most important thing to do here is to add the path of Blend_My_NFTs on your computer to either save_path_mac or save_path_windows.

1. Open the Scripting tab in the menu of Blender: 

<img width="1440" alt="Screen Shot 2021-10-24 at 9 51 25 PM" src="https://user-images.githubusercontent.com/82110564/138623488-9d0efc07-4004-4d3a-a7fe-25cb6050ac51.png">

2. Click the "Open" button in the Blender Text Editor:

<img width="1422" alt="Screen Shot 2021-10-29 at 11 31 38 PM" src="https://user-images.githubusercontent.com/82110564/139518856-7798ea86-0be0-4511-bc87-fa09ce2f6538.png">

3. With the Blender File View open, navigate to the Blend_My_NFTs folder, select main.py and click "Open" in the bottom right corner:

<img width="1061" alt="Screen Shot 2021-10-29 at 11 35 03 PM" src="https://user-images.githubusercontent.com/82110564/139518920-a987d72a-a213-4579-a682-79e8d55fedca.png">

4. Repeat the previous step for PNG_Generator.py.

5. To navigate to the a script click the drop down button shown circled below:

<img width="274" alt="Screen Shot 2021-10-29 at 11 48 13 PM" src="https://user-images.githubusercontent.com/82110564/139519232-20891a2f-041f-4fa7-8f8a-b467e02de503.png">

6. To run a script click the run button shown circled below:

<img width="263" alt="Screen Shot 2021-10-29 at 11 51 08 PM" src="https://user-images.githubusercontent.com/82110564/139519277-4e02ee15-d97c-4f30-83e4-5837a3388d66.png">

## The order to run scripts

Run the scripts in the following order: 
1. main.py - Generates NFTRecord.json, a list of all possible NFT combinations then randomly selects NFTs from NFTReocord.json and adds them to a specified number of Batch#.json files
3. PNG_Generator.py - Renders the NFTs from a specified Batch #number and exmports the image to "Images from PNG Generator"
