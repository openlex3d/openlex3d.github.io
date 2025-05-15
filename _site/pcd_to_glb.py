import open3d as o3d
import numpy as np
from pygltflib import GLTF2, Buffer, BufferView, Accessor, Mesh, MeshPrimitive, Scene, Node

# Load the PCD file using open3d
pcd = o3d.io.read_point_cloud("/media/christina/T7 Shield1/results_openlex3d/concept-graphs/top_5/replica/room0/point_cloud.pcd")

# Get the point cloud data as a numpy array
points = np.asarray(pcd.points)

# Create a GLTF object
gltf = GLTF2()

# Convert the points into a buffer for GLTF
buffer_data = points.astype(np.float32).tobytes()
buffer = Buffer(uri="data:application/octet-stream;base64," + buffer_data.hex(), byteLength=len(buffer_data))
gltf.buffers.append(buffer)

# Create BufferView for the points
buffer_view = BufferView(
    buffer=0,  # Referring to the first buffer
    byteOffset=0,
    byteLength=len(buffer_data),
    target=BufferView.ARRAY_BUFFER  # Using ARRAY_BUFFER for point data
)
gltf.bufferViews.append(buffer_view)

# Create Accessor for the points
accessor = Accessor(
    bufferView=0,
    byteOffset=0,
    componentType=Accessor.FLOAT,
    count=len(points),
    type="VEC3",  # Each point is a 3D vector (x, y, z)
    min=[points[:, 0].min(), points[:, 1].min(), points[:, 2].min()],
    max=[points[:, 0].max(), points[:, 1].max(), points[:, 2].max()]
)
gltf.accessors.append(accessor)

# Create a MeshPrimitive using the points (as points, not faces)
mesh_primitive = MeshPrimitive(
    attributes={"POSITION": 0},  # We are just using position as the attribute
    mode=0  # Points (GL_POINTS mode)
)

# Create a mesh and add the primitive to it
mesh = Mesh(primitives=[mesh_primitive])
gltf.meshes.append(mesh)

# Create a node with the mesh and add it to the scene
node = Node(mesh=0)
scene = Scene(nodes=[0])
gltf.scenes.append(scene)

# Set the scene as the active scene
gltf.scene = 0

# Save the GLTF to a GLB file (binary format)
gltf.save("static/glbs_gd/point_cloud.glb")
