# keyRotation.py
# Translates a number of objects 360 degrees around an axis.
# Instrucitons:
#   1. Select the objects which should rotate around the axis.
#   2. Run the script.

import maya.cmds as cmds


def keyFullRotation(pObjectName, pStartTime, pEndTime, pTargetAttribute):
    """Create a keyframe rotation animation for the specified object.

    Rotates the pObjectName around an axis pTargetAttribute, 
    between pStartTime and pEndTime.
    """ 

    # Remove any animations within the timerange
    cmds.cutKey(
        pObjectName, time=(pStartTime, pEndTime), attribute=pTargetAttribute)
    
    # Sets the target values for start and end points
    cmds.setKeyframe(
        pObjectName, time=pStartTime, attribute=pTargetAttribute, value=0)
    cmds.setKeyframe(
        pObjectName, time=pEndTime, attribute=pTargetAttribute, value=360)
    
    # Ensure the rotation has linear velocity
    cmds.selectKey(pObjectName, time=(pStartTime, pEndTime), 
        attribute=pTargetAttribute, keyframe=True)
    cmds.keyTangent(inTangentType='linear', outTangentType='linear')
    

selectionList = cmds.ls(selection=True, type='transform')

if len(selectionList) >= 1:
    
    startTime = cmds.playbackOptions(query=True, minTime=True)
    endTime = cmds.playbackOptions(query=True, maxTime=True)
    
    for objectName in selectionList:

        keyFullRotation(objectName, startTime, endTime, 'rotateY')

else:
    print 'Please select at least one object'