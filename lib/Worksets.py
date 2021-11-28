
#get all user worksets from doc and return list
def return_user_worksets(doc):
    collector = FilteredWorksetCollector(doc)
    worksets = collector.ToWorksets()
    user_worksets = []
    for i in worksets:
        if i.Kind == WorksetKind.UserWorkset:
            user_worksets.append(i)
    return user_worksets


#check to see if input is a list and if it is, return list and if not return list
def check_list(input):
    if isinstance(input, list):
        return input
    else:
        return [input]


#create new worksets in Revit
def create_workset(doc, name):
    ws = Workset.Create(doc, name)
    return ws.Name


#clean up strings for workset creation
def clean_string(string):
    string = string.replace(' ', '_')
    string = string.replace('/', '_')
    string = string.replace('\\', '_')
    string = string.replace('-', '_')
    string = string.replace('(', '_')
    string = string.replace(')', '_')
    string = string.replace('.', '_')
    string = string.replace('&', '_')
    string = string.replace('%', '_')
    string = string.replace('#', '_')
    string = string.replace('!', '_')
    string = string.replace('@', '_')
    string = string.replace('$', '_')
    string = string.replace('^', '_')
    string = string.replace('*', '_')
    string = string.replace('+', '_')
    string = string.replace('=', '_')
    string = string.replace('~', '_')
    string = string.replace('`', '_')
    string = string.replace('<', '_')
    string = string.replace('>', '_')
    string = string.replace('?', '_')
    string = string.replace('|', '_')
    string = string.replace('{', '_')
    string = string.replace('}', '_')
    return string 


#check to see if workset exists and if the workset is not read only
def check_workset(doc, name, worksets):
    for i in worksets:
        if i.Name == name:
            return True
    return False
    

#create workset from element category name
def create_workset_from_category(doc, elements):
    worksets = return_user_worksets(doc)
    new_worksets = []
    for workset_name in elements:
        if check_workset(doc, workset_name, worksets) == False:
            workset = create_workset(doc, workset_name)
            new_worksets.append(workset)
    return new_worksets


#set worksets for elements
def set_workset(doc, elements):
    worksets = return_user_worksets(doc)
    for i in elements:
        #check to see if element workset property is read only
        for p in i.GetOrderedParameters():
            if p.Definition.Name == "Workset":
                if p.IsReadOnly == False:
                    for j in worksets:
                        if clean_string(i.Category.Name) == j.Name:
                            i.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).Set(int(j.Id.ToString()))
                            break
                
    return elements