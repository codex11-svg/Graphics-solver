import numpy as np

def solve_2d_line_length(angle_deg, base_length):
    """
    Calculates the vertical height (opposite) of a right-angled triangle
    given the base and angle in degrees.
    """
    try:
        angle_rad = np.radians(angle_deg)
        vertical_height = base_length * np.tan(angle_rad)
        return {
            "vertical_height": vertical_height,
            "base": base_length,
            "angle": angle_deg
        }
    except Exception as e:
        return {"error": str(e)}
