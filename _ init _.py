bl_info = {
    "name": "Skmr League Utility",
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


# load and reload submodules
##################################

import importlib
from . import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())



# register
##################################

import traceback

def register():
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()

    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

def unregister():
    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()

    print("Unregistered {}".format(bl_info["name"]))