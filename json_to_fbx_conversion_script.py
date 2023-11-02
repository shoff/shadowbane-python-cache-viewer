import json
import pyfbx

def convert_json_to_fbx(json_path, fbx_path):
    # Read and parse the JSON mesh file
    with open(json_path, 'r') as f:
        mesh_data = json.load(f)

    # Create a new FBX manager and scene
    mgr = pyfbx.Manager()
    scene = pyfbx.Scene(mgr)

    # Create a new mesh in the scene
    mesh = pyfbx.Mesh(scene, mesh_data.get('mesh_name', 'Unnamed'))

    # Add vertices to the mesh
    for vertex in mesh_data.get('mesh_vertices', []):
        mesh.add_vertex(*vertex)

    # Add normals to the mesh
    for normal in mesh_data.get('mesh_normals', []):
        mesh.add_normal(*normal)

    # Add faces to the mesh (assuming they are defined by vertex indices)
    for face in mesh_data.get('mesh_faces', []):
        mesh.add_polygon(face)

    # Export the scene to FBX format
    scene.export(fbx_path)

# Set paths (you need to replace these with your actual paths)
json_path = r"F:\ai\shadowbane\ACTUAL\Aelfborn\5061.json"
fbx_path = r"F:\ai\shadowbane\ACTUAL\Aelfborn\5061.fbx"

# Perform the conversion
convert_json_to_fbx(json_path, fbx_path)
