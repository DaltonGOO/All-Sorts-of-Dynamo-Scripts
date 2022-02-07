#Copy get all elements from a linked Revit file

import clr

#import Revit api
clr.AddReference('RevitAPI')
import Autodesk
#from Autodesk.Revit.DB import *

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#import document manager
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager

#get current document 
def get_current_document():
    doc = DocumentManager.Instance.CurrentDBDocument
    uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
    doc = uidoc.Document
    return doc
#get all links in current revit model
def get_all_links_in_current_revit_model():
    doc = DocumentManager.Instance.CurrentDBDocument
    uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
    doc = uidoc.Document
    #get all links in current model
    links = doc.GetElement(doc.ActiveView.RevitLinkInstanceId)
    return links
def get_all_revit_links_in_current_document():
    doc = DocumentManager.Instance.CurrentDBDocument
    uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
    doc = uidoc.Document
    #get all revit links
    revit_links = doc.GetElement(doc.ActiveView.RevitLinkInstanceId)
    return revit_links

#get all elements of a specific category from a linked Revit file
def get_all_elements_from_linked_file(category, file_path):
    doc = DocumentManager.Instance.CurrentDBDocument
    uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
    doc = uidoc.Document
    #get the linked file
    linked_file = doc.Application.OpenLinkedFile(file_path)
    #get the linked document
    linked_doc = DocumentManager.Instance.CurrentDBDocument
    #get all elements of a specific category from the linked document
    elements = list(linked_doc.GetCategoryElements(category))
    #close the linked file
    linked_file.Close(True)
    return elements

#get all elements of a specific category in active view
def get_all_elements_in_active_view(category):
    filter = ElementCategoryFilter(category)


#create triangle of consective odd numbers
def create_triangle(n):