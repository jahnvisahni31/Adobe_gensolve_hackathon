import numpy as np
from scipy.optimize import leastsq

def detect_straight_lines(paths):
    """Identify and regularize straight lines in the paths."""
    regularized_paths = []
    for path in paths:
        if is_straight_line(path):
            regularized_paths.append(regularize_straight_line(path))
        else:
            regularized_paths.append(path)
    return regularized_paths

def is_straight_line(path):
    """Check if a sequence of points forms a straight line."""
    if len(path) < 2:
        return False
    vector = path[-1] - path[0]
    norm_vector = vector / np.linalg.norm(vector)
    for i in range(1, len(path) - 1):
        diff = path[i] - path[0]
        projected_diff = np.dot(diff, norm_vector)
        if not np.allclose(diff, projected_diff * norm_vector, atol=1e-3):
            return False
    return True

def regularize_straight_line(path):
    """Regularize a sequence of points into a straight line."""
    return np.array([path[0], path[-1]])


def is_circle(path):
    """Check if a sequence of points forms a circle."""
    center, radius = fit_circle(path)
    distances = np.linalg.norm(path - center, axis=1)
    return np.allclose(distances, radius, atol=1e-2)

def fit_circle(path):
    """Fit a circle to a sequence of points."""
    def calc_R(c):
        """Calculate the distance of each 2D point from the center c."""
        return np.sqrt((path[:, 0] - c[0]) ** 2 + (path[:, 1] - c[1]) ** 2)

    def func(c):
        """Calculate the algebraic distance between the data points and the mean circle centered at c."""
        Ri = calc_R(c)
        return Ri - Ri.mean()

    center_estimate = np.mean(path, axis=0)
    center, _ = leastsq(func, center_estimate)
    radius = calc_R(center).mean()
    return center, radius

def regularize_circle(path):
    """Regularize a sequence of points into a circle."""
    center, radius = fit_circle(path)
    num_points = len(path)
    angles = np.linspace(0, 2 * np.pi, num_points)
    return np.column_stack((center[0] + radius * np.cos(angles),
                            center[1] + radius * np.sin(angles)))


def is_rectangle(path):
    """Check if a sequence of points forms a rectangle."""
    if len(path) != 4:
        return False
    # Check if the four points form a rectangle.
    distances = [np.linalg.norm(path[i] - path[j]) for i in range(4) for j in range(i + 1, 4)]
    distances.sort()
    return np.allclose(distances[0] + distances[1], distances[2], atol=1e-2) and \
           np.allclose(distances[2] + distances[3], distances[4], atol=1e-2)

def regularize_rectangle(path):
    """Regularize a sequence of points into a rectangle."""
    if len(path) != 4:
        return path
    # Fit a rectangle to the points. Assumes the points are in clockwise or counter-clockwise order.
    x_min, y_min = np.min(path, axis=0)
    x_max, y_max = np.max(path, axis=0)
    return np.array([[x_min, y_min],
                     [x_min, y_max],
                     [x_max, y_max],
                     [x_max, y_min]])