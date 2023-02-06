import bpy
import math
import numpy as np
import json
import sys
from os import path
import mathutils
from mathutils import Vector


def Update():
    #bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
     
    #bpy.context.view_layer.update()
    #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

def get_point_on_vector(initial_pt, terminal_pt, distance):
    v = np.array(initial_pt, dtype=float)
    u = np.array(terminal_pt, dtype=float)
    n = v - u
    n /= np.linalg.norm(n, 2)
    point = v - distance * n

    #return tuple(point)
    return Vector(point)
def update_progress(job_title, progress):
    length = 40 # modify this to change the length
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100, 2))
    if progress >= 1: msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()
    
def GetBonePositionWSwCorrection(bone, arm, CorrectionX, CorrectionY, CorrectionZ, Gain):
    #global_location = arm.matrix_world @ bone.matrix @ bone.location
    #sourceStart = Vector((0, 0, 0))
    #sourceStart.x = (bone.location.x + CorrectionX)*Gain
    #sourceStart.y = (bone.location.y + CorrectionY)*Gain
    #sourceStart.z = (bone.location.z + CorrectionZ)*Gain
    #print("Getting Bone Position sourceStart: ", sourceStart)
    #armspace = GetBoneMatrix(bone) @  sourceStart
    
    #global_location = arm.matrix_world @ armspace
    #print("Getting Bone Position global_location: ", global_location)
    #print(global_location)
    #bone.location.x = (bone.location.x + CorrectionX)*Gain
    #bone.location.y = (bone.location.y + CorrectionY)*Gain
    #bone.location.z = (bone.location.z + CorrectionZ)*Gain
    newmat = bone.matrix.copy()
    print("Arm space of bone position of ", bone.name, ": ",newmat.translation)
    newmat.translation.x = (newmat.translation.x + CorrectionX)*Gain
    newmat.translation.y = (newmat.translation.y + CorrectionY)*Gain
    newmat.translation.z = (newmat.translation.z + CorrectionZ)*Gain
    print("Corrected Arm space of bone position of ", bone.name, ": ",newmat.translation)
    global_location2 = arm.convert_space(pose_bone=bone, 
        matrix=newmat, 
        from_space='POSE', 
        to_space='WORLD')
    print("Resulting WS: ",global_location2.translation)
    return global_location2.translation
    
def GetBonePositionWS(bone, arm):
    #boneWS = arm.location + bone.head
    boneWS = arm.convert_space(pose_bone=bone, 
        matrix=bone.matrix, 
        from_space='POSE', 
        to_space='WORLD')
    #print("World Space Position of ", bone.name, ": ",boneWS.translation)
    return boneWS.translation
    
def SetBonePositionWS(bone, arm, position):
    #print("Setinng Bone ", bone.name, "to WS Position: ",position)
    mw = arm.convert_space(pose_bone=bone, 
        matrix=GetBoneMatrix(bone), 
        from_space='POSE', 
        to_space='WORLD')
    mw.translation = position
    bone.matrix = arm.convert_space(pose_bone=bone, 
        matrix=mw, 
        from_space='WORLD', 
        to_space='POSE')
        
def SetBonePosition(SourceArmature, SourceBoneName, DestinationArmature, DestinationBoneName, DestinationTwistBoneName, WeShouldKeyframe, CorrectionX, CorrectionY, CorrectionZ, Gain):
    destination_bone =  DestinationArmature.pose.bones[DestinationBoneName]
    sourceBone = SourceArmature.pose.bones[SourceBoneName]
    
    #PositiontoPutDestinationBone = GetBonePositionWSwCorrection(sourceBone, SourceArmature, CorrectionX, CorrectionY, CorrectionZ, Gain)
    #PositiontoPutDestinationBone = GetBonePositionWSwCorrection(sourceBone, SourceArmature, 0, 0, 0, 1)
    PositiontoPutDestinationBone = GetBonePositionWS(sourceBone, SourceArmature)
    
    #newposition = GetBonePositionWS(sourceBone, SourceArmature)

    SetBonePositionWS(destination_bone, DestinationArmature, PositiontoPutDestinationBone)
    
    destination_bone.location.x = (destination_bone.location.x + CorrectionX)*Gain
    destination_bone.location.y = (destination_bone.location.y + CorrectionY)*Gain
    destination_bone.location.z = (destination_bone.location.z + CorrectionZ)*Gain
        
    Update()
    if (WeShouldKeyframe):
        currentFrame = bpy.context.scene.frame_current
        destination_bone.keyframe_insert(data_path='location',frame=currentFrame)

