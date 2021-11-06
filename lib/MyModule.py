import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
from math import sin

from collections import OrderedDict


def hellowWorld():
    return "hello world!"


def distinct(seq):
    return list(OrderedDict.fromkeys(seq))


def boolean_to_string(b):
    return str(b)


def snail(array):
    OUT = []
    while array:
        if array:
            for i in array.pop(0):
                OUT.append(i)
        if array:
            for i in array:
                OUT.append(i.pop(-1))
        if array:
            for i in array.pop(-1)[::-1]:
                OUT.append(i)
        if array:
            for i in array[::-1]:
                OUT.append(i.pop(0))
    return OUT

# Load the Python Standard and DesignScript Libraries

# The inputs to this node will be stored as a list in the IN variables.


# Place your code below this line
def dynamoSine(freq = 0, length = 2):
    """
    This is a simple function for visualizing the sin equation using dynamo objects.
    """
    points = []
    if length <= 1:
        return "The length must be greater than 1."
    else:    
        for i in range(length):
            x = 5 * i
            z = freq * sin(i)
            points.append(Point.ByCoordinates(x,0,z))
        curve = NurbsCurve.ByPoints(points)
        return curve
