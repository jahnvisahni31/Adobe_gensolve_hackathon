import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import cairosvg  # Import the cairosvg library

# Adjust the path to include the necessary modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.regularize import detect_straight_lines
from models.utils import read_csv, polylines2svg
from models.symmetry import detect_symmetry
from models.completion import complete_curves

def convert_svg_to_png(svg_file, png_file):
    """Convert an SVG file to PNG format."""
    cairosvg.svg2png(url=svg_file, write_to=png_file)

def main():
    # Load paths from CSV
    input_files = [
        'isolated.csv',
        'frag0.csv',
        'frag1.csv',
        'frag2.csv',
        'occlusion1.csv',
        # Add other files as needed
    ]   
    
    # Loop through each input file
    for csv_filename in input_files:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'problems/problems', csv_filename)
        paths = read_csv(csv_path)

        # Regularize straight lines and circles/ellipses
        paths = detect_straight_lines(paths)
        paths = detect_symmetry(paths)
        paths = complete_curves(paths)
        
        # Plot and save the regularized paths
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        
        # Create the full output file path
        output_file_svg = os.path.join(output_dir, f'{csv_filename}.svg')
        
        # Call plot_paths with the correct parameters
        polylines2svg(paths, output_file_svg)

        # Convert SVG to PNG
        output_file_png = os.path.join(output_dir, f'{csv_filename}.png')
        convert_svg_to_png(output_file_svg, output_file_png)

if __name__ == "__main__":
    main()
