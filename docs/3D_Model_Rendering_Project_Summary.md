
# 3D Model Rendering Project Summary

## Overview
This project aims to read JSON files representing 3D models and render them using OpenGL in a PyQt5 application.

## File Structure
- **COBJECTS**: Stores COBJECT files.
- **MESH**: Stores mesh information.
- **RENDER**: Contains information about complete objects.
- **SKELETON**: Stores skeleton or bone information.
- **TEXTURE**: Contains texture files.
- **MOTION**: Contains animation data.

## File Relationships
- **Render Objects**: These objects contain references to child objects, textures, skeletons, and motions. The IDs correspond to filenames.
- **Mesh Objects**: Contain vertices, normals, and indices for rendering 3D models. Referred to by Render Objects.

## Code Architecture
- **read_json_file(file_path)**: Reads a JSON file and returns its content.
- **extract_id_from_filename(filename)**: Extracts the ID from a filename.
- **render_mesh_from_file(mesh_file_path)**: Reads a MESH JSON file and renders the mesh using OpenGL.
- **OpenGLWidget Class**: Inherits from QOpenGLWidget and handles the OpenGL rendering.
    - **set_render_id(render_id)**: Sets the current render object ID to render.
    - **initializeGL**: Initializes OpenGL settings.
    - **resizeGL(w, h)**: Handles window resizing.
    - **paintGL**: Handles the OpenGL rendering.
    - **mousePressEvent(event)**: Captures the mouse press event.
    - **mouseMoveEvent(event)**: Handles mouse drag for rotating and panning.
    - **wheelEvent(event)**: Implements zooming using the mouse wheel.

## Features Implemented
- Object Selection via a Dropdown menu.
- 3D Model Rendering using OpenGL.
- Camera Controls:
    - Rotation: Left mouse drag.
    - Zoom: Mouse wheel scroll.
    - Pan: Right mouse drag.

## To Run the Code
1. Replace placeholder paths for the `RENDER` and `MESH` folders.
2. Install PyQt5 and PyOpenGL.
3. Run the Python script.
