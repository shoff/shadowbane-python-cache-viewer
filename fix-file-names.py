import os

def remove_dash_xxx_recursively(directory):
    # Iterate through all files and subdirectories in the current directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if '-' in filename:
                base_name, extension = os.path.splitext(filename)
                parts = base_name.split('-')
                if len(parts) == 2 and parts[1].isdigit():
                    new_filename = f"{parts[0]}{extension}"
                    old_path = os.path.join(root, filename)
                    new_path = os.path.join(root, new_filename)
                    os.rename(old_path, new_path)
                    print(f"Renamed: {filename} -> {new_filename}")

# Example usage:
# Specify the directory where the renaming should start
start_directory = r'C:\dev\shadowbane-python-cache-viewer\ARCANE_DATA'
remove_dash_xxx_recursively(start_directory)