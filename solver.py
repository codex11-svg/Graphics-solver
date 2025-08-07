import numpy as np
import re

def parse_hex_pyramid_section(question):
    """
    Detect hexagonal pyramid word problems and extract base, axis, section info.
    Only handles classic academic phrasing.
    Returns: dict with 'base_side', 'axis_height', 'section_angle'
    """
    # Extract numbers
    base = re.search(r'base\s*(\d+)', question)
    axis = re.search(r'axis\s*(\d+)', question)
    angle = re.search(r'inclined\s*at\s*(\d+)', question)
    base_side = float(base.group(1)) if base else 30.0
    axis_height = float(axis.group(1)) if axis else 65.0
    section_angle = float(angle.group(1)) if angle else 60.0
    return dict(base_side=base_side, axis_height=axis_height, section_angle=section_angle)

def plot_hex_pyramid_with_section(base_side, axis_height, section_angle_deg):
    """
    Plots a hexagonal pyramid and an inclined section plane in 3D.
    Returns a matplotlib fig.
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    # Hex base points (regular hexagon, base on XY, one edge parallel to Y)
    angles = np.deg2rad(np.linspace(0, 360, 7)[:-1])
    x_base = base_side * np.cos(angles)
    y_base = base_side * np.sin(angles)
    base_pts = np.stack((x_base, y_base, np.zeros_like(x_base)), axis=1)
    apex = np.array([0, 0, axis_height])
    # For cut: section plane through axis midpoint, inclined to base at given angle
    mid_axis = np.array([0,0,axis_height/2])
    normal = np.array([0, -np.sin(np.radians(section_angle_deg)), np.cos(np.radians(section_angle_deg))])
    d = -np.dot(normal, mid_axis)
    # Show
    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111, projection='3d')
    # Plot base
    ax.plot(*zip(*(np.vstack([base_pts, base_pts[0]]).T)), c='k')
    # Plot slant edges
    for pt in base_pts:
        ax.plot([pt[0], apex[0]], [pt[1], apex[1]], [0, apex[2]], 'grey')
    # Plot axis
    ax.plot([0,0],[0,0],[0,axis_height],'b--')
    # Plot section plane as a transparent rectangular patch
    xx, yy = np.meshgrid(np.linspace(-base_side*1.5, base_side*1.5, 2), np.linspace(-base_side*1.5, base_side*1.5, 2))
    zz = (-normal[0]*xx - normal[1]*yy - d)/normal[2]
    ax.plot_surface(xx, yy, zz, alpha=0.4, color='orange', shade=False)
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.set_title("Hexagonal Pyramid with Section Plane (3D View)")
    ax.view_init(elev=21, azim=33)
    ax.grid(False)
    return fig
