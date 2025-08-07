import numpy as np
import re

def parse_hex_pyramid_section(question):
    """
    Detect hexagonal pyramid problems and extract numerical parameters for base, axis, and section plane.
    Returns: dict with 'base_side', 'axis_height', 'section_angle', None if not matched
    """
    # Simple regex for numerals; defaults for demo
    base = re.search(r'base\s*(\d+(\.\d+)?)', question)
    axis = re.search(r'axis\s*(\d+(\.\d+)?)', question)
    angle = re.search(r'inclined\s*at\s*(\d+(\.\d+)?)', question)
    base_side = float(base.group(1)) if base else 30.0
    axis_height = float(axis.group(1)) if axis else 65.0
    section_angle = float(angle.group(1)) if angle else 60.0
    return dict(base_side=base_side, axis_height=axis_height, section_angle=section_angle)

def compute_section_polygon(base_side, axis_height, section_angle_deg):
    """
    Compute polygon points formed by the intersection of the section plane with slant edges (approximate).
    Returns: (hex_base_points, apex, section_points)
    """
    angles = np.deg2rad(np.linspace(0, 360, 7)[:-1])
    x_base = base_side * np.cos(angles)
    y_base = base_side * np.sin(angles)
    base_pts = np.stack((x_base, y_base, np.zeros_like(x_base)), axis=1)
    apex = np.array([0, 0, axis_height])

    # Section plane: through midpoint of axis, inclined to base at angle
    axis_mid = axis_height / 2
    theta = np.radians(section_angle_deg)
    # Normal vector: (0, -sin(theta), cos(theta)), passing through (0,0,axis_mid)
    normal = np.array([0, -np.sin(theta), np.cos(theta)])
    d = -np.dot(normal, np.array([0, 0, axis_mid]))

    # Find cut points on each slant edge (base point to apex)
    section_pts = []
    for v in base_pts:
        dir = apex - v
        # Plane equation: n.(v + t*dir) + d = 0 => solve t
        t = -(np.dot(normal, v) + d) / (np.dot(normal, dir))
        if 0 <= t <= 1:
            cut = v + t * dir
            section_pts.append(cut)
    return base_pts, apex, np.array(section_pts)

def plot_hex_pyramid_section(base_side, axis_height, section_angle_deg):
    """
    Plots hexagonal pyramid, section plane, and intersection polygon.
    Returns maptplotlib figure (fig)
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    base_pts, apex, section_pts = compute_section_polygon(base_side, axis_height, section_angle_deg)
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111, projection='3d')

    # plot base
    ax.plot(*zip(*(np.vstack([base_pts, base_pts[0]]).T)), c='k', linewidth=2, label='Base')
    # plot slant edges
    for p in base_pts:
        ax.plot([p[0], apex[0]], [p[1], apex[1]], [p[2], apex[2]], 'grey', linewidth=1)
    # plot axis
    ax.plot([0,0],[0,0],[0,axis_height],'b--',label="Axis")
    # plot section plane as transparent patch
    axis_mid = axis_height / 2
    theta = np.radians(section_angle_deg)
    normal = np.array([0, -np.sin(theta), np.cos(theta)])
    d = -np.dot(normal, np.array([0, 0, axis_mid]))
    xx, yy = np.meshgrid(np.linspace(-base_side*1.5, base_side*1.5, 2), np.linspace(-base_side*1.5, base_side*1.5, 2))
    zz = (-normal[0]*xx - normal[1]*yy - d)/normal[2]
    ax.plot_surface(xx, yy, zz, alpha=0.35, color='orange', shade=False, zorder=0, linewidth=0)
    # plot section polygon
    if len(section_pts) > 2:
        verts = [section_pts]
        poly = Poly3DCollection(verts, alpha=0.6, facecolor='lime', linewidths=2, zorder=10)
        ax.add_collection3d(poly)
        ax.scatter(section_pts[:,0], section_pts[:,1], section_pts[:,2], color='red', s=35, label="Section Points")
    # labels and view
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.set_title(f"Hexagonal Pyramid with Inclined Section ({section_angle_deg}° to base)")
    ax.view_init(elev=20, azim=35)
    ax.legend()
    ax.grid(False)
    return fig
    
