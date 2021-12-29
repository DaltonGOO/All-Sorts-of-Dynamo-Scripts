import sys
sys.path.append("C:\\Users\\dalto\\anaconda3\\envs\\Dynamo_210\\Lib")
sys.path.append("C:\\Users\\dalto\\OneDrive\\My Stuff\\GitHub\\All-Sorts-of-Dynamo-Scripts\\Python Module")

import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

clr.AddReference('System')
from System.Collections.Generic import List

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *


doc = DocumentManager.Instance.CurrentDBDocument
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

#Preparing input from dynamo to revit
lines = UnwrapElement(IN[0])

def find_arcs(lines):
    lines = list(lines)
    arcs = []
    for index, line in enumerate(lines):
        if line.GetType().Name == 'Arc':
            arcs.append(line)
            lines.pop(index)
    return arcs, lines
    
arcs, lines = find_arcs(lines)





#remove lines that are smaller that largest line
line_lengths = []
for line in lines:
    line_lengths.append(line.Length)

# sometimes this doesn't find the all the short lines??
max_line_length = max(line_lengths)
for line in lines:
    if line.Length < max_line_length:
        lines.remove(line)


max_line_length = max(line_lengths)
for line in lines:
    if line.Length < max_line_length:
        lines.remove(line)

#clean out lines that are similar to each other
def clean_lines(lines):
    #creating a list of lines start and end points xy coordinates to compare and remove similar lines
    lines_xy = []
    for line in lines:
        xy = [] 
        xy.append([line.StartPoint.X, line.StartPoint.Y])
        xy.append([line.EndPoint.X, line.EndPoint.Y])
        lines_xy.append(xy)
    
    #sort sublists in list
    for i in lines_xy:
        i.sort()
    
    #remove similar sublists
    templist2 = list(lines_xy) #defined new templist outside of loop to avoid modifying the list in the loop
    for index, i in enumerate(lines_xy):
        templist = templist2[index:] #starts at index of main loop to avoid checking the same line twice
        
        for index2, i2 in enumerate(templist):

            #because of the sorting the start and end point number lists get switched around. That isn't a problem just don't depend on their order for other stuff
            a1 = i[0][0] #x first line start or end
            a2 = i[0][1] #y first line start or end
            b1 = i[1][0] #x first line start or end
            b2 = i[1][1] #y first line start or end

            aa1 = i2[0][0] #x second line start or end
            aa2 = i2[0][1] #y second line start or end
            bb1 = i2[1][0] #x second line start or end
            bb2 = i2[1][1] #y second line start or end
            
            #distance between numbers
            a1_diff = abs(a1 - aa1)
            a2_diff = abs(a2 - aa2)
            b1_diff = abs(b1 - bb1)
            b2_diff = abs(b2 - bb2)


            #if the distance between the two lines is less than the max distance between the lines then remove the second line
            if a1_diff < 0.1 and a2_diff < 0.1 and b1_diff < 0.1 and b2_diff < 0.1:
                del lines[index2]
                del templist2[index2]
                #we don't break the loop because we want to check the next line in the list in case there are more similar lines
        
    return lines 
             

lines = clean_lines(lines)

#find lines point of arc that is closest to door line point
def find_closest_line(lines, arcs):
    arc = arcs[0]
    #find distence between arc enpoint and startpoint to lines startpoint and endpoint
    line_start_dist_to_arc_start = []
    line_end_dist_to_arc_start = []

    line_start_dist_to_arc_end = []
    line_end_dist_to_arc_end = []
    for line in lines:
        line_start_dist_to_arc_start.append(line.StartPoint.DistanceTo(arc.StartPoint))
        line_end_dist_to_arc_start.append(line.EndPoint.DistanceTo(arc.StartPoint))

        line_start_dist_to_arc_end.append(line.StartPoint.DistanceTo(arc.EndPoint))
        line_end_dist_to_arc_end.append(line.EndPoint.DistanceTo(arc.EndPoint))
    
    
    
    #find closest line startpoint or endpoint to arc startpoint or endpoint
    arcs_combinations = [line_start_dist_to_arc_start, line_end_dist_to_arc_start, line_start_dist_to_arc_end, line_end_dist_to_arc_end]
    #
    #this will return the index of the a list from _arcs which would tell us want points to use from the arc and line
    mins_arcs_index = None
    #lines index. This will tell us which line to use in our line list
    mins_line_index = None
    #this will tell us which point to use from the line
    temp_line_min_values = []
    temp_line_min_indexes = []
    for i in arcs_combinations:
        temp_line_min_values.append(min(i))
        temp_line_min_indexes.append(i.index(min(i)))

    #find the index of the min value in the list of min values
    min_index = temp_line_min_values.index(min(temp_line_min_values))

    #get line
    line_index = temp_line_min_indexes[min_index]
    line = lines[line_index]

    #we use this list of strings to get the point we want to use from the line and arc
    point_type_combination = [['StartPoint', 'StartPoint'], ['EndPoint', 'StartPoint'], ['StartPoint', 'EndPoint'], ['EndPoint', 'EndPoint']]
    combination = point_type_combination[min_index]
    if combination[0] == 'StartPoint':
        point = line.StartPoint
    else:
        point = line.EndPoint
    
 
    #get point from arc
    if combination[1] == 'StartPoint':
        point_from_arc = arc.StartPoint
    else:
        point_from_arc = arc.EndPoint
        
 
        
    return lines, temp_line_min_indexes, temp_line_min_values, min_index
        
        
        
        
        
        #do some action in a Transaction

OUT = find_closest_line(lines, arcs)