import json

with open(r'W3C_WoT_Thing_Description.jsonld') as file:
    document = json.load(file)


def find_item(item_name):
    try:
        item_name = item_name.replace(" ", "")
        for item in document["@type"]:
            item = item.lower()
            if item_name in item:
                return True
    except Exception as e:
        return False
    return False


def find_action(do, item):
    try:
        do = do.replace(" ", "")
        for action in document["actions"]:
            action_lower = action.lower()
            if (item in action_lower) and (do in document["actions"][action]["@type"].lower()):
                return "You should take action {} with type of {}".format(action, document["actions"][action]["@type"])
    except Exception as e:
        return ""
    return ""


def find_relationship_items(item1, item2):
    try:
        for property_name in document["properties"]:
            property_name_lower = property_name.lower()
            if item1 in property_name_lower:
                id_lower = document["properties"][property_name]["isPropertyOf"]["@id"].lower()
                if item2 in id_lower:
                    return True
    except Exception as e:
        return False
    return False


def find_data_type(item):
    try:
        for property_name in document["properties"]:
            property_name_lower = property_name.lower()
            if item in property_name_lower:
                return "The data type is {}".format(document["properties"][property_name]["properties"][property_name]["type"])
    except Exception as e:
        return ""
    return ""
