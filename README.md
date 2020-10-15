# Keemap-Blender-Rig-ReTargeting-Addon
Blender Rig Retargeting Addon allows mapping motions of one rig to another.  Works with ANY rig and allows user to map bones from one rig to another and save mapping files out to hard drive.  This script is tested and working on blender 2.83, if a newer version of blender breaks the script I'm sorry.

Installation Procedure:
Download the zip file in the root folder NOT the entire source code tree.  Go to Blender-->edit(pull down from menus at top)--> Preferences, then click on the add ons button on the left of the ui.  Click on the Install button.  Select the zip file you have downloaded.  When the script shows up on the list check the box to enable it.

UI:

![Image of the Blender UI](https://github.com/nkeeline/Keemap-Blender-Rig-ReTargeting-Addon/blob/main/Images/KeeMapUI.jpg)

In the above image is the UI for the GUI in blender when the script is installed.

# Transfer Settings

Starting Frame: When the 'Transfer Animation from Source to Destination Character' button is pressed this is the starting frame in the timeline to start applying the rig modifications from the source to the destination.

Number of Samples: This will be the number of frames in the timeline to transfer.  This is timeline units so if you put a start from of 10 and a number of samples of 20, then the transfer will start at frame 10 and continue until it gets to 30.

Mouth KeyFrame Number: this is the number of frames to wait between each keyframe. so in the previous example with a start frame of 10 and a number of samples of 20 and a Keyframe number of 5 you will get a transfer and keyframe at 10,15,20,25 and 30.

Source Rig Name: Place the Name of the armature that is already keyframed with the animation you wish to transfer.

Destination Rig Name:   Place the name of the armature that you will map all of the tranformations of the source rig on to.

Bone Mapping File:  Browse to an existing or put the name of a file in this location using the browse button to save your bone mapping work to or read from.

Read in Bone Mapping File: press this button to read in all settings from the file to your current settings.  This will BLOW AWAY all settings in the file and replace them with the current settings you have.  EVERYTHING in the KeeMap gui is saved to the file including all check boxes and text fields for both bones and start frames etc.

Save Bone Mapping File:  Press this button to save out all bones and their mapping as well as all other settings you've made in the gui to the selected Bone Mapping File.

Transfer Animation from Source to Destination Character:  Press this button to transfer an animation from the start frame until the number of samples has been reached.  For example with a start frame of 10 and a number of samples of 20 and a Keyframe number of 5 you will get a transfer and keyframe at 10,15,20,25 and 30.  This transfer can take some time.  A percent complete is printed to the console so you can watch its progress.  Select toggle system console in blender to see this, otherwise just wait a while.


# Bone Mapping:

