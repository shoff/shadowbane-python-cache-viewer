import json
import os


# Prompt user for the folder path containing JSON files to process
folder_path = r"F:\ai\shadowbane\ARCANE_DATA\COBJECTS"
full_path = ""

# Loop through every JSON file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        try:
            # Construct the full path to the JSON file
            full_path = os.path.join(folder_path, filename)
            
            # Rest of the processing logic remains the same, but now applied to each file in the folder
            # ... (this will include all the existing logic for loading, parsing, and saving JSON data)
            
        except FileNotFoundError:
            print(f"File {filename} not found. Skipping.")
        except json.JSONDecodeError:
            print(f"Invalid JSON format in {filename}. Skipping.")
            

    # Initialize variables to hold extracted values
    obj_name = ""
    body_part_renders = []

    # Read and parse the JSON file
    try:
        with open(full_path, 'r') as f:
            data = json.load(f)
            
        # Step 2: Search for 'obj_name' and note its value
        obj_name = data.get("obj_name", "")
        if obj_name == "":
            print("obj_name not found in JSON.")
            exit()
            
        # Step 3: Search for 'rune_body_parts' array and extract 'body_part_render' values
        rune_body_parts = data.get("rune_body_parts", [])
        if not rune_body_parts:
            print("rune_body_parts not found in JSON.")
            exit()
        
        body_part_renders = [part.get("body_part_render", "") for part in rune_body_parts if "body_part_render" in part]
        
        if not body_part_renders:
            print("No body_part_render found in rune_body_parts.")
            exit()

        # Step 4: Save the extracted values in a new JSON file in a new folder
        # Create the new folder if it doesn't exist
        new_folder_path = os.path.join(os.getcwd(), f"ACTUAL/{obj_name}")
        os.makedirs(new_folder_path, exist_ok=True)
        
        # Create the new JSON file and write the data
        new_file_path = os.path.join(new_folder_path, f"{obj_name}.json")
        with open(new_file_path, 'w') as new_f:
            json.dump({
                "obj_name": obj_name,
                "body_part_renders": body_part_renders
            }, new_f)
            
        print(f"Data extracted and saved in {new_file_path}.")
        
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")
    except Exception as e:
        print(f"An error occurred: {e}")


    import json
    import os

    # Existing code remains unchanged
    # ...

    # New steps

    # Assume the previous JSON was saved in new_file_path and body_part_renders array is available
    try:
        # Load the previously saved JSON to add new properties
        with open(new_file_path, 'r') as f:
            existing_data = json.load(f)
        
        # Initialize a dictionary to hold the new JSON contents
        new_json_contents = {}
        
        # Iterate over each number in body_part_renders array
        for num in body_part_renders:
            try:
                print(f"Processing {num}.json")
                # Construct the path to the new JSON file
                new_json_path = os.path.join('./ARCANE_DATA/COBJECTS/RENDER/', f'{num}.json')
                
                # Load the JSON file into memory
                with open(new_json_path, 'r') as f:
                    new_data = json.load(f)
                
                # Save the entire contents as a new property in new_json_contents
                new_json_contents[num] = new_data
                
            except FileNotFoundError:
                print(f"File {num}.json not found. Skipping.")
            except json.JSONDecodeError:
                print(f"Invalid JSON format in {num}.json. Skipping.")
        
        # Add the new JSON contents to the existing data
        existing_data['render_data'] = new_json_contents
        
        # Save the updated JSON back to the file
        with open(new_file_path, 'w') as f:
            json.dump(existing_data, f)
            
        print(f"Additional data added and saved in {new_file_path}.")

    except FileNotFoundError:
        print("Previously saved JSON file not found. Please check the file path.")
    except json.JSONDecodeError:
        print("Invalid JSON format in the previously saved file.")
    except Exception as e:
        print(f"An error occurred: {e}")


    # Read the 'render_data' from the JSON file we saved earlier
    try:
        with open(new_file_path, 'r') as f:
            existing_data = json.load(f)
        
        render_data = existing_data.get('render_data', {})
        
        # Iterate over each section corresponding to a number
        for num, section in render_data.items():
            # Locate array named 'render_children'
            render_children = section.get('render_children', [])
            
            # If this array exists and has additional numbers
            if render_children:
                # Initialize a dictionary to hold the new JSON contents
                new_json_contents = {}
                
                # Load each corresponding JSON file
                for child_num in render_children:
                    try:
                        # Construct the path to the new JSON file
                        child_json_path = os.path.join('./RENDER/', f'{child_num}.json')
                        
                        # Load the JSON file into memory
                        with open(child_json_path, 'r') as f:
                            child_data = json.load(f)
                        
                        # Save the entire contents as a new property in new_json_contents
                        new_json_contents[child_num] = child_data
                        
                    except FileNotFoundError:
                        print(f"File {child_num}.json not found in RENDER/. Skipping.")
                    except json.JSONDecodeError:
                        print(f"Invalid JSON format in {child_num}.json. Skipping.")
                
                # Replace the 'render_children' array with the loaded JSON data
                section['render_children'] = new_json_contents
        
        # Save the updated JSON back to the file
        with open(new_file_path, 'w') as f:
            json.dump(existing_data, f)
            
        print(f"Render children data added and saved in {new_file_path}.")

    except FileNotFoundError:
        print("Previously saved JSON file not found. Please check the file path.")
    except json.JSONDecodeError:
        print("Invalid JSON format in the previously saved file.")
    except Exception as e:
        print(f"An error occurred: {e}")


    def process_render_children(data):
        render_children = data.get('render_children', [])
        
        if render_children:
            new_contents = {}
            
            for child_num in render_children:
                try:
                    child_json_path = os.path.join('./RENDER/', f'{child_num}.json')
                    
                    with open(child_json_path, 'r') as f:
                        child_data = json.load(f)
                    
                    new_contents[child_num] = child_data
                    
                    # Recursively process this new data
                    process_render_children(child_data)
                    
                except FileNotFoundError:
                    print(f"File {child_num}.json not found in RENDER/. Skipping.")
                except json.JSONDecodeError:
                    print(f"Invalid JSON format in {child_num}.json. Skipping.")
            
            data['render_children'] = new_contents

    # Assume we have the 'existing_data' dictionary loaded with the previously saved JSON data
    try:
        with open(new_file_path, 'r') as f:
            existing_data = json.load(f)
        
        # Recursively process 'render_children' for each section corresponding to a number
        for num, section in existing_data.items():
            process_render_children(section)
        
        # Save the updated JSON back to the file
        with open(new_file_path, 'w') as f:
            json.dump(existing_data, f)
            
        print(f"Recursively updated render children data and saved in {new_file_path}.")

    except FileNotFoundError:
        print("Previously saved JSON file not found. Please check the file path.")
    except json.JSONDecodeError:
        print("Invalid JSON format in the previously saved file.")
    except Exception as e:
        print(f"An error occurred: {e}")
