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
        
    set_bone_scale: bpy.props.BoolProperty(
        name="Set Scale of Bone",
        description="This will set the bone scale based on angle of other bones.  Currently only used for Rigify Finger Controls.",
        default = False
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

    postion_type: bpy.props.EnumProperty(
        name="Position Type",
        description="Select the method used to position bone.",
        items=[ ('SINGLE_BONE_OFFSET', "Single Bone Offset", ""),
                ('POLE', "Pole Bone", "")
               ]
        )
        
    position_pole_distance: bpy.props.FloatProperty(
        name = "Pole Distance",
        description="Distance from bones to place pole target",
        default = .3,
        min = 0,
        max = 100000
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
        
    scale_gain: bpy.props.FloatProperty(
        name = "Scale Gain",
        description="Amount to scale based on angle of bone",
        default = 1,
        min = -100000,
        max = 100000
        )
        
    scale_secondary_bone_name: bpy.props.StringProperty(
        name="2nd Source Scale Bone Name",
        description="This is the name for the source rig bone name the angle with respect to the other source bone will be used to scale the destination bone.  The angle between the two source bones are used to scale the dest bone.  Mainly used for rigify where the angle between the tip of the finger and the base finger bone is used to scale the finger control bone so scaling the control bone bends the finger.",
        default="",
        maxlen=1024
        )
        
    bone_scale_application_axis: bpy.props.EnumProperty(
        name="Apply Scale To Axis",
        description="Axis to Apply scale to, other axis will be left alone.",
        default = 'Y',
        items=[ ('XYZ', "XYZ", ""),
                ('XY', "XY", ""),
                ('XZ', "XZ", ""),
                ('YZ', "YZ", ""),
                ('X', "X", ""),
                ('Y', "Y", ""),
                ('Z', "Z", "")
               ]
        )
def register():
    bpy.utils.register_class(KeeMapBoneMappingListItem)
    bpy.types.Scene.keemap_bone_mapping_list_index = bpy.props.IntProperty()
    bpy.types.Scene.keemap_bone_mapping_list = bpy.props.CollectionProperty(type = KeeMapBoneMappingListItem) 


def unregister():
    bpy.utils.unregister_class(KeeMapBoneMappingListItem)
    del bpy.types.Scene.keemap_bone_mapping_list
    del bpy.types.Scene.keemap_bone_mapping_list_index