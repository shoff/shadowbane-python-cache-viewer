import os
import json
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QOpenGLWidget, QPushButton
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QOpenGLContext
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

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
            # Read the correct texture ID from the RENDER JSON file associated with the selected rune or render object
            # Ensure the .json extension is only added once
            render_file_path = os.path.join('ARCANE_DATA', 'RENDER', f"{selected_render_id if selected_render_id.endswith('.json') else f'{selected_render_id}.json'}")
            with open(render_file_path, 'r') as file:
                content = json.load(file)
            correct_texture_id = content.get('texture_id', 'Unknown')
            # Use the correct texture ID to form the path for the texture file
            texture_file_path = f"./ARCANE_DATA/TEXTURE/{correct_texture_id}.jpg"
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
        