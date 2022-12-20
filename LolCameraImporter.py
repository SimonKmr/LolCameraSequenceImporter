bl_info = {
    "name": "lol-Camera Importer",
    "author": "SimonKmr",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Uses a json created by CreatorSuite or the LolReplayApiSequence to create a camera with matching movement",
    "warning": "",
    "support": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

import bpy
from pathlib import Path
import json
import math
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.utils import register_class, unregister_class
from bpy_extras.io_utils import ImportHelper

def get_time_scale_factor(j):
    fss = bpy.context.scene.frame_start
    fse = bpy.context.scene.frame_end
    fsd = fse - fss

    te = 86400.0
    tl = 0.0

    for i in j["cameraPosition"]:
        if i["time"] > tl:
            tl = i["time"]
            
    for i in j["cameraPosition"]:
        if i["time"] < te:
            te = i["time"]
         
    td = tl - te
    return [fsd / td,te]

def create_sequence(j):
    #adjust timeframe to blender file
    sa = 0.01
    tsfr = get_time_scale_factor(j)
    tmf = tsfr[0]
    te = tsfr[1]
    
    #create camera
    bpy.ops.object.camera_add(enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
    camera = bpy.context.active_object
    camera.data.angle = 0.698132

    #import camera location
    pc = len(j["cameraPosition"])
    for i in range(pc):
        camera.location = [j["cameraPosition"][i]["value"]["x"] * sa,
        j["cameraPosition"][i]["value"]["z"] * sa,
        j["cameraPosition"][i]["value"]["y"] * sa]
        
        t = j["cameraPosition"][i]["time"]-te
        f = t*tmf+1
        camera.keyframe_insert(data_path="location",index = 1, frame=f)

    #import camera rotation
    rc= len(j["cameraRotation"])
    for i in range(rc):   
        camera.rotation_euler = [math.radians(-j["cameraRotation"][i]["value"]["y"]+90),
        math.radians(j["cameraRotation"][i]["value"]["z"]),
        math.radians(-j["cameraRotation"][i]["value"]["x"])]
        
        t = j["cameraRotation"][i]["time"]-te
        f = t*tmf+1
        camera.keyframe_insert(data_path="rotation_euler", frame=f)
        
        
    return {'FINISHED'}


class ButtonOperator(bpy.types.Operator):
    bl_idname="object.lolcameraimportbutton"
    bl_label="Import lolCameraMovement"
    
    
    


    
    
    def execute(self, context):
        #open_file_menu
        bpy.ops.lol_camera.sequence_importer('INVOKE_DEFAULT')
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
        row.operator(ButtonOperator.bl_idname,text="Import", icon='WORLD_DATA')


def read_sequence(context, filepath):
    with open(filepath) as f:
        return json.load(f)
    
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
        s = read_sequence(context, self.filepath)
        create_sequence(s)
        return {'FINISHED'}

_classes = [
    LolCameraImporterPanel,
    ButtonOperator,
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