def SetBonePositionPole(SourceArmature, SourceBoneName, DestinationArmature, DestinationBoneName, DestinationTwistBoneName, WeShouldKeyframe, PoleDisrance):
    destination_bone =  DestinationArmature.pose.bones[DestinationBoneName]
    sourceBone = SourceArmature.pose.bones[SourceBoneName]
    parent_source_bone = sourceBone.parent_recursive[0]
    
    base_of_parent_bone_WS = GetBonePositionWS(parent_source_bone, SourceArmature)
    base_of_child_bone_WS = GetBonePositionWS(sourceBone, SourceArmature)
    tail_of_child_bone_WS = SourceArmature.matrix_world @ sourceBone.tail
    
    #so we're going to not find the exact average between the hip and ankle, we're going to find the ratio of the bone lengths
    #so when the leg straightens out the kneecap the the point we're calculating are at the correct angles.
    length_parent_bone = math.dist(base_of_parent_bone_WS, base_of_child_bone_WS)
    #print("length Parent Bone:")
    #print(length_parent_bone)
    length_child_bone = math.dist(base_of_child_bone_WS, tail_of_child_bone_WS)
    #print("length Child Bone:")
    #print(length_child_bone)
    
    c_p_ratio = length_parent_bone/(length_child_bone + length_parent_bone)
    #print("CP Ratio:")
    #print(c_p_ratio)
    length_base_parent_to_tip_of_child = math.dist(base_of_parent_bone_WS, tail_of_child_bone_WS)
    
    #we calculate the virtual pount behind the kneecap to draw a line through to the kneecap to out front to the pole
    #so we can have the pole out front of the knee.  We used to average the hip to ankle distance, but as the knee straightened
    #it didn't take into account the difference in lengths between the thigh and knee, so with knee and virtual points at different 
    #heights the pole went crazy going high or low.  This still doesn't behave well if there is NO bend to the knee, but in reality
    # this doesn't happen all that often.
    average_location = get_point_on_vector(base_of_parent_bone_WS, tail_of_child_bone_WS, length_base_parent_to_tip_of_child*c_p_ratio)
    
    #here is the old average code with the above mentioned problem.
        #for a hip we average the location of the hip and ankle
        #average_location = (base_of_parent_bone_WS + tail_of_child_bone_WS)/2
        #for a hip we calc the slope of teh average of the hip and ankle to the kneecap:
        #print(average_location)
        #print(base_of_child_bone_WS)
        #slope = base_of_child_bone_WS - average_location
        
        #PositiontoPutDestinationBone = slope*2 + average_location

    PositiontoPutDestinationBone = get_point_on_vector(base_of_child_bone_WS, average_location, PoleDisrance)
    #dist = abs(math.dist(average_location,base_of_child_bone_WS))
    
    SetBonePositionWS(destination_bone, DestinationArmature, PositiontoPutDestinationBone)
        
    Update()
    if (WeShouldKeyframe):
        currentFrame = bpy.context.scene.frame_current
        destination_bone.keyframe_insert(data_path='location',frame=currentFrame)
        
def GetBoneMatrix(bone):
    return bone.matrix
    
