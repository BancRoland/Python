import trimesh
from shapely.geometry import Polygon

# Define a 2D polygon
polygon = Polygon([
    (0, 0),
    (40, 0),
    (20, 30)
])

# Extrude it into 3D
prism = trimesh.creation.extrude_polygon(
    polygon,
    height=50
)

# Save as STL
prism.export("prism.stl")

print("Created prism.stl")