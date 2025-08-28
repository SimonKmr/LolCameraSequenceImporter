bl_info = {
    "name": "League Camera Importer",
    "author": "SimonKmr",
    "version": (1, 0),
    "blender": (4, 5, 0),
    "location": "",
    "description": "Get the camera data from League of Legends and create a camera in Blender. Also works with json files from CreatorSuite / LolNam-Editor.",
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

def create_camera(lol_camera, settings):
    #adjust timeframe to blender file
    scale = settings.scale
    duration_scale = 1 / settings.speed
    
    #create camera
    bpy.ops.object.camera_add(enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
    camera = bpy.context.active_object
    camera.data.angle = 0.698132
    
    #get offset to set first frame at 0
    offset = get_time_offset(lol_camera["cameraPosition"])
    
    #import camera location
    if settings.use_position:
        positions = len(lol_camera["cameraPosition"])
        for pos in range(positions):
            location = [lol_camera["cameraPosition"][pos]["value"]["x"] * scale,
                        lol_camera["cameraPosition"][pos]["value"]["z"] * scale,
                        lol_camera["cameraPosition"][pos]["value"]["y"] * scale]
            
            
            camera.location = location
            
            time = lol_camera["cameraPosition"][pos]["time"] - offset
            frame = time * bpy.context.scene.render.fps * duration_scale
            
            camera.keyframe_insert(data_path="location",index = 0, frame=frame)
            camera.keyframe_insert(data_path="location",index = 1, frame=frame)
            camera.keyframe_insert(data_path="location",index = 2, frame=frame)

    #import camera rotation
    if settings.use_rotation:
        rotations = len(lol_camera["cameraRotation"])
        for rot in range(rotations):
            rotation = [math.radians(-lol_camera["cameraRotation"][rot]["value"]["y"]+90),
                        math.radians(lol_camera["cameraRotation"][rot]["value"]["z"]),
                        math.radians(-lol_camera["cameraRotation"][rot]["value"]["x"])]
            
            camera.rotation_euler = rotation
            
            time = lol_camera["cameraRotation"][rot]["time"] - offset
            frame = time * bpy.context.scene.render.fps * duration_scale
              
            camera.keyframe_insert(data_path="rotation_euler", frame=frame)
            
    #import focal length
    if settings.use_fov:
        focal_lengths = len(lol_camera["fieldOfView"])
        for fov in range(rotations):
            camera.data.angle = 0.698132
    
    return {'FINISHED'}

def get_time_offset(keyframes):
    n = len(keyframes)
    
    result = -1
    smallest_offset = float("inf")
    
    for k in range(n):
        if keyframes[k]["time"] < smallest_offset:
            smallest_offset = keyframes[k]["time"]

    return smallest_offset

class Import_File_Button_Operator(bpy.types.Operator):
    bl_idname="object.lolcameraimportbutton"
    bl_label="Import lolCameraMovement"
    
    def execute(self, context):
        #open_file_menu
        bpy.ops.lol_camera.sequence_importer('INVOKE_DEFAULT')
        return {'FINISHED'}

class Import_Client_Button_Operator(bpy.types.Operator):
    bl_idname="object.lolcameraimportclientbutton"
    bl_label="Import lolCameraMovement"
    
    def execute(self, context):
        #request sequence data from League API
        #https://127.0.0.1:2999/replay/sequence
        response = requests.get("https://127.0.0.1:2999/replay/sequence", verify=False)
        sequence = json.loads(response.text)
        create_camera(sequence,context.scene.camera_props)
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
            create_camera(sequence,context.scene.camera_props)
        return {'FINISHED'}

class LolCameraImporterPanel(bpy.types.Panel):
    bl_label = "League Camera"
    bl_idname = "lolcameraimportpanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "League Camera"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        layout.label(text="Settings")
        #row = layout.row()
        #row.prop(context.scene.camera_props, 'target')
        layout.row().prop(context.scene.camera_props, 'scale')
        layout.row().prop(context.scene.camera_props, 'speed')
        row = layout.row()
        
        row = layout.label(text="Selection")
        layout.row().prop(context.scene.camera_props, 'use_position')
        layout.row().prop(context.scene.camera_props, 'use_rotation')
        layout.row().prop(context.scene.camera_props, 'use_fov')
        row = layout.row()
        
        row = layout.label(text="Import Camera by")
        layout.row().operator(Import_Client_Button_Operator.bl_idname,text="Client")
        layout.row().operator(Import_File_Button_Operator.bl_idname,text="File")
        
class CameraPropertyGroup(bpy.types.PropertyGroup):
    #target: bpy.props.PointerProperty(type='MaterialSettings',name="Camera")
    scale: bpy.props.FloatProperty(name="Scale", soft_min=0.001, soft_max=1, default=0.01)
    speed: bpy.props.FloatProperty(name="Speed", soft_min=0.25, soft_max=4, default = 1)
    
    use_position: bpy.props.BoolProperty(name="Position",default=True)
    use_rotation: bpy.props.BoolProperty(name="Rotation",default=True)
    use_fov: bpy.props.BoolProperty(name="FOV",default=True)

_classes = [
    LolCameraImporterPanel,
    Import_File_Button_Operator,
    Import_Client_Button_Operator,
    ImportSequence,
]

def register():
    
    bpy.utils.register_class(CameraPropertyGroup)
    bpy.types.Scene.camera_props = bpy.props.PointerProperty(type=CameraPropertyGroup)
    
    for cls in _classes:
        register_class(cls)
    

def unregister():
    for cls in _classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()