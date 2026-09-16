import trimesh

# Create a cylinder
cylinder = trimesh.creation.cylinder(
    radius=20,      # mm
    height=50,      # mm
    sections=64     # smoothness
)

# Save as STL
cylinder.export("cylinder.stl")

print("Created cylinder.stl")