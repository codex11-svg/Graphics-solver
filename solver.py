import numpy as np
import matplotlib.pyplot as plt
import re

def classify_problem_type(question):
    q = question.lower()
    if 'hexagonal' in q and 'pyramid' in q: return 'hex_pyramid'
    elif 'square' in q and 'prism' in q: return 'square_prism'
    elif 'triangular' in q and 'prism' in q: return 'tri_prism'
    elif 'cylinder' in q: return 'cylinder'
    elif 'cone' in q: return 'cone'
    elif 'frustum' in q or 'truncated' in q: return 'frustum'
    elif 'sphere' in q: return 'sphere'
    elif ('penetration' in q or 'intersection' in q or 'combined' in q): return 'combined'
    return None

def parse_hex_pyramid_section(question):
    base = re.search(r'base\s*(\d+(\.\d+)?)', question)
    axis = re.search(r'axis\s*(\d+(\.\d+)?)', question)
    angle = re.search(r'inclined\s*at\s*(\d+(\.\d+)?)', question)
    base_side = float(base.group(1)) if base else 30.0
    axis_height = float(axis.group(1)) if axis else 65.0
    section_angle = float(angle.group(1)) if angle else 60.0
    return dict(base_side=base_side, axis_height=axis_height, section_angle=section_angle)

def plot_hex_pyramid_conceptual(base_side=30, axis_height=65, section_angle=60):
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
    ax.plot(base_hex_x, [xy_y]*6, 'k-', lw=2)
    for x in base_hex_x:
        ax.plot([x, x], [xy_y, apex_y], 'grey', lw=1, linestyle='--')
    ax.plot([mx, mx], [xy_y, apex_y], 'b--', lw=2)
    ax.text(mx, apex_y+7, "O' (Apex in FV)", ha='center', fontsize=11)
    ax.text(mx, (apex_y+xy_y)/2, f"^ Axis ({axis_height} mm)", fontsize=10, color='b')
    ax.text(mx, xy_y-4, "M' (midpoint of axis)", ha='center', color='tab:orange', fontsize=11)
    for i, x in enumerate(base_hex_x):
        lbl = chr(ord('A')+i)+"'"
        ax.text(x, xy_y-7, lbl, ha='center', fontsize=10)
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
    r = base_side
    hex_theta = np.linspace(np.pi/6, 2*np.pi+np.pi/6, 7)
    hex_x = r*np.cos(hex_theta)
    hex_y = r*np.sin(hex_theta)
    ax.plot(hex_x, hex_y, 'k-', lw=2)
    cut_pts_x = [hex_x[i]+i*1 for i in range(6)]
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

def parse_square_prism_section(question):
    base = re.search(r'base\s*(\d+(\.\d+)?)', question)
    axis = re.search(r'axis\s*(\d+(\.\d+)?)', question)
    angle = re.search(r'inclined\s*at\s*(\d+(\.\d+)?)', question)
    base_side = float(base.group(1)) if base else 40.0
    axis_height = float(axis.group(1)) if axis else 70.0
    section_angle = float(angle.group(1)) if angle else 45.0
    return dict(base_side=base_side, axis_height=axis_height, section_angle=section_angle)

def plot_square_prism_conceptual(base_side=40, axis_height=70, section_angle=45):
    fig, axes = plt.subplots(3, 1, figsize=(10, 9))
    fig.subplots_adjust(hspace=0.5)
    ax = axes[0]
    ax.set_title("Front View (Elevation)", fontsize=12, weight='bold')
    ax.axis('off')
    left = 10; right = left + base_side
    xy = 10; top = xy + axis_height
    ax.plot([left, right], [xy, xy], 'k-', lw=2)
    ax.plot([left, left], [xy, top], 'grey', lw=1)
    ax.plot([right, right], [xy, top], 'grey', lw=1)
    mid = (left + right)/2
    ax.plot([mid, mid], [xy, top], 'b--', lw=2)
    from math import tan, radians
    sx1 = mid - axis_height/2 / tan(radians(section_angle))/2
    sx2 = mid + axis_height/2 / tan(radians(section_angle))/2
    sy = (xy + top)/2
    ax.plot([sx1, sx2], [sy, sy], color='tab:orange', lw=2)
    ax.text(left, xy-5, "A'", ha='center')
    ax.text(right, xy-5, "D'", ha='center')
    ax.text(mid, top+7, "O' (Centroid/FV)", ha='center')
    ax.text(mid, sy+5, "Section plane (trace)", color='tab:orange')
    ax = axes[1]
    ax.set_title("Sectional Top View (Plan)", fontsize=12, weight='bold')
    ax.axis('off')
    base_x = [left, right, right, left]
    base_y = [xy, xy, xy+base_side, xy+base_side]
    ax.plot(base_x+[base_x[0]], base_y+[base_y[0]], 'k-', lw=2)
    ax.fill_between([left, right], xy, xy+base_side, color='tab:red', alpha=0.2)
    for i, (x, y) in enumerate(zip(base_x, base_y)):
        ax.text(x-2, y-2, chr(ord('A')+i), fontsize=10)
    ax.text((left+right)/2, xy-7, "Base ABCD (Plan)", ha='center')
    ax = axes[2]
    ax.set_title("True Shape of Section", fontsize=12, weight='bold')
    ax.axis('off')
    ts_x = np.array([0, base_side, base_side*1.15, base_side*0.15, 0])
    ts_y = np.array([0, 0, base_side*0.8, base_side*0.8, 0])
    ax.plot(ts_x, ts_y, 'tab:red', lw=2)
    ax.fill(ts_x, ts_y, 'tab:red', alpha=0.2)
    ax.text(base_side/2, base_side*0.9, "True Shape (hatched)", color='tab:red', ha='center', fontsize=11)
    return fig

