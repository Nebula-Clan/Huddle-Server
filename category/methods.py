from .models import categories

def categoryid_mapper(category_id):
    for category in categories:
        if category[0].lower() == category_id.lower():
            return category[1]
    return None

def categoryname_mapper(category_name):
    for category in categories:
        if category[1].lower() == category_name.lower():
            return category[0]
    return None 