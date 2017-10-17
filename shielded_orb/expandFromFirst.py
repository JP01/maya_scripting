# expandFromFirst.py
# Expands and contracts the selected objects from a central object.
# Uses an expression on a point constraint.
# Instructions:
#   1. Select the central object.
#   2. Select all the other objects which are to be transformed.
#   3. Run the script. 

import maya.cmds as cmds

selectionList = cmds.ls(orderedSelection=True, type='transform')

if len(selectionList) >= 2:
    
    # Remove the first item from the list and store it
    targetName = selectionList[0]
    selectionList.remove(targetName)
    
    # Create a unique group using the remaining selection
    locatorGroupName = cmds.group(empty=True, name='expansion_locator_grp#')
    
    # Create an expansion variable 
    maxExpansion = 100
    newAttributeName = 'expansion'
    
    # if the attr doesn't exist, add to target
    if not cmds.objExists('%s.%s' % (targetName, newAttributeName)):
        
        cmds.select(targetName) 

        # not exactly pep8-compliant but saves a bit of room!
        cmds.addAttr(longName=newAttributeName, shortName='exp', 
                     attributeType='double', min=0, max=maxExpansion,            
                     defaultValue=maxExpansion, keyable=True)
    
    # iterate over each object in the list
    for objectName in selectionList:
        # obtain the coordinate position of the object
        coords = cmds.getAttr('%s.translate' % (objectName))[0]
        
        # create a locator at the same position with a name and number
        locatorName = cmds.spaceLocator(
          position=coords, name='%s_loc#' % (objectName))[0]
        
        # Center locator pivot
        cmds.xform(locatorName, centerPivots=True)
        
        # Group the locators
        cmds.parent(locatorName, locatorGroupName)
        
        # Constrain the object between the target and its locator
        pointConstraintName = cmds.pointConstraint(
          [targetName, locatorName], objectName, 
          name='%s_pointConstraint#' % (objectName))[0]
        
        # Create an expression for expand/contract 
        cmds.expression(alwaysEvaluate=True, 
                        name='%s_attractWeight' % (objectName),
                        object=pointConstraintName,
                        string='%sW0=%s-%s.%s' % (
                          targetName, maxExpansion, targetName, newAttributeName))
        
        # Connect value of the expansion attr to point constraint locator weight
        cmds.connectAttr(
          '%s.%s' % (targetName, newAttributeName),        # source
          '%s.%sW1' % (pointConstraintName, locatorName))  # destination
        
    
    # Center locator group's pivot
    cmds.xform(locatorGroupName, centerPivots=True)
    
else:
    print 'Please select two or more objects.'