def CalcLocationOffset(index):  
    scene = bpy.context.scene
    KeeMap = scene.keemap_settings 
    bone_mapping_list = scene.keemap_bone_mapping_list
    
    print('Calc location offsets:')
    SourceArmName = KeeMap.source_rig_name
    DestArmName = KeeMap.destination_rig_name
    
    if SourceArmName == "":
        self.report({'ERROR'}, "Must Have a Source Armature Name Entered")
    elif DestArmName == "":
        self.report({'ERROR'}, "Must Have a Destination Armature Name Entered")
    else:
        SourceArm = bpy.data.objects[SourceArmName]
        DestArm  = bpy.data.objects[DestArmName]
        
        SourceBoneName = bone_mapping_list[index].SourceBoneName
        DestBoneName = bone_mapping_list[index].DestinationBoneName
                    
        if SourceBoneName == "":
            self.report({'ERROR'}, "Must Have a Source Bone Name Entered")
        elif DestBoneName == "":
            self.report({'ERROR'}, "Must Have a Destination Bone Name Entered")
        else:
            sourceBone = SourceArm.pose.bones[SourceBoneName]
            print("Source Bone: ", SourceBoneName)
            sourcepos = GetBonePositionWS(sourceBone, SourceArm)
            print("Source Bone Position WS: ",sourcepos)
            
            destBone = DestArm.pose.bones[DestBoneName]
            print("Destination Bone: ", DestBoneName)
            destpos = GetBonePositionWS(destBone, DestArm)
            print("Dest Bone Position WS: ", destpos)
            
            
            print("Source Bone Pose Space: ",sourcepos)
            currentDestPosPS = destBone.location.copy()
            print("Pose Space of ", destBone.name, " before move: ",currentDestPosPS)
            SetBonePositionWS(destBone, DestArm,sourcepos)
            Update()
            DestMovedtoSourcePS = destBone.location.copy()
            print("Pose Space of ", destBone.name, " after moved to source position: ",DestMovedtoSourcePS)
            SetBonePositionWS(destBone, DestArm,destpos)
            Update()
            delta = currentDestPosPS - DestMovedtoSourcePS
            print("Pose Space Delta of ", destBone.name, " : ",delta)
            bone_mapping_list[index].position_correction_factor.x = delta.x
            bone_mapping_list[index].position_correction_factor.y = delta.y
            bone_mapping_list[index].position_correction_factor.z = delta.z
            #mt = SourceArm.convert_space(pose_bone=sourceBone, 
            #    matrix=GetBoneMatrix(sourceBone), 
            #    from_space='POSE', 
            #    to_space='WORLD')
            #mt2 = mt.copy()
            #mt.translation = destpos
            #destboneinsourcebonespace = SourceArm.convert_space(pose_bone=sourceBone, 
            #    matrix=mt, 
            #    from_space='WORLD', 
            #    to_space='POSE')
            #    
            #mt2.translation = sourcepos
            #sourceboneinsourcebonespace = SourceArm.convert_space(pose_bone=sourceBone, 
            #    matrix=mt2, 
            #    from_space='WORLD', 
            #    to_space='POSE')
            #bone_mapping_list[index].position_correction_factor.x = destboneinsourcebonespace.translation.x - sourceboneinsourcebonespace.translation.x
            #bone_mapping_list[index].position_correction_factor.y = destboneinsourcebonespace.translation.y - sourceboneinsourcebonespace.translation.y
            #bone_mapping_list[index].position_correction_factor.z = destboneinsourcebonespace.translation.z - sourceboneinsourcebonespace.translation.z
            
            #bone_mapping_list[index].position_correction_factor.x = 0
            #bone_mapping_list[index].position_correction_factor.y = 0
            #bone_mapping_list[index].position_correction_factor.z = 0
            
            #ws_SourceMatrix = SourceArm.matrix_world @ GetBoneMatrix(sourceBone) 
            #ws_DestMatrix = DestArm.matrix_world @ GetBoneMatrix(destBone)

            #We get the matrix of the destination Global position moved to source arm space.
            #WStoSourceArm = SourceArm.matrix_world.inverted() @ ws_DestMatrix.translation
            #print("Source Arm Coords for Destination Bone ", destBone.name, " WS Position: ", WStoSourceArm)
            
            #mat = GetBoneMatrix(sourceBone)
            #SourceArmtoPoseBone = mat.inverted() @ WStoSourceArm
            #print("Pose Bone Coords for Destination Bone ", destBone.name, " WS Position: ", SourceArmtoPoseBone)
            
            #bone_mapping_list[index].position_correction_factor.x = SourceArmtoPoseBone.x
            #bone_mapping_list[index].position_correction_factor.y = SourceArmtoPoseBone.y
            #bone_mapping_list[index].position_correction_factor.z = SourceArmtoPoseBone.z
            
            #new_ws_DestMatrix = ws_DestMatrix.copy()
            #new_ws_DestMatrix.translation.x = ws_SourceMatrix.translation.x
            #new_ws_DestMatrix.translation.y = ws_SourceMatrix.translation.y
            #new_ws_DestMatrix.translation.z = ws_SourceMatrix.translation.z
            #mw = SourceArm.convert_space(pose_bone=sourceBone, 
                #matrix=ws_DestMatrix, 
                #from_space='WORLD', 
                #to_space='POSE')
            #mw =   ws_DestMatrix.inverted() @ new_ws_DestMatrix
            #bone_mapping_list[index].position_correction_factor.x = mw.translation.x
            #bone_mapping_list[index].position_correction_factor.y = mw.translation.y
            #bone_mapping_list[index].position_correction_factor.z = mw.translation.z
            
            #global_location = destBone.matrix @ DestArm.matrix_world 
            #final = global_location.inverted() @ finaltranslation
            #thr = destBone.matrix.inverted @ finaltranslation
            #print("final position bone space: ", mw.translation)
            #SetBonePositionWS(destBone, DestArm, sourcepos)
            #Update()
            #bone_mapping_list[index].position_correction_factor.x = destBone.location.x*(-1)
            #bone_mapping_list[index].position_correction_factor.y = destBone.location.y*(-1)
            #bone_mapping_list[index].position_correction_factor.z = destBone.location.z*(-1)
            
            #SetBonePositionWS(destBone, DestArm, destpos)
            Update()
            
