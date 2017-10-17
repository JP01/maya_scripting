# keyRotationWithUI.py
# Provides a UI for the keyRotation script.

import maya.cmds as cmds
import functools


def createUI(pWindowTitle, pApplyCallback):
    """Create a UI for the key rotation script and display."""

    windowID = 'myWindowID'
    
    # If a window with this id already exists, close it
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
    
    # Create the window
    cmds.window(
        windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True)
    
    # Set the layout
    cmds.rowColumnLayout(
        numberOfColumns=3, 
        columnWidth=[ (1,75), (2,60), (3,60) ],
        columnOffset=[ (1,'right',3) ])
    
    # Row 1
    cmds.text(label='Time Range:')

    startTimeField = cmds.intField(
        value=cmds.playbackOptions(q=True, minTime=True))
    
    endTimeField = cmds.intField(
        value=cmds.playbackOptions(q=True, maxTime=True))
    
    # Row 2
    cmds.text(label='Attribute:')
    
    targetAttributeField = cmds.textField(text='rotateY')
    
    cmds.separator(h=10, style='none')
    
    # Row 3 - Create an empty row of seperators
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    
    # Row 4
    cmds.separator(h=10, style='none')
    
    cmds.button(
        label='Apply', 
        command=functools.partial(
            pApplyCallback, startTimeField, endTimeField,argetAttributeField))
    
    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
    
    cmds.button(label='Cancel', command=cancelCallback)
    
    # Display the window!
    cmds.showWindow()


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
    
    
    
def applyCallback(pStartTimeField, pEndTimeField, pTargetAttributeField, *pArgs):
    """"""

    # Get our values from the input fields
    startTime = cmds.intField(pStartTimeField, query=True, value=True)
    endTime = cmds.intField(pEndTimeField, query=True, value=True)
    targetAttribute = cmds.textField(
        pTargetAttributeField, query=True, text=True)
    
    # make sure everything is correct in console log
    print 'Start Time: %s' % (startTime)
    print 'End Time: %s' % (endTime)
    print 'Attribute: %s' % (targetAttribute)
    
    # access current user transform object selection
    selectionList = cmds.ls(selection=True, type='transform')
    
    # Rotate each object in the list
    for objectName in selectionList:
        keyFullRotation(objectName, startTime, endTime, targetAttribute)
    

createUI('My Title', applyCallback)
    