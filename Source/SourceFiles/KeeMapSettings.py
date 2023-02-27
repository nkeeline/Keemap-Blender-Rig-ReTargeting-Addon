import bpy

class KeeMapSettings(bpy.types.PropertyGroup):

    start_frame_to_apply: bpy.props.IntProperty(
        name = "Starting Frame",
        description="Frame to Apply Motion Capture To",
        default = 0,
        min = 0,
        max = 10000
        )
        
    number_of_frames_to_apply: bpy.props.IntProperty(
        name = "Number of Samples",
        description="Number of Samples to read in and apply",
        default = 100,
        min = 0,
        max = 10000
        )


    keyframe_every_n_frames: bpy.props.IntProperty(
        name = "Keyframe Number",
        description="Frame to Apply a Keyframe to, 1 is every frame",
        default = 3,
        min = 1,
        max = 100
        )
    source_rig_name: bpy.props.StringProperty(
        name="Source Rig Name",
        description="Rig Name to Apply Capture To",
        default="",
        maxlen=1024
        )
    destination_rig_name: bpy.props.StringProperty(
        name="Destination Rig Name",
        description="Rig Name to Apply Capture To",
        default="",
        maxlen=1024
        )
        
    bone_mapping_file: bpy.props.StringProperty(
        name="Bone Mapping File to Read and Save",
        description="Select a File to Read In:",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
        )
      
    bone_rotation_mode: bpy.props.EnumProperty(
        name="Rotation Mode",
        description="What mode to set rotation of bone in.  Quaternion more robust, Euler easier to understand but has gimbal lock.",
        default="EULER",
        items=[ ('EULER', "EULER", ""),
                ('QUATERNION', "QUATERNION", "")
               ]
        )
        
    keyframe_test: bpy.props.BoolProperty(
        name="KeyFrame Test",
        description="Use this checkbox to enable keyframing of this bone while testing.",
        default = False
        ) 
		
	
def register():
    bpy.utils.register_class(KeeMapSettings)
    bpy.types.Scene.keemap_settings = bpy.props.PointerProperty(type=KeeMapSettings)


def unregister():
    bpy.utils.unregister_class(KeeMapSettings)
    del bpy.types.Scene.keemap_settings	