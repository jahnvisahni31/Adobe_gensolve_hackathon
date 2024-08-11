import numpy as np
from shapely.geometry import LineString, Polygon, Point
from shapely.affinity import rotate

def detect_symmetry(paths):
    """Detect symmetry in paths and return symmetric curves."""
    symmetric_paths = []
    for path in paths:
        if has_reflection_symmetry(path):
            symmetric_paths.append(handle_reflection_symmetry(path))
        elif has_rotation_symmetry(path):
            symmetric_paths.append(handle_rotation_symmetry(path))
        else:
            symmetric_paths.append(path)
    return symmetric_paths

def has_reflection_symmetry(path):
    """Check if a path has reflection symmetry."""
    shape = LineString(path) if len(path) > 2 else None
    if not shape or not shape.is_valid:
        return False
    # Check reflection symmetry along the x-axis and y-axis
    return (is_symmetric_along_axis(shape, 'x') or 
            is_symmetric_along_axis(shape, 'y'))

def is_symmetric_along_axis(shape, axis):
    """Check if the shape is symmetric along a given axis."""
    if axis == 'x':
        reflected_shape = reflect_along_x_axis(shape)
    elif axis == 'y':
        reflected_shape = reflect_along_y_axis(shape)
    else:
        raise ValueError("Axis must be 'x' or 'y'.")
    return shape.equals(reflected_shape)

def reflect_along_x_axis(shape):
    """Reflect a shape along the x-axis."""
    x, y = shape.xy
    reflected_y = [-yi for yi in y]  # Reflect y-coordinates
    return LineString(zip(x, reflected_y))

def reflect_along_y_axis(shape):
    """Reflect a shape along the y-axis."""
    x, y = shape.xy
    reflected_x = [-xi for xi in x]  # Reflect x-coordinates
    return LineString(zip(reflected_x, y))


def handle_reflection_symmetry(path):
    """Handle reflection symmetry in a path."""
    shape = LineString(path) if len(path) > 2 else None
    if not shape or not shape.is_valid:
        return path
    # Reflect the shape along the y-axis for simplicity
    reflected_shape = reflect_along_y_axis(shape)
    return np.array(reflected_shape.xy).T

def has_rotation_symmetry(path):
    """Check if a path has rotation symmetry."""
    shape = LineString(path) if len(path) > 2 else None
    if not shape or not shape.is_valid:
        return False
    # Check rotation symmetry by rotating the shape around its centroid
    centroid = shape.centroid
    return any(
        shape.equals(rotate(shape, angle, origin=centroid))
        for angle in np.linspace(0, 360, num=36)  # Check 36 rotation angles
    )

def handle_rotation_symmetry(path):
    """Handle rotation symmetry in a path."""
    shape = LineString(path) if len(path) > 2 else None
    if not shape or not shape.is_valid:
        return path
    centroid = shape.centroid
    # Rotate the shape around its centroid by 45 degrees
    rotated_shape = rotate(shape, 45, origin=centroid)
    return np.array(rotated_shape.xy).T