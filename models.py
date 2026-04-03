# Check if the input is valid (not empty and not just whitespace)
def validate_input(name, description, location, mobile_no):
    
    if not name.strip() or not description.strip() or not location.strip() or not mobile_no.strip():
        return False
    return True

# Format the item data into a dictionary
def format_item(name, description, location, mobile_no, image):
    
    return {
        "name": name.strip(),
        "description": description.strip(),
        "location": location.strip(),
        "mobile_no": mobile_no.strip(),
        "image": image
    }