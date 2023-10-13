
from PIL import Image
import json
import os

class RuneObject:
    def __init__(self):
        self.rune_name = None
        self.rune_id = None
        self.rune_body_parts = []

    class BodyPart:
        def __init__(self):
            self.body_part_render = None
            self.body_part_position = None
            self.render_data = None
            self.mesh_data = None
            self.texture_data = None

    def load_from_json(self, json_path, render_folder, mesh_folder, texture_folder):
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        self.rune_name = data.get('rune_name', None)
        self.rune_id = data.get('rune_id', None)
        
        for part in data.get('rune_body_parts', []):
            body_part = self.BodyPart()
            body_part.body_part_render = part['body_part_render']
            body_part.body_part_position = part['body_part_position']
            
            render_data_path = os.path.join(render_folder, f"{body_part.body_part_render}.json")
            with open(render_data_path, 'r') as f:
                body_part.render_data = json.load(f)
            
            mesh_id = body_part.render_data['render_template']['template_mesh']['mesh_set'][0]['polymesh_id']
            mesh_data_path = os.path.join(mesh_folder, f"{mesh_id}.json")
            with open(mesh_data_path, 'r') as f:
                body_part.mesh_data = json.load(f)
            
            if 'render_texture_set' in body_part.render_data and body_part.render_data['render_texture_set']:
                texture_id = body_part.render_data['render_texture_set'][0]['texture_data']['texture_id']
                texture_data_path = os.path.join(texture_folder, f"{texture_id}.jpg")
                body_part.texture_data = Image.open(texture_data_path)
            
            self.rune_body_parts.append(body_part)
