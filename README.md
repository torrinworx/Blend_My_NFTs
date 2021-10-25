# Blend_My_NFTs


## Description
This project is a work in progress (as of Oct 24th, 2021) and will eventually be an add on to Blender. Blend_My_NFTs is bing developed to create the NFT project This Cozy Place. This Cozy Place will be an NFT collection with a total of 10000 unique NFTs all rendered in Blender with this add on. If you need help with your project please visit our discord server: https://discord.gg/UpZt5Un57t. If you are looking to buy your own Cozy Place NFT, please visit ThisCozyPlace.com

## Disclaimer

Nothing in this repository is financial advice. Create an NFT project/collection at your own risk, I am simply providing a means of acomplishing a goal, not investment/financial information about that goal. Do your own research before spending money on NFTs or any asset. 

I do not garuntee this software will work with your setup. There are many variables and factors that go into running the scripts provided, it differs from system to system, and from blend file to blend file. I encourage you to do some trouble shooting, read the Blender API documentation, or if your desperate, risk it all on the Blender Stack Exchange. 

If you need help I am available on the disord channel above for consulting. However! I am not a toutor, although I enjoy teaching people, I simply do not have the time to work, build this project, teach people Blender/Python, and live my life. So please respect my time, I'd love to help.

If building an NFT collection in blender is something you really want to do and you have experience with Blender, I suggest you get familiar with Python and the Blender API. However if you don't use Blender, how did you find this repository? Like seriously, how? You must be lost... I think Reddit was the other way...

To be honest I have no idea how to use Blender. I know some basic things, but I know the API a lot better. This is my first Blender/Python project, so you may be wondering "how is he making a NFT collection with Blender??" Well I'm not, I write the code for the image generator, my team has three other members; Devlin and Caelin, who create the scenes and models in Blender and do magic with it, and the third is Quinn who is the web developer for the our site and makes everything look all pretty. 

This page is not finished! I don't know how long it will take to make this tutorial page, but it shouldn't be to long. (As of Oct 24th, 2021)

I garuntee this will be an add on to Blender and not just a script you run through the script editor. This will take some time, as of Oct 24th 2020 I am still wrking out some user friendly issues with the software, and some kinks, but other than that we are a go for the add on phase. (I mostly just put this in here for motivation, please don't pester me about the date lol)

The scripts are a bit of a mess right now, I mostly have them set up so I know the main processes will work. I will consolodate them whenever I begin the add on phase where I will implement Blender UI to make the porcess of generating thousnds of NFTs more user friendly. 

If you are interested in helping out develop the image generator, please feel free to message me on the discord above would love to collaborate with you to improve my bad code! 

# Guide to Blend_My_NFTs

## Blender API
This Blender add on heaviliy relies on the Blender API and its documentation which you can find here: https://docs.blender.org/api/current/index.html

## Terminology 
Before we can continue there are a few terms that I will be using to describe the process of this program and make it a bit easier to understand. Please refer to this section if you come accross an unfamiliar term. 

For the following two terms, lets say you have an NFT where the image is of a person wearing a hat:

**- Attribute** - A part of an NFT that can be changed. The hat on a man is an attribute, there are many types of hats, but the hat itself I will refer to it as an attribute.

**- Variants** - These are the types of hats; red hat, blue hat, cat hat, etc. These can be swapped into the hat Attribute one at a time to create different NFTs. 

**- DNA** - DNA is a sequence of numbers that determins what Variant from every Attribute to include in a single NFT image. This program generates a uniqe DNA sequence for every possible combination of Variants in Attributes. 


## How to set up your .Blend file

In order for Blend_My_NFTs to read your .blend file, you need to structure your scene in a certain way. Please follow all naming conventions exactly, otherwise the scripts will not run properly. 

Rules for .blend structure: 

- All Objects, collections, light sources, cameras, or anything else you want to stay constant for each NFT insert it into a collection named "Script_Ignore" exactly. This collection must be located directly beneath the 'Scene Collection' in your .blend file. 

- Every Attribute of your NFT must be represented by a collection directly beneath the 'Scene Collection' in your .blend file. DO NOT USE NUMBERS IN THE NAME, this will mess with the script. Only use capital letters and lowercase letters, no numbers or the underscore symbol. 

- For each Variant of each Attribute create a collection containing everything that makes up that Variant. This Variant collection must be placed within the Attribute collection and named with the following format: VariantName_(variant number begining at 1)_0 (e.g. Cube_1_0, Cube_2_0, etc.). The VariantName CANNOT CONTAIN NUMBERS. LIke above, this will mess with the script, no underscore symbols either.

Here is an example of the collection format I used to create this script in my .blend file:

<img width="422" alt="Screen Shot 2021-10-24 at 8 37 35 PM" src="https://user-images.githubusercontent.com/82110564/138619320-80a9f2a7-719a-46bc-b1cf-0e19dd4d640d.png">

**Important Note**
Your .blend file must be inside the Blend_My_NFTs folder. When you run the script, the .blend file must have the same directory of the Blend_My_NFTs folder. The Blender text editor has some weird quirks that make finding the right directory a bit tricky, I suggest reading about it in the Blender API above. 

## How to run scripts in Blender
If you have no experience with Blender, python, or the Blender API, please watch this tutorial for basic Blender Python information: https://www.youtube.com/watch?v=cyt0O7saU4Q There is also helpful documentation in the Blender API about running scripts here: https://docs.blender.org/api/current/info_quickstart.html#running-scripts

First open the Scripting tab in the menu of Blender: 
<img width="1440" alt="Screen Shot 2021-10-24 at 9 51 25 PM" src="https://user-images.githubusercontent.com/82110564/138623488-9d0efc07-4004-4d3a-a7fe-25cb6050ac51.png">

Next 


