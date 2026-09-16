import trimesh
from shapely.geometry import Polygon
import polys
import utils

height = 3

drawings_to_do = [polys.female, 
                  polys.male]

for drawing in drawings_to_do:

    # Define a 2D polygon
    polygon = Polygon(drawing.points)

    clearance = 0.2

    polygon = polygon.buffer(-clearance)


    drawing.plot_my_drawing()

    # Extrude it into 3D
    prism = trimesh.creation.extrude_polygon(
        polygon,
        height=height
    )

    # Save as STL
    prism.export(f"{drawing.name}.stl")

    print("Created stl")