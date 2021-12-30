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
lines_input = UnwrapElement(IN[0])

OUT = []


#find arcs in list of lines
def find_arcs(lines):
    lines = list(lines)
    arcs = []
    temp_lines = []
    for index, line in enumerate(lines):
        if line.GetType().Name == 'Arc':
            arcs.append(line)
            lines.pop(index)
    #check to see if there are more than one arc and if so separate them into their own lists and duplicate the lines
    if len(arcs) > 1:
        for arc in arcs:
            temp_lines.append(lines)
        return arcs, temp_lines
    else:
        return arcs, lines


#flatten arc list to one list
def flatten_list_arcs(arcs):
    flat_list = []
    for i in arcs:
        if isinstance(i, list):
            for j in i:
                flat_list.append(j)
        else:
            flat_list.append(i)
    return flat_list

#flatten lines list to one list
def flatten_list_lines(lines):
    flat_list = []
    for i in lines:
        if isinstance(i, list):
            for j in i:
                flat_list.append(j)
        else:
            flat_list.append(i)
    return flat_list

arcs = []
lines = []

for i in lines_input:
    a, l = find_arcs(i)
    arcs.extend(flatten_list_arcs(a))
    #check to see if i is a list of list
    if isinstance(l[0], list):
        lines.extend(l)
    else:
        lines.append(l)

#duplicate lines to a new list to maybe use for creation of rooms    
door_and_frame = lines[:]

#remove lines that are smaller that largest line
def remove_small_lines(lines):
    #find largest line
    largest_line = lines[0]
    for line in lines:
        if line.Length > largest_line.Length:
            largest_line = line
    
    #remove lines that are smaller than largest line
    lines = [l for l in lines if l.Length > largest_line.Length/1.5]

    return lines



main_lines = []
for i in lines:
    i = remove_small_lines(i)
    main_lines.append(i)



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
        templist = templist2[index+1:] #starts at index of main loop to avoid checking the same line twice
        
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
            if a1_diff < 0.01 and a2_diff < 0.01 and b1_diff < 0.01 and b2_diff < 0.01:
                try:
                    del lines[index2]
                    del templist2[index2]
                except:
                    pass
                #we don't break the loop because we want to check the next line in the list in case there are more similar lines
        
    return lines 


#clean out lines that are similar to each other
cleaned_lines = []
for i in main_lines:
    i = clean_lines(i)
    cleaned_lines.append(i)


#find lines point of arc that is closest to door line point
def find_doorway_points(lines, arc):
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

    #get point from line and return opposite point
    if combination[0] == 'StartPoint':
        point_from_line = line.EndPoint
    else:
        point_from_line = line.StartPoint
    
 
    #get point from arc  and return opposite point
    if combination[1] == 'StartPoint':
        point_from_arc = arc.EndPoint
    else:
        point_from_arc = arc.StartPoint
        
    #draw line from line and arc point to create the doorway line
    doorway_line = line.ByStartPointEndPoint(point_from_line, point_from_arc)
        
    return point_from_line, point_from_arc, line, arc, doorway_line


#find lines point of arc that is closest to door line point
for l,a in zip(cleaned_lines, arcs):
    point_from_line, point_from_arc, line, arc, doorway_line = find_doorway_points(l, a)
    OUT.append([point_from_line, point_from_arc, line, arc, doorway_line])
OUT.append(door_and_frame) 
    
      