def CalcRotationOffset(index):    
    scene = bpy.context.scene
    KeeMap = scene.keemap_settings 
    bone_mapping_list = scene.keemap_bone_mapping_list
    
    print('')
    print('Calc Pressed:')
    SourceArmName = KeeMap.source_rig_name
    DestArmName = KeeMap.destination_rig_name
    
    if SourceArmName == "":
        self.report({'ERROR'}, "Must Have a Source Armature Name Entered")
    elif DestArmName == "":
        self.report({'ERROR'}, "Must Have a Destination Armature Name Entered")
    else:
        SourceArm = bpy.data.objects[SourceArmName]
        DestArm  = bpy.data.objects[DestArmName]
        
        SourceBoneName = bone_mapping_list[index].SourceBoneName
        DestBoneName = bone_mapping_list[index].DestinationBoneName
        
        xferAxis = bone_mapping_list[index].bone_rotation_application_axis
        xPose = bone_mapping_list[index].bone_transpose_axis
        
        if SourceBoneName == "":
            self.report({'ERROR'}, "Must Have a Source Bone Name Entered")
        elif DestBoneName == "":
            self.report({'ERROR'}, "Must Have a Destination Bone Name Entered")
        else:
            destBone = DestArm.pose.bones[DestBoneName]
            sourceBone = SourceArm.pose.bones[SourceBoneName]
            destBoneMode = 'XYZ'
            destBone.rotation_mode = destBoneMode
            
            StartingDestBoneWSQuat = GetBoneWSQuat(destBone, DestArm)
            print("Destination Bone Starting WS")
            print(StartingDestBoneWSQuat.to_euler())
            destBoneStartPosition = destBone.rotation_euler.copy()
            #print(destBoneStartPosition)
            
            HasTwist = bone_mapping_list[index].has_twist_bone
            if HasTwist:
                TwistBoneName = bone_mapping_list[index].TwistBoneName
                TwistBone = DestArm.pose.bones[TwistBoneName]
                y =  TwistBone.rotation_euler.y
            else:
                TwistBoneName = ''
                
            CorrQuat =  mathutils.Quaternion((1,0,0,0))
            SetBoneRotation(SourceArm, SourceBoneName, DestArm, DestBoneName, TwistBoneName, CorrQuat, False, HasTwist, xferAxis,xPose)
            Update()
            
            ModifiedDestBoneWSQuat = GetBoneWSQuat(destBone, DestArm)
            print("Destination Bone After Modifying WS")
            print(ModifiedDestBoneWSQuat.to_euler())
            
            q = ModifiedDestBoneWSQuat.rotation_difference(StartingDestBoneWSQuat)
            print('Difference between before and After modification')
            print(q.to_euler())
            corrEuler = q.to_euler()
            print(math.degrees(corrEuler.x))
            print(math.degrees(corrEuler.y))
            print(math.degrees(corrEuler.z))
            print(corrEuler.to_quaternion())
            bone_mapping_list[index].CorrectionFactor.x = corrEuler.x
            bone_mapping_list[index].CorrectionFactor.y = corrEuler.y
            bone_mapping_list[index].CorrectionFactor.z = corrEuler.z
            
            destBone.rotation_euler = destBoneStartPosition
            if HasTwist:
                TwistBone.rotation_euler.y = y
                destBone.rotation_euler.y = 0
            print(destBoneStartPosition)
            
            
def GetBoneWSQuat(Bone, Arm):
    source_arm_matrix = Arm.matrix_world
    source_bone_matrix = Bone.matrix
    
    #get the source bones rotation in world space.
    source_bone_world_matrix = source_arm_matrix @ source_bone_matrix
    
    return source_bone_world_matrix.to_quaternion()
        
def SetBoneRotation(SourceArmature, SourceBoneName, DestinationArmature, DestinationBoneName, DestinationTwistBoneName, CorrectionQuat, WeShouldKeyframe, hastwistbone, xferAxis, Transpose):

    #Get the rotation of the bone in edit mode
#    SourceBoneEdit = SourceArmature.data.bones[SourceBoneName]
#    SourceBoneEditRotation = SourceBoneEdit.matrix_local.to_quaternion()
    
    #Get the rotation of the bone in edit mode
