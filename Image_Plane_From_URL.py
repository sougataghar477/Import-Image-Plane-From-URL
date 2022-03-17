bl_info = {
    "name": "Import Image As Plane From URL",
    "author": "Sougata Ghar,Florian Meyer",
    "version": (1),
    "blender": (3,0,1),
    "location": "VIEW3D > UI",
    "description": "Import Image Plane from a URL",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Import",
}

import bpy
import urllib.request
import os
import random
import addon_utils
from pathlib import Path
from os import getcwd


addon_utils.enable("io_import_images_as_planes",default_set = True,persistent=True)

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Image Plane From URL"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Image Plane From URL'

    def draw(self, context):
        self.layout.prop(context.scene, "string_prop")
        row=self.layout.row()
        row.operator("mesh.mycubeoperator")

class MyOperator(bpy.types.Operator):
    bl_idname="mesh.mycubeoperator"
    bl_label="Import Image Plane"
    
    def execute(self,context):

        parentFolder=Path(getcwd())
        
        tempDir = Path(bpy.app.tempdir)
        
        url = bpy.context.scene.string_prop
        
        filename=url.split('/')[-1]
        
        shortenedName = filename[0:5]
        
        print(shortenedName)
        
        isImageinFormat=True
        
        if(not filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.webp') or filename.endswith('.cms')):
            isImageinFormat=False
            
        if(not isImageinFormat):
            if('jpg' in filename):
                filename=shortenedName+'.jpg'
            
            if('png' in filename):
                filename=shortenedName+'.png'
            
            if('jpeg' in filename):
                filename=shortenedName+'.jpg'
                
            if('webp' in filename):
                filename=shortenedName+'.webp'
            
            if('cms' in filename):
                filename=shortenedName+'.cms'                
        

        
        
        sub_name='images'
        
        
        subfolder=tempDir / sub_name
        
        subfolder.mkdir(exist_ok=True)
        
        filename_path = subfolder / filename
        
        print(filename_path)


        urllib.request.urlretrieve(bpy.context.scene.string_prop,filename_path)
        
        bpy.ops.import_image.to_plane(files=[{"name":str(filename_path)}], directory=str(parentFolder))
        
        print(filename_path)



        return {"FINISHED"}

def register():
#    addon_utils.enable("import_image.to_plane",default_set = True,persistent=True)
    bpy.types.Scene.string_prop = bpy.props.StringProperty(name="URL")
    bpy.utils.register_class(LayoutDemoPanel)
    bpy.utils.register_class(MyOperator)


def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)
    bpy.utils.unregister_class(MyOperator)
    bpy.utils.unregister_class(MyOperator)
    del(bpy.types.Scene.string_prop)

if __name__ == "__main__":
    register()
    

    