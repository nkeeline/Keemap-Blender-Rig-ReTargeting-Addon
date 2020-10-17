import bpy
 
class KeeMapBoneMappingListItem(bpy.types.PropertyGroup): 
      #"""Group of properties representing a bone mapping from OpenPose to a Rig""" 
      
    name : bpy.props.StringProperty()
    label : bpy.props.StringProperty()
    description : bpy.props.StringProperty()

    SourceBoneName: bpy.props.StringProperty(
        name="Source Bone Name",
        description="This is the name for the rig bone name.",
        default="",
        maxlen=1024
        )

    DestinationBoneName: bpy.props.StringProperty(
        name="Destination Bone Name",
        description="This is the name for the rig bone name.",
        default="",
        maxlen=1024
        )
        
    keyframe_this_bone: bpy.props.BoolProperty(
        name="KeyFrame This Bone",
        description="Use this checkbox to disable keyframing of this bone for testing.",
        default = True
        ) 

    CorrectionFactor: bpy.props.FloatVectorProperty(
        name="Correction Rotation",
        description="After Setting the global position of the bone to the same as the source the script will rotate the bone by these angles afterwards to correct rotational differences between the sourc and destination bones.",
        subtype = 'EULER',
        unit = 'ROTATION',
        default = (0.0, 0.0, 0.0), 
        size = 3
        )

        
    has_twist_bone: bpy.props.BoolProperty(
        name="Has a Twist Bone",
        description="This will apply the twist along the y axis",
        default = False
        ) 
        

    TwistBoneName: bpy.props.StringProperty(
        name="Twist Bone Name",
        description="This is the name for the rig bone name.",
        default="",
        maxlen=1024
        )
        
    set_bone_position: bpy.props.BoolProperty(
        name="Set Position of Bone",
        description="This will set the bone position to the same position of the source bone.",
        default = False
        ) 
        
    set_bone_rotation: bpy.props.BoolProperty(
        name="Set Rotation of Bone",
        description="This will set the bone rotation to the same position of the source bone.",
        default = True
        ) 
        
      
    bone_rotation_application_axis: bpy.props.EnumProperty(
        name="Apply To Axis",
        description="Axis to Apply twist translation or rotation to, other axis will be left zero.",
        items=[ ('XYZ', "XYZ", ""),
                ('XY', "XY", ""),
                ('XZ', "XZ", ""),
                ('YZ', "YZ", ""),
                ('X', "X", ""),
                ('Y', "Y", ""),
                ('Z', "Z", "")
               ]
        )
      
    bone_transpose_axis: bpy.props.EnumProperty(
        name="Transpose Axis",
        description="Select Two Axis to swap when applying angle.",
        items=[ ('NONE', "NONE", ""),
                ('ZXY', "ZXY", ""),
                ('ZYX', "ZYX", ""),
                ('XZY', "XZY", ""),
                ('YZX', "YZX", ""),
                ('YXZ', "YXZ", ""),
                ('ZXY', "ZXY", "")
               ]
        )

    position_correction_factor: bpy.props.FloatVectorProperty(
        name="Correction Position",
        description="After Setting the global position of the bone to the same as the source the script will offset the position of the bone by the amount in each direction here.",
        subtype = 'TRANSLATION',
        unit = 'LENGTH',
        default = (0.0, 0.0, 0.0), 
        size = 3
        )

    position_gain: bpy.props.FloatProperty(
        name = "Position Gain",
        description="Multiplication applied to the position, so if your source is a large character and the destination a small one you want a velue less than one so the character does not move as much.",
        default = 1,
        min = 0,
        max = 100000
        )
def register():
    bpy.utils.register_class(KeeMapBoneMappingListItem)
    bpy.types.Scene.keemap_bone_mapping_list_index = bpy.props.IntProperty()
    bpy.types.Scene.keemap_bone_mapping_list = bpy.props.CollectionProperty(type = KeeMapBoneMappingListItem) 


def unregister():
    bpy.utils.unregister_class(KeeMapBoneMappingListItem)
    del bpy.types.Scene.keemap_bone_mapping_list
    del bpy.types.Scene.keemap_bone_mapping_list_index