#    DestinationBoneEdit = DestinationArmature.data.bones[DestinationBoneName]
#    DestinationBoneEditRotation = DestinationBoneEdit.matrix_local.to_quaternion()
#    
#    DeltaSourceEditBoneandDestEditBone = DestinationBoneEditRotation.rotation_difference(SourceBoneEditRotation)
#    DeltaDestinationEditBoneandSourceEdit = SourceBoneEditRotation.rotation_difference(DestinationBoneEditRotation)
    
    #rotate the edit rotation quat first to armature rotation
    #ArmatureSpaceBoneEditPosition = RigArmature.rotation_quaternion * BoneEditRotation
    if(DestinationTwistBoneName == "" and hastwistbone):
        self.report({'ERROR'}, "You checked Twist Bone, but no name of bone entered!")
        hastwistbone = False
    elif hastwistbone:  
        TwistBone = DestinationArmature.pose.bones[DestinationTwistBoneName]
    destination_bone =  DestinationArmature.pose.bones[DestinationBoneName]
    sourceBone = SourceArmature.pose.bones[SourceBoneName]
    
    #Set Bone Position now that we've calculated it.
    destination_bone.rotation_mode = 'QUATERNION'
     
     #################################################
     ################## Get Source WS Quat ###########
     #################################################
    source_arm_matrix = SourceArmature.matrix_world
    source_bone_matrix = sourceBone.matrix
    
    #get the source bones rotation in world space.
    source_bone_world_matrix = source_arm_matrix @ source_bone_matrix
    
    SourceBoneRotWS = source_bone_world_matrix.to_quaternion()
    #print('Source Rotation WS Before:')
    #print(SourceBoneRotWS.to_euler())
     
     #################################################
     ################## Get Dest edit WS Quat ###########
     #################################################
    dest_arm_matrix = DestinationArmature.matrix_world
    dest_bone_matrix = destination_bone.matrix
    
    #get the DESTINATION bones rotation in world space.
    dest_bone_world_matrix = dest_arm_matrix @ dest_bone_matrix
    
    DestBoneRotWS = dest_bone_world_matrix.to_quaternion()
    #print('Destination Rotation WS Before:')
    #print(DestBoneRotWS.to_euler())
    
    DifferenceBetweenSourceWSandDestWS = DestBoneRotWS.rotation_difference(SourceBoneRotWS)
    #print('Difference Rotation')
    FinalQuat = destination_bone.rotation_quaternion.copy() @ DifferenceBetweenSourceWSandDestWS @ CorrectionQuat
    destination_bone.rotation_mode = 'XYZ'
    FinalEul = FinalQuat.to_euler()
    if Transpose == 'ZYX':
        destination_bone.rotation_euler.x = FinalEul.z
        destination_bone.rotation_euler.y = FinalEul.y
        destination_bone.rotation_euler.z = FinalEul.x
    elif Transpose == 'ZXY':
        destination_bone.rotation_euler.x = FinalEul.z
        destination_bone.rotation_euler.y = FinalEul.x
        destination_bone.rotation_euler.z = FinalEul.y
    elif Transpose == 'XZY':
        destination_bone.rotation_euler.x = FinalEul.x
        destination_bone.rotation_euler.y = FinalEul.z
        destination_bone.rotation_euler.z = FinalEul.y
    elif Transpose == 'YZX':
        destination_bone.rotation_euler.x = FinalEul.y
        destination_bone.rotation_euler.y = FinalEul.z
        destination_bone.rotation_euler.z = FinalEul.x
    elif Transpose == 'YXZ':
        destination_bone.rotation_euler.x = FinalEul.y
        destination_bone.rotation_euler.y = FinalEul.x
        destination_bone.rotation_euler.z = FinalEul.z
    else:
        destination_bone.rotation_euler = FinalEul
    
    if xferAxis == 'X':
        destination_bone.rotation_euler.y = 0
        destination_bone.rotation_euler.z = 0
    elif xferAxis == 'Y':
        destination_bone.rotation_euler.x = 0
        destination_bone.rotation_euler.z = 0
    elif xferAxis == 'Z':
        destination_bone.rotation_euler.x = 0
        destination_bone.rotation_euler.y = 0
    elif xferAxis == 'XY':
        destination_bone.rotation_euler.z = 0
    elif xferAxis == 'XZ':
        destination_bone.rotation_euler.y = 0
    elif xferAxis == 'YZ':
        destination_bone.rotation_euler.x = 0
        
    Update()
    
    if (hastwistbone):
        TwistBone.rotation_mode = 'XYZ'
        yrotation = destination_bone.rotation_euler.y
        destination_bone.rotation_euler.y = 0
        TwistBone.rotation_euler.y = math.degrees(yrotation)
        #print('Setting Twist Bone: ' + yrotation)
        #TwistBone.rotation_mode = 'QUATERNION'
        #destination_bone.rotation_mode = 'QUATERNION'
        
    Update()
    
    if (WeShouldKeyframe):
        currentFrame = bpy.context.scene.frame_current
        destination_bone.rotation_mode = 'XYZ'
        destination_bone.keyframe_insert(data_path='rotation_euler',frame=currentFrame)
        #print('keyframed' + str(currentFrame))
        if (hastwistbone):
            TwistBone.rotation_mode = 'XYZ'
            TwistBone.keyframe_insert(data_path='rotation_euler',frame=currentFrame)

