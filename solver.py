import numpy as np
import matplotlib.pyplot as plt
import re

def parse_hex_pyramid_section(question):
    """
    Extracts base, axis, and section angle from any descriptive hexagonal pyramid problem.
    Returns: dict with 'base_side', 'axis_height', 'section_angle'
    """
    base = re.search(r'base\s*(\d+(\.\d+)?)', question)
    axis = re.search(r'axis\s*(\d+(\.\d+)?)', question)
    angle = re.search(r'inclined\s*at\s*(\d+(\.\d+)?)', question)
    base_side = float(base.group(1)) if base else 30.0
    axis_height = float(axis.group(1)) if axis else 65.0
    section_angle = float(angle.group(1)) if angle else 60.0
    return dict(base_side=base_side, axis_height=axis_height, section_angle=section_angle)

def plot_hex_pyramid_conceptual(base_side=30, axis_height=65, section_angle=60):
    """
    Draws conceptual FV (front view), sectional TV (top view), and true shape for a hexagonal pyramid with section.
    Returns matplotlib fig.
    """
    fig, axes = plt.subplots(3, 1, figsize=(11, 10))
    fig.subplots_adjust(hspace=0.4)

    # --- FV (Front View) ---
    ax = axes[0]
    ax.set_title("Front View (Elevation)", fontsize=12, weight='bold')
    ax.axis('off')

    dx = base_side*1.1
    margin = 10
    xy_y = margin
    apex_y = xy_y + axis_height
    base_hex_x = np.linspace(margin, margin+dx*5, 6)
    mx = (base_hex_x[2]+base_hex_x[3])/2
    # Base line
    ax.plot(base_hex_x, [xy_y]*6, 'k-', lw=2)
    # Projection lines
    for x in base_hex_x:
        ax.plot([x, x], [xy_y, apex_y], 'grey', lw=1, linestyle='--')
    # Axis
    ax.plot([mx, mx], [xy_y, apex_y], 'b--', lw=2)
    ax.text(mx, apex_y+7, "O' (Apex in FV)", ha='center', fontsize=11)
    ax.text(mx, (apex_y+xy_y)/2, "^ Axis (65mm)", fontsize=10, color='b')
    ax.text(mx, xy_y-4, "M' (midpoint of axis)", ha='center', color='tab:orange', fontsize=11)
    for i, x in enumerate(base_hex_x):
        lbl = chr(ord('A')+i)+"'"
        ax.text(x, xy_y-7, lbl, ha='center', fontsize=10)
    # Section plane trace
    from math import radians, tan
    section_x1 = mx - (apex_y-xy_y)/tan(radians(section_angle))/2
    section_x2 = mx + (apex_y-xy_y)/tan(radians(section_angle))/2
    ax.plot([section_x1, section_x2], [apex_y/2]*2, color='tab:orange', lw=2)
    ax.text(section_x2+7, apex_y/2, f"Section Plane (Trace, {section_angle}°)", color='tab:orange', fontsize=9)
    ax.set_xlim(margin-10, margin+dx*5+15)
    ax.set_ylim(xy_y-20, apex_y+20)

    # --- Sectional Top View ---
    ax = axes[1]
    ax.axis('off')
    ax.set_title("Sectional Top View (Plan)", fontsize=12, weight='bold')
    # Hexagon base
    r = base_side
    hex_theta = np.linspace(np.pi/6, 2*np.pi+np.pi/6, 7)
    hex_x = r*np.cos(hex_theta)
    hex_y = r*np.sin(hex_theta)
    ax.plot(hex_x, hex_y, 'k-', lw=2)
    # "Section polygon" (concept only!)
    cut_pts_x = [hex_x[i]+i*1 for i in range(6)]  # offset for concept effect
    cut_pts_y = [hex_y[i]+7 for i in range(6)]
    ax.plot(cut_pts_x+[cut_pts_x[0]], cut_pts_y+[cut_pts_y[0]], 'tab:red', lw=2)
    ax.fill(cut_pts_x, cut_pts_y, 'tab:red', alpha=0.18)
    for i in range(6):
        ax.plot([hex_x[i], cut_pts_x[i]], [hex_y[i], cut_pts_y[i]], 'k--', lw=0.7)
        ax.text(cut_pts_x[i], cut_pts_y[i]+3, f"P{i+1}", color='tab:red', fontsize=9)
    ax.text(0, -r-8, "Sectioned area (hatched)", ha='center', color='tab:red', fontsize=10)
    ax.set_xlim(-r*1.5, r*1.5)
    ax.set_ylim(-r*1.7, r*1.7)

    # --- True Shape ---
    ax = axes[2]
    ax.axis('off')
    ax.set_title("True Shape of Section", fontsize=12, weight='bold')
    angles2 = np.linspace(0, 2*np.pi, 7)[:-1] + 0.12
    rad2 = r*0.85
    ts_x = rad2*np.cos(angles2)
    ts_y = rad2*np.sin(angles2)
    ax.plot(ts_x, ts_y, color='tab:red', lw=2)
    ax.fill(ts_x, ts_y, 'tab:red', alpha=0.2)
    for i in range(6):
        ax.text(ts_x[i]*1.09, ts_y[i]*1.08, f"P{i+1}''", ha='center', fontsize=10)
    ax.text(0, 0, "True Shape (hatched)", ha='center', color='tab:red', fontsize=11)
    ax.set_xlim(-rad2*1.5, rad2*1.5)
    ax.set_ylim(-rad2*1.2, rad2*1.35)

    return fig
    
