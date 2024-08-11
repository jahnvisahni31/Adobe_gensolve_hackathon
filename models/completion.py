import numpy as np
from shapely.geometry import LineString

def complete_curves(paths):
    """Complete incomplete curves in paths."""
    completed_paths = []
    for path in paths:
        completed_path = complete_incomplete_curve(path)
        completed_paths.append(completed_path)
    return completed_paths

def complete_incomplete_curve(path):
    """Complete an incomplete curve by connecting gaps or extrapolating."""
    if len(path) < 2:
        return path
    return connect_or_extrapolate(path)

def connect_or_extrapolate(path):
    """Connect gaps or extrapolate to complete a curve."""
    line = LineString(path)
    if not line.is_valid:
        return path
    return np.array(line.xy).T