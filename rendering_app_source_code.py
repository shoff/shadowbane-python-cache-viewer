import json
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QOpenGLWidget, QPushButton
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QOpenGLContext
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

# Define a dictionary to hold multiple texture IDs
texture_ids = {}

def load_texture(image_path, texture_name):
    global texture_ids
    # Load the image
    img = Image.open(image_path)
    img_data = img.tobytes("raw", "RGB", 0, -1)
    
    # Generate a texture ID and bind to it
    texture_id = glGenTextures(1)
    print('DEBUG: Generated texture ID:', texture_id)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    print('DEBUG: Bound to texture ID:', texture_id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    
    # Save the texture ID in the dictionary
    texture_ids[texture_name] = texture_id
    print('DEBUG: Stored texture ID in texture_ids:', texture_ids)
    return texture_id

# Function to read a JSON file and return its content
def read_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to extract the ID from a filename
def extract_id_from_filename(filename):
    return filename.split('-')[0].split('.')[0]

def render_mesh_from_file(mesh_file_path, texture_name):
    # Read the mesh data from the JSON file
    with open(mesh_file_path, 'r') as f:
        mesh_data = json.load(f)
    print('DEBUG:     # Extract vertices, UV coordinates, and normals')
    # Flatten nested lists of vertices and normals
    vertices = [coord for vertex in mesh_data.get('mesh_vertices', []) for coord in vertex]
    normals = [coord for normal in mesh_data.get('mesh_normals', []) for coord in normal]
    uv_coords = mesh_data.get('mesh_uv', [])
    indices = mesh_data.get('mesh_indices', [])
    
    # Bind the texture
    glBindTexture(GL_TEXTURE_2D, texture_ids.get(texture_name, 0))
    
    # Start drawing the mesh
    glBegin(GL_TRIANGLES)
    for index in indices:
        vertex = vertices[index * 3: index * 3 + 3]
        normal = normals[index * 3: index * 3 + 3]
        uv_coord = uv_coords[index] if index < len(uv_coords) else (0, 0)
        
        # Apply normal if available
        if len(normal) == 3:
            glNormal3f(*normal)
        
        # Apply texture coordinate if available
        if len(uv_coord) == 2:
            glTexCoord2f(*uv_coord)
        
        # Apply vertex coordinate
        if len(vertex) == 3:
            glVertex3f(*vertex)
    glEnd()


# Load all RENDER JSON files
render_dir = Path('./ARCANE_DATA/RENDER')  # Replace with the actual path
render_files = list(render_dir.glob('*.json'))

# Read RENDER files and store them in a dictionary keyed by their IDs
render_objects = {}
for render_file in render_files:
    render_id = extract_id_from_filename(render_file.name)
    render_objects[render_id] = read_json_file(render_file)

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, render_objects, *args, **kwargs):
        super(OpenGLWidget, self).__init__(*args, **kwargs)
        self.render_objects = render_objects
        self.current_render_id = None
        self.lastPos = QPoint()
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.translation_z = -10
        self.translation_x = 0  # For panning
        self.translation_y = 0  # For panning
        
    def set_render_id(self, render_id):
        self.current_render_id = render_id
        self.update()

    def initializeGL(self):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w/h, 1, 1000)
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.translation_x, self.translation_y, self.translation_z)
        glRotatef(self.xRot / 16.0, 1, 0, 0)
        glRotatef(self.yRot / 16.0, 0, 1, 0)
        glRotatef(self.zRot / 16.0, 0, 0, 1)

        if self.current_render_id:
            texture_file_path = f"./ARCANE_DATA/TEXTURE/{self.current_render_id}.jpg"
            self.texture_id = load_texture(texture_file_path, str(self.current_render_id))
            
            render_object = self.render_objects.get(self.current_render_id, {})
            mesh_file_path = f"./ARCANE_DATA/MESH/{render_object.get('render_template', {}).get('template_mesh', {}).get('mesh_set', [{}])[0].get('polymesh_id', '')}.json"
            
            render_mesh_from_file(mesh_file_path, str(self.current_render_id))

        self.doneCurrent()
        self.makeCurrent()
        
    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.xRot += 8 * dy
            self.yRot += 8 * dx
        elif event.buttons() & Qt.RightButton:
            self.translation_x += dx / 100.0  # For panning
            self.translation_y -= dy / 100.0  # For panning
        self.lastPos = event.pos()
        self.update()
        
    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120  # Get wheel movement
        self.translation_z += delta  # Update translation factor based on wheel movement
        self.update()
        
app = QApplication([])
window = QWidget()
window.resize(1024, 768)
layout = QVBoxLayout()

label = QLabel('Select RENDER Object ID:')
layout.addWidget(label)

dropdown = QComboBox()
dropdown.addItems(list(render_objects.keys()))
layout.addWidget(dropdown)

load_button = QPushButton('Load 3D Model')
layout.addWidget(load_button)

opengl_widget = OpenGLWidget(render_objects=render_objects)
layout.addWidget(opengl_widget)

def on_dropdown_change():
    selected_render_id = dropdown.currentText()
    opengl_widget.set_render_id(selected_render_id)

def on_button_click():
    selected_render_id = dropdown.currentText()
    opengl_widget.set_render_id(selected_render_id)
    opengl_widget.update()

# dropdown.currentIndexChanged.connect(on_dropdown_change)
load_button.clicked.connect(on_button_click)

window.setLayout(layout)
window.show()

app.exec_()
