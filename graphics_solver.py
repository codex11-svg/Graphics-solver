import streamlit as st
import solver
import google.generativeai as genai
import matplotlib.pyplot as plt
from PIL import Image
import io
import numpy as np
from streamlit_drawable_canvas import st_canvas

# --- Gemini API Setup ---
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    st.error("Gemini API Key is missing. Please add it to Streamlit secrets.")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("Engineering Graphics Solver 🚀")
st.write(
    "Type a graphics/geometry question, draw a diagram below, or upload an image. "
    "Get instant solutions powered by Gemini AI, plus interactive 2D calculations."
)

# --- Input Section ---
st.header("Input Problem")

question = st.text_area(
    "Type your engineering graphics question:",
    height=100,
    help="Ask a technical drawing, construction, or geometry question."
)

# --- Virtual Drawing Section ---
st.subheader("Draw a Diagram Virtually")
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # transparent orange
    stroke_width=2,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=300,
    width=400,
    drawing_mode="freedraw",   # Options: "freedraw", "line", "rect", etc.
    key="canvas"
)

# Turn Canvas Result into Gemini-compatible image (if drawn)
virtual_draw_bytes = None
if canvas_result.image_data is not None:
    try:
        im_array = (canvas_result.image_data * 255).astype(np.uint8)
        im_pil = Image.fromarray(im_array)
        buf = io.BytesIO()
        im_pil.save(buf, format="PNG")
        virtual_draw_bytes = buf.getvalue()
        st.image(im_pil, caption="Your Drawing", use_column_width=True)
    except Exception:
        st.warning("Couldn't process the drawn image.")

# --- Optional File Upload Section ---
image_file = st.file_uploader(
    "Or, upload a graphic or drawing (PNG, JPG, JPEG):",
    type=["png", "jpg", "jpeg"]
)
upload_bytes = None
if image_file:
    try:
        img = Image.open(io.BytesIO(image_file.getvalue()))
        st.image(img, caption="Uploaded Image", use_column_width=True)
        upload_bytes = image_file.read()
    except Exception:
        st.warning("Uploaded file could not be previewed as an image.")

# --- Numeric Example Demo ---
st.subheader("2D Geometry Instant Demo")
col1, col2 = st.columns(2)
with col1:
    base = st.number_input("Base length", value=10.0)
with col2:
    angle = st.number_input("Angle (degrees)", value=30.0)

if st.button("Solve Demo 2D Problem"):
    sol = solver.solve_2d_line_length(angle, base)
    if "error" in sol:
        st.error("Error in calculation: " + sol["error"])
    else:
        st.success(f"Vertical Height: {sol['vertical_height']:.2f}")
        fig, ax = plt.subplots()
        ax.plot([0, sol['base']], [0, 0], 'bo-', label='Base')
        ax.plot([sol['base'], sol['base']], [0, sol['vertical_height']], 'ro-', label='Vertical')
        ax.plot([0, sol['base']], [0, sol['vertical_height']], 'go-', label='Hypotenuse')
        ax.legend()
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Right Triangle Visualization")
        st.pyplot(fig)

# --- Gemini AI Solution Section ---
st.header("AI-Powered Gemini Solution")

if st.button("Submit Question to Gemini"):
    from google.genai import types
    contents = []
    if question.strip():
        contents.append(question.strip())
    # Prefer virtual draw (if any), otherwise uploaded image
    if virtual_draw_bytes:
        contents.append(types.Part.from_bytes(data=virtual_draw_bytes, mime_type="image/png"))
    elif upload_bytes:
        contents.append(types.Part.from_bytes(data=upload_bytes, mime_type=image_file.type))
    if not contents:
        st.warning("Please enter a question, draw a diagram, or upload an image.")
    else:
        with st.spinner("Gemini is analyzing your input..."):
            try:
                response = model.generate_content(contents)
                output_text = getattr(response, "text", None) or str(response)
                st.success("Gemini AI Solution:")
                st.write(output_text)
            except Exception as e:
                st.error(f"Error from Gemini: {e}")