def parse_tri_prism_section(question):
    base = re.search(r'base\s*(\d+(\.\d+)?)', question)
    axis = re.search(r'axis\s*(\d+(\.\d+)?)', question)
    angle = re.search(r'inclined\s*at\s*(\d+(\.\d+)?)', question)
    base_side = float(base.group(1)) if base else 35.0
    axis_height = float(axis.group(1)) if axis else 60.0
    section_angle = float(angle.group(1)) if angle else 45.0
    return dict(base_side=base_side, axis_height=axis_height, section_angle=section_angle)

def plot_tri_prism_conceptual(base_side=35, axis_height=60, section_angle=45):
    fig, axes = plt.subplots(3, 1, figsize=(10, 9))
    fig.subplots_adjust(hspace=0.5)
    # --- FV ---
    ax = axes[0]
    ax.set_title("Front View (Elevation)", fontsize=12, weight='bold')
    ax.axis('off')
    base_x = [15, 15+base_side, 15+base_side/2]
    base_y = [10, 10, 10+base_side*np.sin(np.pi/3)]
    top_y = [y+axis_height for y in base_y]
    ax.plot(base_x + [base_x[0]], base_y + [base_y[0]], 'k-', lw=2)
    for x, y in zip(base_x, base_y):
        ax.plot([x, x], [y, y+axis_height], 'grey', lw=1, linestyle='--')
    ax.plot([np.mean(base_x), np.mean(base_x)], [min(top_y), max(top_y)], 'b--', lw=2)
    from math import tan, radians
    mx = np.mean(base_x)
    y_mid = (min(top_y)+max(top_y))/2
    sx1 = mx - axis_height/2/tan(radians(section_angle))/2
    sx2 = mx + axis_height/2/tan(radians(section_angle))/2
    ax.plot([sx1, sx2], [y_mid, y_mid], color='tab:orange', lw=2)
    ax.text(mx, min(top_y)-7, "B'", ha='center')
    ax.text(mx, max(top_y)+10, "O' (Centroid/FV)", ha='center')
    ax.text(mx, y_mid+7, "Section Plane", color="tab:orange")
    # --- TV ---
    ax = axes[1]
    ax.set_title("Sectional Top View (Plan)", fontsize=12, weight='bold')
    ax.axis('off')
    base_tx = [15, 15+base_side, 15+base_side/2]
    base_ty = [20, 20, 20+base_side*np.sin(np.pi/3)]
    ax.plot(base_tx + [base_tx[0]], base_ty + [base_ty[0]], 'k-', lw=2)
    ax.fill(base_tx + [base_tx[0]], [ty+10 for ty in base_ty]+[base_ty[0]+10], 'tab:red', alpha=0.15)
    ax.text(np.mean(base_tx), 20-6, "Base (Plan)", ha='center')
    # --- True Shape ---
    ax = axes[2]
    ax.set_title("True Shape of Section", fontsize=12, weight='bold')
    ax.axis('off')
    angles2 = np.linspace(0, 2*np.pi, 4)[:-1] + 0.15
    rad2 = base_side*0.7
    ts_x = rad2*np.cos(angles2)
    ts_y = rad2*np.sin(angles2)
    ax.plot(ts_x, ts_y, color='tab:red', lw=2)
    ax.fill(ts_x, ts_y, 'tab:red', alpha=0.2)
    for i in range(3):
        ax.text(ts_x[i]*1.1, ts_y[i]*1.1, f"P{i+1}''", ha='center', fontsize=10)
    ax.text(0, 0, "True Shape (hatched)", ha='center', color='tab:red', fontsize=11)
    ax.set_xlim(-rad2*1.5, rad2*1.5)
    ax.set_ylim(-rad2*1.2, rad2*1.35)
    return fig
    