def GetBoneEditRotationWorldSpace(arm, bonename):
    BoneEdit = arm.data.bones[bonename]
    BoneEditRotation = BoneEdit.matrix_local.to_quaternion()
    BoneEditWS = arm.rotation_quaternion*BoneEditRotation
    return BoneEditWS
	
####################################################################################
####################################################################################
####################################################################################
# Code for iteration through frames and applying positions and angles to rig
####################################################################################
####################################################################################
####################################################################################

class PerformAnimationTransfer(bpy.types.Operator):
    bl_idname = "wm.perform_animation_transfer"
    bl_label = "Transfer Animation from Source to Destination"

    def execute(self, context):
        scene = bpy.context.scene
        KeeMap = bpy.context.scene.keemap_settings 
        bone_mapping_list = context.scene.keemap_bone_mapping_list
        wm = bpy.context.window_manager
        
        SourceArmName = KeeMap.source_rig_name
        DestArmName = KeeMap.destination_rig_name
        KeyFrame_Every_Nth_Frame = KeeMap.keyframe_every_n_frames
        NumberOfFramesToTransfer = KeeMap.number_of_frames_to_apply
        #StartFrame = scene.frame_current
        StartFrame = KeeMap.start_frame_to_apply


        print('')
        print('Starting Transfer:')
        print('')
        #SourcArm = bpy.context.selected_objects[SourcArmName]
        #DestArm  = bpy.context.selected_objects[DestArmName]
                    
        if SourceArmName == "":
            self.report({'ERROR'}, "Must Have a Source Armature Name Entered")
        elif DestArmName == "":
            self.report({'ERROR'}, "Must Have a Destination Armature Name Entered")
        else:
            SourceArm = bpy.data.objects[SourceArmName]
            DestArm  = bpy.data.objects[DestArmName]
            
            i=0
            wm.progress_begin(0, 100)
            while (i < NumberOfFramesToTransfer):
                #scene.frame_current = StartFrame + i
                bpy.context.scene.frame_set(StartFrame + i)
                Update()
                
                #print('')
                CurrentFrame = scene.frame_current
                EndFrame =  StartFrame + NumberOfFramesToTransfer
                PercentComplete = ((CurrentFrame - StartFrame)/(EndFrame - StartFrame))*100
                update_progress("Transferring to Rig: ", PercentComplete/100.0)
                wm.progress_update(PercentComplete/100)
                #print('Working On Frame: ' + str(scene.frame_current) + ' of ' + str(EndFrame) + ' ' + "{:.1f}".format(PercentComplete) + '%')
                #print('')

                bpy.ops.wm.test_all_bones(keyframe = True)
                Update()
                i = i + KeyFrame_Every_Nth_Frame

            update_progress("Transferring to Rig: ", 1)
            wm.progress_end()
        return{'FINISHED'}
    
