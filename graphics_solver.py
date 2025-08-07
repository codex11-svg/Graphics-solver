import streamlit as st
import solver
import google.generativeai as genai

st.title("Engineering Graphics Solver 🚀")
st.write(
    "Enter a classic descriptive engineering graphics problem (e.g., about pyramids, sections, projections). "
    "You'll receive a Gemini AI expert answer and an automated 3D diagram."
)

# Gemini API
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    st.error("Gemini API Key is missing. Add it to Streamlit secrets.")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

question = st.text_area("Enter your question:", height=140)
if st.button("Solve with Gemini & Virtual Diagram") and question.strip():
    # 1. Step-by-step Gemini answer
    with st.spinner("Gemini is analyzing your question..."):
        try:
            response = model.generate_content([question.strip()])
            st.success("Gemini AI Solution:")
            st.write(getattr(response, "text", None) or str(response))
        except Exception as e:
            st.error(f"Error from Gemini: {e}")

    # 2. Virtual 3D Diagram (auto-detects hex pyramid with inclined cut)
    if "pyramid" in question.strip().lower() and "base" in question.lower() and "axis" in question.lower():
        params = solver.parse_hex_pyramid_section(question)
        fig = solver.plot_hex_pyramid_with_section(
            base_side=params['base_side'],
            axis_height=params['axis_height'],
            section_angle_deg=params['section_angle']
        )
        st.markdown("**Automated 3D Diagram:**")
        st.pyplot(fig)
    else:
        st.info("Diagram generation currently supports classic hexagonal pyramid with section problems. Expandable to more shapes—just ask!")

st.markdown(
    """
    ℹ️ **Example question:**  
    "A hexagonal pyramid base 30 mm side, axis 65 mm long has its base on H.P. with an edge of base parallel to V.P. A section plane perpendicular to V.P. and inclined at 60º to H.P. bisects the axis of the pyramid. Draw front view, sectional top view and true shape of the section."
    """
)
