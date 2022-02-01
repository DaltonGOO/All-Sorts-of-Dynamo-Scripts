import sys
sys.path.append("C:\\Users\\dalto\\anaconda3\\envs\\Dynamo_210\\Lib")
sys.path.append("C:\\Users\\dalto\\OneDrive\\My Stuff\\GitHub\\All-Sorts-of-Dynamo-Scripts\\Python Module")

import clr




clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Line, Vector, Geometry

#Preparing input from dynamo to revit
cuboids = UnwrapElement(IN[0])
points = UnwrapElement(IN[1])
geom = UnwrapElement(IN[2])
#Do some action in a Transaction

lines = []
xy = [-1,1]

for p,c in zip(points, cuboids):
	sub = []
	for n in xy:
		l1 = Line.ByStartPointDirectionLength(p, Vector.ByCoordinates(n,0,0), c.Width/2)
		l2 = Line.ByStartPointDirectionLength(p, Vector.ByCoordinates(0,n,0), c.Length/2)
		sub.extend((l1,l2))	
	lines.append(sub)

OUT = []
#split geometry into multiple surfaces
for g, l in zip(geom, lines):
    sub = []
    for i in l:
        split_geom = Geometry.Split(g, i)
        if len(split_geom) > 1:
            sub.append(split_geom[0])
        
    OUT.append(sub)
    

