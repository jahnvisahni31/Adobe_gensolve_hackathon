import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import svgwrite

def read_csv(file_path):
    """Read a CSV file and return the paths as a list of numpy arrays."""
    paths = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            points = np.array([float(x) for x in row]).reshape(-1, 2)
            paths.append(points)
    return paths

def polylines2svg(paths_XYs, svg_path):
    # Calculate the dimensions of the SVG canvas
    W, H = 0, 0
    for path_XYs in paths_XYs:
        # Ensure that path_XYs is a 2D array
        if len(path_XYs.shape) == 1:
            path_XYs = path_XYs.reshape(-1, 2)  # Reshape to 2D if it's 1D
        for XY in path_XYs:
            # Ensure that XY is a 2D array
            if len(XY.shape) == 1:
                XY = XY.reshape(-1, 2)  # Reshape to 2D if it's 1D
            W, H = max(W, np.max(XY[:, 0])), max(H, np.max(XY[:, 1]))
    
    padding = 0.1
    W, H = int(W + padding * W), int(H + padding * H)

    # Create a new SVG drawing
    dwg = svgwrite.Drawing(svg_path, profile='tiny', size=(W, H))
    group = dwg.g()
    colours = ['black', 'red', 'blue', 'green', 'purple', 'orange']  # Add more colours as needed

    for i, path in enumerate(paths_XYs):
        path_data = []
        c = colours[i % len(colours)]

        # Start constructing the path data
        if len(path) > 0:
            path_data.append(f"M {path[0][0]} {path[0][1]}")  # Move to the first point
            for j in range(1, len(path)):
                path_data.append(f"L {path[j][0]} {path[j][1]}")  # Line to subsequent points
            if not np.allclose(path[0], path[-1]):
                path_data.append("Z")  # Close the path if it's not a loop

        # Combine path data into a single string
        path_string = " ".join(path_data)
        group.add(dwg.path(d=path_string, fill='none', stroke=c, stroke_width=2))

    dwg.add(group)
    dwg.save()

    print(f"SVG saved to {svg_path}")