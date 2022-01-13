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
import uuid
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

#revit 2022
#set SetUnitType was deprecated 
def createSchemaAndStoreData_2022(doc, element): 
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
    entity.Set<XYZ>(field, XYZ(int(113421541235),int(111),int(1)), UnitTypeId.Inch)
    element.SetEntity(entity)
    TransactionManager.Instance.TransactionTaskDone()
    #get the data back from the wall
    TransactionManager.Instance.EnsureInTransaction(doc)
    retrievedEntity = element.GetEntity(schema)
    retrievedEntity.Get<XYZ>(schema.GetField("Element_Location"))
    TransactionManager.Instance.TransactionTaskDone()
    return retrievedEntity.Get<XYZ>(schema.GetField("Element_Location"))

#revit 2020
def createSchemaAndStoreData_2021(doc, element): 
    """
    Create a schema and store data in a view element
    """
    TransactionManager.Instance.EnsureInTransaction(doc)
    #Create GUID from a string

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
    fieldBuilder.SetUnitType(UnitType.UT_Length)
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
    entity.Set(field, XYZ(1,2,3), DisplayUnitType.DUT_DECIMAL_FEET)
    element.SetEntity(entity)

    TransactionManager.Instance.TransactionTaskDone()
    return 

#get schemas from the element
def getSchemasFromElement(element):
    """
    Get the schemas from the element
    """
    TransactionManager.Instance.EnsureInTransaction(doc)
    #get the schemas from the element
    schemas = element.GetEntitySchemaGuids()
    #get the schema names from the schemas
    schemaNames = [ExtensibleStorage.Schema.Lookup(schema).SchemaName for schema in schemas]

    for index,i in enumerate(schemaNames):
        if i == "ElementLocation":
            schemaGuid = schemas[index]
            schema = ExtensibleStorage.Schema.Lookup(schemaGuid)
            TransactionManager.Instance.TransactionTaskDone()
            return schema
            break
        else:
       		return None
    


#get value of element location from the schema
def getValueFromSchema(element, schema):
    """
    Get the value from the schema
    """
    if schema is not None:
        TransactionManager.Instance.EnsureInTransaction(doc)
	    #get the value from the schema
        fieldType = schema.GetField("Element_Location").GetType()
        t = schema.GetField("Element_Location")
        value = element.GetEntity(schema).Get[t.ValueType](schema.GetField("Element_Location"),DisplayUnitType.DUT_DECIMAL_FEET)
	    
	    #get the value from the schema
        TransactionManager.Instance.TransactionTaskDone()
        return value
    else:
        return "There is no schema to get the value from"
    

schema = getSchemasFromElement(element)

def deleteSchemaFromElement(element, schema):
    """
    Delete the schema from the element
    """
    if schema is not None:
        TransactionManager.Instance.EnsureInTransaction(doc)
        #delete the schema from the element
        element.DeleteEntity(schema)
        TransactionManager.Instance.TransactionTaskDone()
        return "Schema deleted"
    else:
        return "There is no schema to delete"

OUT = getValueFromSchema(element, schema)


