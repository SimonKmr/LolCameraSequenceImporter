bl_info = {
    "name": "lol-Camera Importer",
    "author": "SimonKmr",
    "version": (1, 0),
    "blender": (4, 5, 0),
    "location": "",
    "description": "Uses a json created by CreatorSuite or the LolReplayApiSequence to create a camera with matching movement",
    "warning": "",
    "support": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

import bpy
import logging
import json
import math
import requests
from pathlib import Path
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.utils import register_class, unregister_class
from bpy_extras.io_utils import ImportHelper
from bpy.props import *

def create_camera(lol_camera):
    #adjust timeframe to blender file
    scale = 0.01
    duration_scale = 1
    
    #create camera
    bpy.ops.object.camera_add(enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
    camera = bpy.context.active_object
    camera.data.angle = 0.698132
    
    #import camera location
    positions = len(lol_camera["cameraPosition"])
    for pos in range(positions):
        location = [lol_camera["cameraPosition"][pos]["value"]["x"] * scale,
                    lol_camera["cameraPosition"][pos]["value"]["z"] * scale,
                    lol_camera["cameraPosition"][pos]["value"]["y"] * scale]
        
        
        camera.location = location
        
        
        offset = get_time_offset(lol_camera["cameraPosition"])
        time = lol_camera["cameraPosition"][pos]["time"] - offset
        frame = time * bpy.context.scene.render.fps * duration_scale
        
        camera.keyframe_insert(data_path="location",index = 0, frame=frame)
        camera.keyframe_insert(data_path="location",index = 1, frame=frame)
        camera.keyframe_insert(data_path="location",index = 2, frame=frame)

    #import camera rotation
    rotations = len(lol_camera["cameraRotation"])
    for rot in range(rotations):
        rotation = [math.radians(-lol_camera["cameraRotation"][rot]["value"]["y"]+90),
                    math.radians(lol_camera["cameraRotation"][rot]["value"]["z"]),
                    math.radians(-lol_camera["cameraRotation"][rot]["value"]["x"])]
        
        camera.rotation_euler = rotation
        
        time = lol_camera["cameraRotation"][rot]["time"] - offset
        frame = time * bpy.context.scene.render.fps * duration_scale
          
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        
    return {'FINISHED'}

def get_time_offset(keyframes):
    n = len(keyframes)
    
    result = -1
    smallest_offset = float("inf")
    
    for k in range(n):
        if keyframes[k]["time"] < smallest_offset:
            smallest_offset = keyframes[k]["time"]

    return smallest_offset

class ImportFileButtonOperator(bpy.types.Operator):
    bl_idname="object.lolcameraimportbutton"
    bl_label="Import lolCameraMovement"
    
    def execute(self, context):
        #open_file_menu
        bpy.ops.lol_camera.sequence_importer('INVOKE_DEFAULT')
        return {'FINISHED'}

class ImportClientButtonOperator(bpy.types.Operator):
    bl_idname="object.lolcameraimportclientbutton"
    bl_label="Import lolCameraMovement"
    
    def execute(self, context):
        #request sequence data from League API
        #https://127.0.0.1:2999/replay/sequence
        response = requests.get("https://127.0.0.1:2999/replay/sequence", verify=False)
        sequence = json.loads(response.text)
        create_camera(sequence)
        return {'FINISHED'}    

class ImportSequence(bpy.types.Operator, ImportHelper):
    bl_idname = "lol_camera.sequence_importer"
    bl_label = "Import Sequence" 
    
    filename_ext = ".json"
    
    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    def execute(self, context):
        with open(self.filepath) as file:
            sequence = json.load(file)
            create_camera(sequence)
        return {'FINISHED'}


class LolCameraImporterPanel(bpy.types.Panel):
    bl_label = "lol-Camera"
    bl_idname = "lolcameraimportpanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "lol-Camera"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
        row.operator(ImportFileButtonOperator.bl_idname,text="Import File")
        row = layout.row()
        row.operator(ImportClientButtonOperator.bl_idname,text="Import Client")
        
    


_classes = [
    LolCameraImporterPanel,
    ImportFileButtonOperator,
    ImportClientButtonOperator,
    ImportSequence
]

def register():
    for cls in _classes:
        register_class(cls)
    

def unregister():
    for cls in _classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()