
import json
import os
import shutil

# Prompt user for the JSON file path
json_file_path = input("Enter the path to the JSON file: ")

# Read and parse the JSON file
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Initialize list to hold all polymesh_id values
polymesh_ids = []

# Recursive function to find all instances of "mesh_set" and extract "polymesh_id"
def find_mesh_set(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "mesh_set":
                for item in value:
                    polymesh_id = item.get("polymesh_id")
                    if polymesh_id is not None:
                        polymesh_ids.append(polymesh_id)
            else:
                find_mesh_set(value)
    elif isinstance(data, list):
        for item in data:
            find_mesh_set(item)

# Call the function to populate polymesh_ids
find_mesh_set(data)

# Define the folder containing mesh files
mesh_folder = r"F:\ai\shadowbane\ARCANE_DATA\COBJECTS\MESH"

# Copy each mesh file to the same folder as the original JSON file
json_folder = os.path.dirname(json_file_path)
for polymesh_id in polymesh_ids:
    mesh_file_path = os.path.join(mesh_folder, f"{polymesh_id}.json")
    if os.path.exists(mesh_file_path):
        shutil.copy(mesh_file_path, json_folder)
    else:
        print(f"Mesh file for polymesh_id {polymesh_id} not found.")
