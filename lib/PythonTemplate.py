"""
Dynamo Core Assemblies: https://www.nuget.org/packages/DynamoVisualProgramming.Core/2.13.1.3887
Revit API: https://www.revitapidocs.com/2020/d4648875-d41a-783b-d5f4-638df39ee413.htm
"""

import sys
sys.path.append("C:\\Users\\dalto\\anaconda3\\envs\\Dynamo_2022\\Lib")
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

doc = DocumentManager.Instance.CurrentDBDocument
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

#Preparing input from dynamo to revit
element = UnwrapElement(IN[0])

#Do some action in a Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

TransactionManager.Instance.TransactionTaskDone()

OUT = element