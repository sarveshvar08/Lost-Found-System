import csv
import os

FILE_NAME = "data_files.csv"

# Save item data to CSV
def save_item(item):
    
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ["name", "description", "image"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only once
        if not file_exists:
            writer.writeheader()

        writer.writerow(item)

# Read items from CSV and return as a list of dictionaries
def read_items():

    items = []

    if not os.path.exists(FILE_NAME):
        return items

    with open(FILE_NAME, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            items.append({
                "name": row.get("name", ""),
                "description": row.get("description", ""),
                "image": row.get("image", "")
            })

    return items

# Search items by keyword in name or description
def search_items(keyword):
   
    results = []
    items = read_items()

    keyword = keyword.lower()

    for item in items:
        if keyword in item["name"].lower() or keyword in item["description"].lower():
            results.append(item)

    return results