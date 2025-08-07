import numpy as np
import matplotlib.pyplot as plt

def plot_hex_pyramid_conceptual(base_side=30, axis_height=65, section_angle=60):
    """
    Draws the classic FV (front view), sectional TV (top view), and true shape diagram
    for a hexagonal pyramid with a section plane inclined to HP.
    Returns matplotlib fig.
    """
    fig, axes = plt.subplots(3, 1, figsize=(11, 10))
    fig.subplots_adjust(hspace=0.4)

    # --- FV (Front View) ---
    ax = axes[0]
    ax.set_title("Front View (Elevation)", fontsize=12, weight='bold')
    ax.axis('off')
    # Apex, base on XY, axis
    dx = base_side*1.1
    margin = 10
    xy_y = margin
    apex_y = xy_y + axis_height
    base_hex_x = np.linspace(margin, margin+dx*5, 6)
    # Draw base
    ax.plot(base_hex_x, [xy_y]*6, 'k-', lw=2)
    for x in base_hex_x:
        ax.plot([x, x], [xy_y, apex_y], 'grey', lw=1, linestyle='--')
    # Draw axis
    mx = base_hex_x[2]+(base_hex_x[3]-base_hex_x[2])/2
    ax.plot([mx, mx], [xy_y, apex_y], 'b--', lw=2)
    ax.text(mx, apex_y+7, "O'", ha='center', fontsize=11)
    ax.text(mx, xy_y-4, "M' (midpoint)", ha='center', color='tab:orange', fontsize=11)
    for i, x in enumerate(base_hex_x):
        lbl = chr(ord('A')+i)+"'"
        ax.text(x, xy_y-7, lbl, ha='center', fontsize=10)
    # Section plane trace through mid axis at 60 deg
    from math import radians, tan
    section_x1 = mx - (apex_y-xy_y)/tan(radians(section_angle))/2
    section_x2 = mx + (apex_y-xy_y)/tan(radians(section_angle))/2
    ax.plot([section_x1, section_x2], [apex_y/2]*2, color='tab:orange', lw=2)
    ax.text(section_x2+5, apex_y/2, "Section Plane Trace (60°)", color='tab:orange', fontsize=9)
    ax.set_xlim(margin-10, margin+dx*5+10)
    ax.set_ylim(xy_y-20, apex_y+20)

    # --- Sectional Top View ---
    ax = axes[1]
    ax.axis('off')
    ax.set_title("Sectional Top View (Plan)", fontsize=12, weight='bold')
    # Hexagon base (6 points)
    r = base_side
    hex_theta = np.linspace(np.pi/6, 2*np.pi+np.pi/6, 7)
    hex_x = r*np.cos(hex_theta)
    hex_y = r*np.sin(hex_theta)
    ax.plot(hex_x, hex_y, 'k-', lw=2)
    # Section polygon points (arbitrary hatch for concept)
    cut_pts_x = [hex_x[i] for i in [0,1,2,3,4,5]]
    cut_pts_y = [hex_y[i]+10 for i in [0,1,2,3,4,5]]
    ax.plot(cut_pts_x, cut_pts_y, 'tab:red', lw=2)
    ax.fill(cut_pts_x, cut_pts_y, 'tab:red', alpha=0.2)
    # Hatch the section
    for i in range(6):
        ax.plot([hex_x[i], cut_pts_x[i]], [hex_y[i], cut_pts_y[i]], 'k--', lw=0.7)
    ax.text(0, -r-8, "Sectional area (hatched)", ha='center', color='tab:red', fontsize=10)
    ax.set_xlim(-r*1.5, r*1.5)
    ax.set_ylim(-r*1.7, r*1.7)

    # --- True Shape of Section ---
    ax = axes[2]
    ax.axis('off')
    ax.set_title("True Shape of Section", fontsize=12, weight='bold')
    # Draw as irregular hexagon to show true shape
    angles2 = np.linspace(0, 2*np.pi, 7)[:-1] + 0.1
    rad2 = r*0.85
    ts_x = rad2*np.cos(angles2)
    ts_y = rad2*np.sin(angles2)
    ax.plot(ts_x, ts_y, color='tab:red', lw=2)
    ax.fill(ts_x, ts_y, 'tab:red', alpha=0.2)
    for i in range(6):
        ax.text(ts_x[i]*1.07, ts_y[i]*1.07, f"P{i+1}''", ha='center', fontsize=10)
    ax.text(0, 0, "True Shape (hatched)", ha='center', color='tab:red', fontsize=11)
    ax.set_xlim(-rad2*1.5, rad2*1.5)
    ax.set_ylim(-rad2*1.2, rad2*1.35)

    return fig
    
