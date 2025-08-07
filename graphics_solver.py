import streamlit as st
import solver
import google.generativeai as genai
import matplotlib.pyplot as plt
from PIL import Image
import io

# Initialize Gemini
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    st.error("Gemini API Key is missing. Please add it to Streamlit secrets.")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)

st.title("Engineering Graphics Solver 🚀")
st.write(
    "Type your graphics or geometry question, and/or upload an image. "
    "Get instant solutions powered by Gemini AI, plus interactive 2D calculations."
)

# --- Input Section ---
st.header("Input Problem")

question = st.text_area(
    "Type your engineering graphics question:",
    height=100,
    help="Ask a technical drawing, construction, or geometry question."
)
image_file = st.file_uploader(
    "Optionally upload a graphic or drawing (PNG, JPG, JPEG):",
    type=["png", "jpg", "jpeg"]
)

# Show image preview
if image_file:
    try:
        img = Image.open(io.BytesIO(image_file.getvalue()))
        st.image(img, caption="Uploaded Image", use_column_width=True)
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
        # Plot triangle
        fig, ax = plt.subplots()
        ax.plot([0, sol['base']], [0, 0], 'bo-', label='Base')
        ax.plot([sol['base'], sol['base']], [0, sol['vertical_height']], 'ro-', label='Vertical')
        ax.plot([0, sol['base']], [0, sol['vertical_height']], 'go-', label='Hypotenuse')
        ax.legend()
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Right Triangle Visualization")
        st.pyplot(fig)

st.header("AI-Powered Gemini Solution")

if st.button("Submit Question to Gemini"):
    # Prepare Gemini prompt
    contents = []
    if question.strip():
        contents.append(question.strip())
    if image_file:
        try:
            image_bytes = image_file.read()
            from google.genai import types
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=image_file.type))
        except Exception as e:
            st.error(f"Could not process uploaded image: {e}")
    
    if not contents:
        st.warning("Please enter a question or upload an image.")
    else:
        with st.spinner("Gemini is analyzing your input..."):
            try:
                response = genai.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents
                )
                output_text = getattr(response, "text", None) or str(response)
                st.success("Gemini AI Solution:")
                st.write(output_text)
            except Exception as e:
                st.error(f"Error from Gemini: {e}")
