
# File Relationships for 3D Model Rendering

This document describes the relationships between various types of JSON files used for 3D model rendering.

## Directories

- `COBJECTS`: Contains JSON files detailing common objects.
- `MESH`: Contains JSON files with mesh information.
- `RENDER`: Contains JSON files that describe how to render complete objects. These are the central files that link to other types.
- `SKELETON`: Contains JSON files with skeleton (bone) information.
- `TEXTURE`: Contains JSON files with texture data.
- `MOTION`: Contains JSON files detailing animations.

## Relationships

### RENDER

- **ID**: Obtained from the filename, serves as a unique identifier.
- **Child Objects**: A `RENDER` object can have multiple child objects, also potentially `RENDER` objects. These are listed under the `render_children` attribute.
- **Mesh Information**: Contains a `template_mesh` attribute that holds a `mesh_set`. Each entry in `mesh_set` has a `polymesh_id` linking to a file in the `MESH` folder.
- **Texture Information**: Contains a `render_texture_set` attribute that holds texture information. Each texture set has a `texture_id` that links to a file in the `TEXTURE` folder.

### MESH

- **ID**: Obtained from the filename, serves as a unique identifier.
- **Used By**: Referenced by `RENDER` objects in their `template_mesh` attribute's `mesh_set`.

### TEXTURE

- **ID**: Obtained from the filename, serves as a unique identifier.
- **Used By**: Referenced by `RENDER` objects in their `render_texture_set`.

### SKELETON, MOTION, COBJECTS

- **ID**: Obtained from the filename, serves as a unique identifier.
- **Used By**: These files could potentially be referenced by `RENDER` objects, although this is not demonstrated in the sample data.

## Example

A `RENDER` object with ID `100` might contain:
- A `render_children` attribute with `[101, 102]` meaning it has two child objects with IDs `101` and `102`.
- A `template_mesh` attribute with a `mesh_set` containing `polymesh_id: 200`. This links to a `MESH` object with ID `200`.
- A `render_texture_set` attribute containing `texture_id: 300`. This links to a `TEXTURE` object with ID `300`.

This `RENDER` object would thus form the central hub connecting to other types of objects to form a complete 3D model.

- MESH: Contains mesh details like vertices, normals, UV coordinates, etc.
    - Keys: mesh_name, mesh_distance, mesh_start_point, mesh_end_point, mesh_ref_point, mesh_use_face_normals, mesh_use_tangent_basis, mesh_vertices, mesh_normals, mesh_uv, mesh_indices, mesh_extra_indices
- RENDER: Contains rendering information, including links to mesh, texture, and child objects.
    - Keys: render_template, render_target_bone, render_scale, render_has_loc, render_loc, render_children, render_has_texture_set, render_texture_set, render_collides, render_calculate_bounding_box, render_nation_crest, render_guild_crest, render_bumped, render_vp_active, render_has_light_effects
- SKELETON: Contains skeleton or bone information.
    - Keys: skeleton_name, skeleton_motion, skeleton_root
- MOTION: Contains motion or animation information.
 - Keys: motion_file, motion_smoothed_count, motion_smoothed_value, motion_smoothed_factor, motion_sound, motion_sheath, motion_reset_loc, motion_leave_ground, motion_force, motion_disable_blend, motion_parts, motion_smoothing, motion_target_frames
Given this information, the next step is to extract the relevant data from these JSON files and use it for OpenGL rendering.

To get started, we can focus on the 'RENDER' and 'MESH' categories, as these will provide the main information needed for rendering the 3D models. Specifically, we will need to:

Extract the mesh details from the 'MESH' JSON files referenced in the 'RENDER' JSON files.
Use these mesh details to render the shapes using OpenGL.