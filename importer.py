import bpy
import os
import sys
import importlib
import pathlib


def import_fbx_files(list_of_files, collection_name):
	# create collection for all attributes of this type 
	bpy.ops.collection.create(name=collection_name)
	
	# link this collection to scene root (eg. rootCol -> coneCol)
	bpy.context.scene.collection.children.link(bpy.data.collections[collection_name])
	
	index = 0    
	for file in list_of_files:  	  
		index = index + 1
		# create collection for every attribute variation (eg. coneWhite_1_0)
		obj_col_name = file[:-4] + "_" + str(index) + "_" #+ str(probability)
		bpy.ops.collection.create(name=obj_col_name)
		
		# link collection to current attribute collection
		bpy.data.collections[collection_name].children.link(bpy.data.collections[obj_col_name])
		
		# import .fbx file
		bpy.ops.import_scene.fbx(filepath=os.getcwd() + "\\" + file)   
		
		# get all selected objs (objs are auto selected after import)
		objs = (bpy.context.selected_objects)
		
		# rename object to filename (remove .fbx file ending)
		objs[0].name = file[:-4]
		
		# link object to corresponding collection (eg. coneWhite_1_0)
		bpy.context.scene.collection.objects.unlink(objs[0])
		bpy.data.collections[obj_col_name].objects.link(objs[0])		
		
		# make sure last imported object is no longer selected
		bpy.ops.object.select_all(action="DESELECT")  
		
def run():

	
	# Go to folder where models are stored (<.blend-file>\\3D_Model_Input)
	model_dir = os.chdir(os.getcwd() + "\\3D_Model_Input")
	
	# Save directory location of (<.blend-file>\\3D_Model_Input)
	top_level_dir = os.getcwd()
	
	# Get every subdirectory of current directory (<.blend-file>\\3D_Model_Input\\[Cone, Sphere, ....])
	directory_contents = os.listdir(os.getcwd())
	
	# Go through every model-dir ([Cone, Sphere,...])
	for directory in directory_contents:

		# make sure we are in <.blend-file>\\3D_Model_Input
		os.chdir(top_level_dir)

		# exclude files (eg. .gitignore etc.)
		if os.path.isdir(directory):
			
			# go into model directory eg. <.blend-file>\\3D_Model_Input\\Cone
			os.chdir(os.getcwd()+"\\"+directory)
			
			# get all files contained in eg. <.blend-file>\\3D_Model_Input\\Cone
			list_of_files = os.listdir(os.getcwd())

			# directory should always be the name of the attribute
			import_fbx_files(list_of_files, directory)
		
	
if __name__ == '__main__':
	# Make sure we are in correct starting directory (dir of this .blend file)
	os.chdir(pathlib.Path(__file__).parent.resolve().parent.resolve())
	
	# run importer prog
	run()