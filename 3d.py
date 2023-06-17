import bpy
from mathutils import Vector
from math import radians
import itertools
import random

# Define the parameters
n = 15
L = 30
W = 30
Hz = 10
O = 0.1
max_r_values = [2.00, 2.50, 3.00, 3.50, 4.00, 4.50, 5.00]

# Define the function to calculate the number of combinations
def calculate_combinations(n, L, W, Hz, O, max_r_values):
    combinations = 0
    for k in range(1, n+1):
        for max_r_sublist in itertools.combinations(max_r_values, k):
            prod_term = 1
            for r in max_r_sublist:
                prod_term *= (r - 0) / (r - O * r)
            sum_term = prod_term * ((L - max(max_r_sublist)) / (max(max_r_sublist) - O * max(max_r_sublist))) * ((W - max(max_r_sublist)) / (max(max_r_sublist) - O * max(max_r_sublist))) * ((Hz - max(max_r_sublist)) / (max(max_r_sublist) - O * max(max_r_sublist)))
            combinations += sum_term
            if sum_term > 0.5:  # Add a threshold for usability
                add_sphere(max_r_sublist, (random.uniform(-L/2, L/2), random.uniform(-W/2, W/2), random.uniform(0, Hz-max(max_r_sublist))))
    print(combinations)
    

# Define a function to add a sphere to the scene
def add_sphere(radii, location):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radii[0], location=location)
    sphere = bpy.context.active_object
    for r in radii[1:]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=location)
        bool_mod = sphere.modifiers.new(name='Boolean', type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = bpy.context.active_object
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    return sphere

# Create a new scene
bpy.ops.scene.new(type='NEW')
scene = bpy.context.scene

# Set up the camera
cam_data = bpy.data.cameras.new('camera')
cam_ob = bpy.data.objects.new('camera', cam_data)
scene.camera = cam_ob
cam_ob.location = (50, -50, 50)
cam_ob.rotation_euler = (radians(45), 0, radians(45))
cam_data.type = 'ORTHO'
cam_data.ortho_scale = 25

# Add the plane
bpy.ops.mesh.primitive_plane_add(size=L, location=(0, 0, -1))

# Set up lighting
bpy.ops.object.light_add(type='SUN', location=(10, -10, 10))
bpy.context.active_object.data.energy = 5
bpy.ops.mesh.primitive_cube_add(size=2.0, calc_uvs=True, enter_editmode=False, align='WORLD', location=(0.0, 0.0, -50.0), rotation=(0.0, 0.0, 0.0), scale=(50.0, 50.0, -50.0))
# Run the calculations and display the spheres
calculate_combinations(n, L, W, Hz, O, max_r_values)

