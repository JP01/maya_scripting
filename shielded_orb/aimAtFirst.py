# aimAtFirst.py
# Note: Requires Preferences->Selection->Track Selection order enabled
# Instructions:
#     1. Select an object to point all other objects towards.
#     2. Ctrl+select all the other objects which you want to point towards
#		 the first.
#     3. Run the script

import maya.cmds as cmds

selectionList = cmds.ls(orderedSelection=True)

if len(selectionList) >= 2:
    
    print 'Selected items: %s' % (selectionList)
    
    # remove and store the first item from the list
    targetName = selectionList[0]
    selectionList.remove(targetName)

    # aim the other objects in the list towards the first
    for objectName in selectionList:
        print 'Constraining %s towards %s' % (objectName, targetName)
        cmds.aimConstraint(targetName, objectName, aimVector=[0,1,0])
    
else:
    print 'Please select two or more objects.'
    