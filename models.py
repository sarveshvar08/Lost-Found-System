# Check if the input is valid (not empty and not just whitespace)
def validate_input(name, description):
    
    if not name.strip() or not description.strip():
        return False
    return True

# Format the item data into a dictionary
def format_item(name, description, image):
    
    return {
        "name": name.strip(),
        "description": description.strip(),
        "image": image
    }