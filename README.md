# Keemap-Blender-Rig-ReTargeting-Addon
Blender Rig Retargeting Addon allows mapping motions of one rig to another.  Works with ANY rig and allows user to map bones from one rig to another and save mapping files out to hard drive.  This script is tested and working on blender 2.83, if a newer version of blender breaks the script I'm sorry.

Installation Procedure:
Download the zip file in the root folder NOT the entire source code tree.  Go to Blender-->edit(pull down from menus at top)--> Preferences, then click on the add ons button on the left of the ui.  Click on the Install button.  Select the zip file you have downloaded.  When the script shows up on the list check the box to enable it.  Make certain you DO NOT download this entire source code tree as a zip and try and install that, if you do, make sure to unzip it until you get to the file 'KeeMap Rig Transfer Addon.zip' and DO NOT UNZIP THIS FILE.  You must select this ZIP file still zipped to install into blender.

Tutorial:
Here is a tutorial video with instructions on exactly how to use the script:

https://youtu.be/EG-VCMkVpxg

UI:

![Image of the Blender UI](https://github.com/nkeeline/Keemap-Blender-Rig-ReTargeting-Addon/blob/main/Images/KeeMapUI.jpg)

In the above image is the UI for the GUI in blender when the script is installed.

## Transfer Settings

![Image of the Blender UI](https://github.com/nkeeline/Keemap-Blender-Rig-ReTargeting-Addon/blob/main/Images/TransferSettings.jpg)

**Starting Frame**: When the 'Transfer Animation from Source to Destination Character' button is pressed this is the starting frame in the timeline to start applying the rig modifications from the source to the destination.

**Number of Samples**: This will be the number of frames in the timeline to transfer.  This is timeline units so if you put a start from of 10 and a number of samples of 20, then the transfer will start at frame 10 and continue until it gets to 30.

**KeyFrame Number**: this is the number of frames to wait between each keyframe. so in the previous example with a start frame of 10 and a number of samples of 20 and a Keyframe number of 5 you will get a transfer and keyframe at 10,15,20,25 and 30.

**Source Rig Name**: Place the Name of the armature that is already keyframed with the animation you wish to transfer.

**Destination Rig Name**:   Place the name of the armature that you will map all of the tranformations of the source rig on to.

**Bone Mapping File**:  Browse to an existing or put the name of a file in this location using the browse button to save your bone mapping work to or read from.

**Read in Bone Mapping File**: press this button to read in all settings from the file to your current settings.  This will BLOW AWAY all settings in the file and replace them with the current settings you have.  EVERYTHING in the KeeMap gui is saved to the file including all check boxes and text fields for both bones and start frames etc.

**Save Bone Mapping File**:  Press this button to save out all bones and their mapping as well as all other settings you've made in the gui to the selected Bone Mapping File.

**Transfer Animation from Source to Destination Character**:  Press this button to transfer an animation from the start frame until the number of samples has been reached.  For example with a start frame of 10 and a number of samples of 20 and a Keyframe number of 5 you will get a transfer and keyframe at 10,15,20,25 and 30.  This transfer can take some time.  A percent complete is printed to the console so you can watch its progress.  Select toggle system console in blender to see this, otherwise just wait a while.


## Bone Mapping:


![Image of the Blender UI](https://github.com/nkeeline/Keemap-Blender-Rig-ReTargeting-Addon/blob/main/Images/BoneMapping.jpg)

**Bone List**: The bone list is a section that contains each bone map.  When you click 'New' it will create a new bone mapping and it's settings will display below.  You can create as many bone maps as you like.  Each bone map will get run IN ORDER when the Transfer Animation button is pressed.  When Rotation is transferred from one bone to another all of it's children will move.  Therefore this list should start with parents and move to the children so no bones are moved erroneously..

**New**: this will add a new bone to the list.

**Remove**: this will remove the selected bone from the list.

**Up**: this moves the selected bone up one in the list making this bone get operated on prior to all bones below it.

**Down**: this will move a bone down the list causing it to be acted on after all bones above it.

**name**: this is a use setable name for the bone to help you identify it.  It can be blank or anything you like and will not effect how the mapping or transfer is done.

**Source Bone Name**:  this is the name of the bone from the source armature from which to get the information for the transfer of rotation or location.

**Destination Bone Name**:  this is the name of the destination bone to which the tranformation will be applied.

**Get Name**:  Press this button to get the selected bones name and auto populate the source or destination bone names for you.  The Destination Rig Name and the Source Rig Names will be used to auto detect which field to place the bone's name into source or destination.  If the name field is empty and you select a source bone, it will be auto populated too for convenience, but if you ever change the name it will not be updated by this button.  Get Name will error if the source or destination rig name is wrong or missing.

**Select**:  This button will select the bonemapping automatically based on the bone that is selected on the destination rig in blender.  This way when you are tweaking settings you can click on the bone on the rig, press this button and the correct bone mapping will be auto selected for you.

**KeyFrame This Bone**:  Select this check box to keyframe this bone.  Unchecking this box will cause this bones rotation and position to NOT be keyframed when any process is run.  Basically this will disable this bone, but may be useful if you want to position some bone prior to positioning and keyframing another.  Not sure why you would want to do this, but this check box is there in case it is needed.

**Set Rotation of Bone**:  Check this box to set a destination bones global rotation data with the source bones global rotation.

**Apply To Axis**:  select which axis to apply the rotation, you have the option of limit the rotation modification to only a few axis of the bone.  In almost all circumstances leave this at 'XYZ'

**Transpose Axis**:  This should never be used, but allows you to take the XYZ from bone and move where the data goes.  I put this in the script just in case some day it is needed, hopefully never.

**Correction Rotation**:  After the bone is positioned globally from the source bone this is the additional rotation to move the bone.  Say your character limbs are disappearing inside it's body because the source rig was skinnier and the large characters arms need to angle outward more.  rotate the destination characters arms until they are more angled out and note which axis you did it in and then put those values in the correction field to correct the problem.

**Calc correction**:  Use this button at your own risk, but basically if you press the test button to position the bone, you can correct the bones position in the 3d view then press this button to 'auto' populate the correction factor with your corrected values.  This button hasn't been tested fully and may have some use, but I recommend saving your bone mapping file prior to using it and if doesn't do what you want read the file back to put the values back and give yourself an undo.

**Set Position of Bone**: Typically this is only used on the 'root' bone of a destination armature to position the character in the same locaiton as the source character.

**Test**:  Press this to position the destination bone according to your settings to see what your settings do.   VERY USEFUL, use this constantly to test everything as you map all the bones in your character.

**Test All**: this is the same as selecting each bone in the bone list in turn and pressing the 'Test' button.

**KeyFrame Test**:  This will keyframe what you you test.  In essence you can move the timeline along and with this checkbox checked, press the test buttons and it will keyframe each test you do.  In this way you can manually run a transfer putting the keyframes manually exactly where you want them.