class KEEMAP_TestSetRotationOfBone(bpy.types.Operator): 
    """Maps a Single Bone on the Current Frame to Test Mapping""" 
    bl_idname = "wm.test_set_rotation_of_bone" 
    bl_label = "Test Bone Re-Targetting" 
    index2pose: bpy.props.IntProperty() 
    keyframe: bpy.props.BoolProperty(default = False) 
    
    def execute(self, context): 
        scene = bpy.context.scene
        if(self.index2pose == -1):
            index = scene.keemap_bone_mapping_list_index 
        else:
            index = self.index2pose
        KeeMap = bpy.context.scene.keemap_settings 
        bone_mapping_list = context.scene.keemap_bone_mapping_list
        
        #if the box is checked we're going to keyframe no matter what:
        if KeeMap.keyframe_test:
            self.keyframe = True
            
        #print('')
        #print('Test Pressed:')
        SourceArmName = KeeMap.source_rig_name
        DestArmName = KeeMap.destination_rig_name
                    
        if SourceArmName == "":
            self.report({'ERROR'}, "Must Have a Source Armature Name Entered")
        elif DestArmName == "":
            self.report({'ERROR'}, "Must Have a Destination Armature Name Entered")
        else:
            SourceArm = bpy.data.objects[SourceArmName]
            DestArm  = bpy.data.objects[DestArmName]
            
            SourceBoneName = bone_mapping_list[index].SourceBoneName
            DestBoneName = bone_mapping_list[index].DestinationBoneName
            
            xferAxis = bone_mapping_list[index].bone_rotation_application_axis
            xPose = bone_mapping_list[index].bone_transpose_axis
            
            if SourceBoneName == "":
                self.report({'ERROR'}, "Must Have a Source Bone Name Entered")
            elif DestBoneName == "":
                self.report({'ERROR'}, "Must Have a Destination Bone Name Entered")
            else:
                HasTwist = bone_mapping_list[index].has_twist_bone
                TwistBoneName = bone_mapping_list[index].TwistBoneName
                CorrectionVectorX = bone_mapping_list[index].CorrectionFactor.x
                #print(math.degrees(CorrectionVectorX))
                CorrectionVectorY = bone_mapping_list[index].CorrectionFactor.y
                #print(math.degrees(CorrectionVectorY))
                CorrectionVectorZ = bone_mapping_list[index].CorrectionFactor.z
                #print(math.degrees(CorrectionVectorZ))
                corrEul = mathutils.Euler((CorrectionVectorX, CorrectionVectorY, CorrectionVectorZ), 'XYZ')
                #print('correction Eul in:')
                #print(corrEul)
                CorrQuat = corrEul.to_quaternion()
                #print('correction in:')
                #print(CorrQuat.to_euler())
                if bone_mapping_list[index].set_bone_rotation:
                    SetBoneRotation(SourceArm, SourceBoneName, DestArm, DestBoneName, TwistBoneName, CorrQuat, self.keyframe, HasTwist, xferAxis,xPose)
                if bone_mapping_list[index].set_bone_position:
                    if bone_mapping_list[index].postion_type == "SINGLE_BONE_OFFSET":
                        corr = bone_mapping_list[index].position_correction_factor
                        gain = bone_mapping_list[index].position_gain
                        SetBonePosition(SourceArm, SourceBoneName, DestArm, DestBoneName, TwistBoneName, self.keyframe,corr.x,corr.y,corr.z,gain)
                    else:
                        dist = bone_mapping_list[index].position_pole_distance*(-1)
                        #print(dist)
                        SetBonePositionPole(SourceArm, SourceBoneName, DestArm, DestBoneName, TwistBoneName, self.keyframe, dist)
        return{'FINISHED'}
    
class KEEMAP_BoneSelectedOperator(bpy.types.Operator):
    bl_idname = "wm.bone_selected"
    bl_label = "Operator to Change Selection based on selected bone"

    @classmethod
    def poll(cls, context):
        return len(context.selected_pose_bones) > 0
    
    def execute(self, context):
        print('Checking')

        bone_mapping_list = context.scene.keemap_bone_mapping_list
        index = context.scene.keemap_bone_mapping_list_index 
        KeeMap = bpy.context.scene.keemap_settings 
        
        DestArmName = KeeMap.destination_rig_name
        if DestArmName != '':
            DestArm  = bpy.data.objects[DestArmName]
            if len(context.selected_pose_bones) > 0:
                bonename = context.selected_pose_bones[0].name
                i = 0
                for bone_settings in bone_mapping_list:
                    if bone_settings.DestinationBoneName == bonename:
                        context.scene.keemap_bone_mapping_list_index = i
                    i = i+1
        return {'FINISHED'}    
    
class KEEMAP_TestAllBones(bpy.types.Operator): 
    """Test All Bones to set there position""" 
    bl_idname = "wm.test_all_bones" 
    bl_label = "Test Set All Bone's Position"
    keyframe: bpy.props.BoolProperty(default = False) 

    def execute(self, context): 

        bone_mapping_list = context.scene.keemap_bone_mapping_list
        index = context.scene.keemap_bone_mapping_list_index 
        # CODE FOR SETTING BONE POSITIONS:
        i = 0
        for bone_settings in bone_mapping_list:
            index = i
            #print(bone_settings.name)
            bpy.ops.wm.test_set_rotation_of_bone(index2pose = index,keyframe = self.keyframe)
            Update()
            i = i+1
        return{'FINISHED'}

class KEEMAP_GetArmatureName(bpy.types.Operator):
    """If an armature is selected, get the name and populate"""
    bl_idname = "wm.get_arm_name"
    bl_label = "Get Armature Name"
    bl_options = {"REGISTER", "INTERNAL"}

    source : bpy.props.BoolProperty()

    @classmethod
    def poll(self, context):
        return context.object is not None and context.object.type == 'ARMATURE'

    def execute(self, context):
        KeeMap = bpy.context.scene.keemap_settings
        if self.source:
            KeeMap.source_rig_name = context.object.name
        else:
            KeeMap.destination_rig_name = context.object.name
        return{'FINISHED'}

