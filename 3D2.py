import bpy
from mathutils import Vector
from math import radians
import itertools
import random

# Define the parameters
n = 10
L = 15
W = 15
Hz = 10
O = 0.1
max_r_values = [2.00, 2.50, 3.00, 3.50, 4.00, 4.50, 5.00]
threshold = 0.5

# Define the function to calculate the number of combinations
def calculate_combinations(n, L, W, Hz, O, max_r_values):
    combinations = 0
    usable_spaces = []
    for k in range(1, n+1):
        for max_r_sublist in itertools.combinations(max_r_values, k):
            prod_term = 1
            for r in max_r_sublist:
                prod_term *= (r - 0) / (r - O * r)
            sum_term = prod_term * ((L - max(max_r_sublist)) / (max(max_r_sublist) - O * max(max_r_sublist))) * ((W - max(max_r_sublist)) / (max(max_r_sublist) - O * max(max_r_sublist))) * ((Hz - max(max_r_sublist)) / (max(max_r_sublist) - O * max(max_r_sublist)))
            combinations += sum_term
            if sum_term > threshold:
                usable_spaces.append(max_r_sublist)
    
    return usable_spaces

# Define a function to add a sphere to the scene
def add_sphere(radii):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radii[0], location=(radii[0], radii[0], radii[0]))
    sphere = bpy.context.active_object
    for r in radii[1:]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(r, r, r))
        bool_mod = sphere.modifiers.new(name='Boolean', type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = bpy.context.active_object
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    return sphere

# Create a new scene
bpy.ops.scene.new(type='NEW')
scene = bpy.context.scene

# Add a camera to the scene
cam_data = bpy.data.cameras.new('camera')
cam_ob = bpy.data.objects.new('camera', cam_data)
scene.camera = cam_ob

# Set camera location and orientation
cam_ob.location = (25, -25, 25)
cam_ob.rotation_euler = (radians(45), 0, radians(45))

# Set camera settings
cam_data.type = 'ORTHO'
cam_data.ortho_scale = 12

# Generate usable spaces and add spheres to the scene
usable_spaces = calculate_combinations(n, L, W, Hz, O, max_r_values)
for space in usable_spaces:
    x = random.uniform(space[0], L-space[0])
    y = random.uniform(space[0], W-space[0])
    z = random.uniform(space[0], Hz-space[0])
    add_sphere(space).location = (x,y,z)

# Add a solid plane to the scene to cut the spheres
bpy.ops.mesh.primitive_plane_add(size=25, enter_editmode=False, location=(0, 0, -1))
plane = bpy.context.active_object
plane.name = "CuttingPlane"
plane_data = plane.data
plane_data.materials.append(bpy.data.materials["Material"])

bpy.ops.mesh.primitive_cube_add(size=2.0, calc_uvs=True, enter_editmode=False, align='WORLD', location=(0.0, 0.0, -50.0), rotation=(0.0, 0.0, 0.0), scale=(50.0, 50.0, -50.0))
