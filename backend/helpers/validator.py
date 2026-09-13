

def validate_issue(data):
    #check json data

    #title exists
    if "title" not in data: 
        return False 

    #title is a string
    if not isinstance(data["title"], str): 
        return False

    #if labels exists, should be a list of strings
    if "labels" in data:
        if not isinstance(data["labels"], list):
            return False
        if not all(isinstance(label, str) for label in data["labels"]):
            return False

    return True
    
        


        
        