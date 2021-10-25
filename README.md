# Blend_My_NFTs


## Description
This project is a work in progress (as of Oct 24th, 2021) and will eventually be an add on to Blender. Blend_My_NFTs is bing developed to create the NFT project This Cozy Place. This Cozy Place will be an NFT collection with a total of 10000 unique NFTs all rendered in Blender with this add on. If you need help with your project please visit our discord server: https://discord.gg/UpZt5Un57t. If you are looking to buy your own Cozy Place NFT, please visit ThisCozyPlace.com


## Terminology 
Before we can continue there are a few terms that I will be using to describe the process of this program and make it a bit easier to understand. Please refer to this section if you come accross an unfamiliar term. 

For the following two terms, lets say you have an NFT where the image is of a person wearing a hat:

**- Attribute** - A part of an NFT that can be changed. The hat on a man is an attribute, there are many types of hats, but the hat itself I will refer to it as an attribute.

**- Variants** - These are the types of hats; red hat, blue hat, cat hat, etc. These can be swapped into the hat Attribute one at a time to create different NFTs. 

**- DNA** - DNA is a sequence of numbers that determins what Variant from every Attribute to include in a single NFT image. This program generates a uniqe DNA sequence for every possible combination of Variants in Attributes. 


## How to set up Collections in your .Blend file

In order for Blend_My_NFTs to read your .blend file, you need to structure your scene in a certain way. Please follow all naming conventions exactly, otherwise the scripts will not run properly. 

Rules for .blend structure: 

- All Objects, collections, light sources, cameras, or anything else you want to stay constant for each NFT insert it into a collection named "Script_Ignore" exactly. This collection must be located directly beneath the 'Scene Collection' in your .blend file. 

- Every Attribute of your NFT must be represented by a collection directly beneath the 'Scene Collection' in your .blend file. DO NOT USE NUMBERS IN THE NAME, this will mess with the script. Only use capital letters and lowercase letters, no numbers or the underscore symbol. 

- For each Variant of each Attribute create a collection containing everything that makes up that Variant. This Variant collection must be placed within the Attribute collection and named with the following format: VariantName_(variant number begining at 1)_0 (e.g. Cube_1_0, Cube_2_0, etc.). The VariantName CANNOT CONTAIN NUMBERS. LIke above, this will mess with the script, no underscore symbols either.

Here is an example of the collection format I used to create this script in my .blend file:

<img width="422" alt="Screen Shot 2021-10-24 at 8 37 35 PM" src="https://user-images.githubusercontent.com/82110564/138619320-80a9f2a7-719a-46bc-b1cf-0e19dd4d640d.png">