class KEEMAP_GetSourceBoneName(bpy.types.Operator): 
    """If a bone is selected, get the name and popultate""" 
    bl_idname = "wm.get_source_bone_name" 
    bl_label = "Get Source Bone Name" 

    def execute(self, context): 
        scene = bpy.context.scene
        index = scene.keemap_bone_mapping_list_index 
        KeeMap = bpy.context.scene.keemap_settings 
        bone_mapping_list = context.scene.keemap_bone_mapping_list
        if len(context.selected_objects) == 1:
            rigname = context.selected_objects[0].name
            bonename = context.selected_pose_bones[0].name
        elif len(context.selected_objects) == 2:
            bonename = context.selected_pose_bones[0].name
            rig1 = context.selected_objects[0]
            if rig1.pose.bones.find(bonename) == -1:
                rigname = context.selected_objects[1].name
            else:
                rigname = context.selected_objects[0].name
        if len(context.selected_pose_bones) == 1:
            if rigname == KeeMap.source_rig_name:
                bone_mapping_list[index].SourceBoneName = bonename
            if rigname == KeeMap.destination_rig_name:
                bone_mapping_list[index].DestinationBoneName = bonename
            if bone_mapping_list[index].name == '' and rigname == KeeMap.source_rig_name:
                bone_mapping_list[index].name = bonename
        return{'FINISHED'}

class KEEMAP_AutoGetBoneCorrection(bpy.types.Operator): 
    """Auto Calculate the Bones Correction Number from calculated to current rotation.""" 
    bl_idname = "wm.get_bone_rotation_correction" 
    bl_label = "Auto Calc Correction" 

    def execute(self, context): 
        scene = bpy.context.scene
        index = scene.keemap_bone_mapping_list_index 
        CalcRotationOffset(index)
                
        return{'FINISHED'}



class KEEMAP_AutoGetBoneCorrectionPosition(bpy.types.Operator): 
    """Auto Calculate the Bones Correction Number from calculated to current position.""" 
    bl_idname = "wm.get_bone_location_correction" 
    bl_label = "Auto Calc Correction Location" 

    def execute(self, context): 
        scene = bpy.context.scene
        index = scene.keemap_bone_mapping_list_index 
        CalcLocationOffset(index)
                
        return{'FINISHED'}
        
class KEEMAP_AutoGetBoneCorrectionAllBonesPositionandRotation(bpy.types.Operator): 
    """"Auto Calculate the Bones Correction Number from calculated to current position and rotation for ALL bones.""" 
    bl_idname = "wm.calc_correct_all_bones" 
    bl_label = "Auto Calculate All Bones Rotation and Position"
    keyframe: bpy.props.BoolProperty(default = False) 

    def execute(self, context): 

        scene = bpy.context.scene
        bone_mapping_list = scene.keemap_bone_mapping_list
        index = context.scene.keemap_bone_mapping_list_index 
        # CODE FOR SETTING BONE POSITIONS:
        i = 0
        for bone_settings in bone_mapping_list:
            index = i
            print(bone_settings.name)
            CalcRotationOffset(index)
            if "pole" not in  bone_settings.name.lower():
                CalcLocationOffset(index)
            i = i+1
        return{'FINISHED'}
        
def register():
    bpy.utils.register_class(PerformAnimationTransfer)
    bpy.utils.register_class(KEEMAP_GetArmatureName)
    bpy.utils.register_class(KEEMAP_GetSourceBoneName)
    bpy.utils.register_class(KEEMAP_TestSetRotationOfBone)
    bpy.utils.register_class(KEEMAP_AutoGetBoneCorrection)
    bpy.utils.register_class(KEEMAP_AutoGetBoneCorrectionPosition)
    bpy.utils.register_class(KEEMAP_TestAllBones)
    bpy.utils.register_class(KEEMAP_BoneSelectedOperator)
    bpy.utils.register_class(KEEMAP_AutoGetBoneCorrectionAllBonesPositionandRotation)


def unregister():
    bpy.utils.unregister_class(PerformAnimationTransfer)
    bpy.utils.unregister_class(KEEMAP_GetArmatureName)
    bpy.utils.unregister_class(KEEMAP_GetSourceBoneName)
    bpy.utils.unregister_class(KEEMAP_TestSetRotationOfBone)
    bpy.utils.unregister_class(KEEMAP_AutoGetBoneCorrection)
    bpy.utils.unregister_class(KEEMAP_AutoGetBoneCorrectionPosition)
    bpy.utils.unregister_class(KEEMAP_TestAllBones)
    bpy.utils.unregister_class(KEEMAP_BoneSelectedOperator)
    bpy.utils.unregister_class(KEEMAP_AutoGetBoneCorrectionAllBonesPositionandRotation)
