
import os
import json

# Function to load a JSON file and return its content
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to recursively combine JSON data
def combine_json_data(file_path, base_dir):
    combined_data = load_json(file_path)
    
    # Check for rune_body_parts and recursively combine them if present
    if 'rune_body_parts' in combined_data:
        combined_data['rune_body_parts'] = [combine_json_data(os.path.join(base_dir, 'RENDER', f"{part}.json"), base_dir) for part in combined_data['rune_body_parts']]
    
    # Check for render_children and recursively combine them if present
    if 'render_children' in combined_data:
        combined_data['render_children'] = [combine_json_data(os.path.join(base_dir, 'RENDER', f"{child}.json"), base_dir) for child in combined_data['render_children']]
    
    # TODO: Add other conditions for MOTION and SKELETON folders based on their relationships, which will be similar to above
    
    return combined_data

# Loop through all top-level JSON files and generate combined JSON files
# Filtering out folders like 'RENDER', 'TEXTURE', 'MOTION', 'SKELETON'
extract_dir = '.\ARCANE_DATA\COBJECTS'
actual_dir = '.\ACTUAL'
os.makedirs(actual_dir, exist_ok=True)
top_level_files = [f for f in os.listdir(extract_dir) if not f.endswith('/')]

for file_name in top_level_files:
    try:
        combined_data = combine_json_data(os.path.join(extract_dir, file_name), extract_dir)
        
        # Save the combined JSON into ACTUAL folder
        output_file_path = os.path.join(actual_dir, f"{combined_data['obj_name']}.json")
        with open(output_file_path, 'w') as f:
            json.dump(combined_data, f, indent=4)
    except Exception as e:
        print(f"Skipping {file_name} due to an error: {e}")
