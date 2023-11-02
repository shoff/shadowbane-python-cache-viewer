def write_mtl_file(mtl_path, texture_files):
    with open(mtl_path, 'w') as f:
        for texture_file in texture_files:
            f.write(f"newmtl {texture_file}\n")
            f.write(f"map_Kd {texture_file}.jpg\n\n")

def write_obj_file(obj_path, mtl_path, vertices, faces, texture_ids):
    with open(obj_path, 'w') as f:
        f.write(f"mtllib {mtl_path}\n")
        for v in vertices:
            f.write(f"v {' '.join(map(str, v))}\n")
        for face, texture_id in zip(faces, texture_ids):
            f.write(f"usemtl {texture_id}\n")
            f.write(f"f {' '.join(map(str, [i+1 for i in face]))}\n")

# ... (The rest of the code remains the same)

# Initialize a list to store texture IDs for each face
global_texture_ids = []

# Loop through each mesh JSON file
for body_part_file in body_part_files:
    # ... (The rest of the code in this loop remains the same)

    # Retrieve texture ID and extend to the length of faces for this part
    texture_id = render_data[body_part_file]['render_texture_set']
    global_texture_ids.extend([texture_id] * len(faces))

# Unique texture files to be written into the MTL file
unique_texture_files = set(global_texture_ids)

# Write to OBJ and MTL files
write_mtl_file("path/to/save/your/combined/file.mtl", unique_texture_files)
write_obj_file("path/to/save/your/combined/file.obj", "path/to/save/your/combined/file.mtl", global_vertices, global_faces, global_texture_ids)