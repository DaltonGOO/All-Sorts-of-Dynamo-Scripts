"""
1. Create and name a new schema
2. Set the read/write access for the schema
3. Define one or more fields of data for the schema
4. Create an entity based on the schema
5. Assign values to the fields for the entity
6. Associate the entity with a Revit element
"""
#import sys
import sys
import os
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager



import clr
clr.AddReference('System')
from System import Guid, String, Int32

doc = DocumentManager.Instance.CurrentDBDocument
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument


element = UnwrapElement(IN[0])

def createSchemaAndStoreData(doc, element): 
    """
    Create a schema and store data in a view element
    """
    TransactionManager.Instance.EnsureInTransaction(doc)
    #create a new revit guid
    schemaGuid = Guid.NewGuid()
    schemaBuilder = ExtensibleStorage.SchemaBuilder(schemaGuid)
    #set read/write access
    schemaBuilder.SetReadAccessLevel(ExtensibleStorage.AccessLevel.Public)
    schemaBuilder.SetWriteAccessLevel(ExtensibleStorage.AccessLevel.Public)
    #set the schema name
    schemaBuilder.SetSchemaName("ElementLocation")
    #add a field to the schema
    fieldBuilder = schemaBuilder.AddSimpleField("Element_Location", XYZ)
    #fieldBuilder = schemaBuilder.AddSimpleField("ElementLocation", XYZ)
    fieldBuilder.SetSpec(SpecTypeId.Length)
    #set documentation
    fieldBuilder.SetDocumentation("The coordinates of the element location")

    #create the schema
    schema = schemaBuilder.Finish()
    entity = ExtensibleStorage.Entity(schema)
    #get the field from the schema
    field = schema.GetField("Element_Location")
    #set the value of the field

    #TransactionManager.Instance.EnsureInTransaction(doc)
    #set the value of the field
    entity.Set<XYZ>(field, XYZ(int(113421541235),int(111),int(1)), UnitTypeId.Meters)
    element.SetEntity(entity)
    TransactionManager.Instance.TransactionTaskDone()
    #get the data back from the wall
    TransactionManager.Instance.EnsureInTransaction(doc)
    retrievedEntity = element.GetEntity(schema)
    retrievedEntity.Get<XYZ>(schema.GetField("Element_Location"))
    TransactionManager.Instance.TransactionTaskDone()
    return retrievedEntity.Get<XYZ>(schema.GetField("Element_Location"))

#OUT = createSchemaAndStoreData(doc, element)

OUT = (createSchemaAndStoreData(doc, element))