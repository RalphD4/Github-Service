

def validate_issue(data, type):
    #check json data
    match type:
        case "issue":
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
        
        case "comment":
            if "body" not in data:
                return False
            return True

        case "update":
            if not data:
                return False
            if "state" in data:
                if data["state"] not in {"closed", "open"}:
                    return False
            return True

        case _:
            return False
    
        


        
        